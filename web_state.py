"""
web_state.py - Thread-safe shared state for the background update worker.

All communication between the Flask routes and the worker thread goes
through this module.  No locking primitives are exposed outside.
"""

import threading
from datetime import datetime
from typing import Any, Dict, List, Optional


class UpdateState:
    """
    Singleton-style class that holds the live state of the update job.
    All public methods are thread-safe.
    """

    _lock: threading.Lock = threading.Lock()

    # ---- internal mutable state ----------------------------------------
    _running: bool = False
    _stop_requested: bool = False
    _logs: List[str] = []
    _progress: float = 0.0
    _total: int = 0
    _processed: int = 0
    _success: int = 0
    _failed: int = 0
    _current_username: str = ""
    _started_at: Optional[datetime] = None
    _finished_at: Optional[datetime] = None
    _status: str = "idle"            # idle | running | completed | failed
    _last_run_time: str = "Never"
    _last_status: str = "N/A"
    _last_updated_records: int = 0
    _last_execution_time: str = "N/A"

    # -----------------------------------------------------------------------
    # Mutation helpers (called by updater.py)
    # -----------------------------------------------------------------------

    @classmethod
    def reset(cls) -> None:
        """Reset all per-run counters before a new job starts."""
        with cls._lock:
            cls._running = False
            cls._logs = []
            cls._progress = 0.0
            cls._total = 0
            cls._processed = 0
            cls._success = 0
            cls._failed = 0
            cls._current_username = ""
            cls._started_at = None
            cls._finished_at = None
            cls._status = "idle"
            cls._stop_requested = False

    @classmethod
    def set_running(cls, value: bool) -> None:
        with cls._lock:
            cls._running = value
            if value:
                cls._status = "running"
                cls._started_at = datetime.now()

    @classmethod
    def set_total(cls, total: int) -> None:
        with cls._lock:
            cls._total = total

    @classmethod
    def add_log(cls, line: str) -> None:
        """Append a log line (timestamped)."""
        ts = datetime.now().strftime("%H:%M:%S")
        with cls._lock:
            cls._logs.append(f"[{ts}] {line}")

    @classmethod
    def increment_processed(cls, username: str, success: bool) -> None:
        with cls._lock:
            cls._processed += 1
            if success:
                cls._success += 1
            else:
                cls._failed += 1
            cls._current_username = username
            if cls._total > 0:
                cls._progress = round(cls._processed / cls._total * 100, 1)

    @classmethod
    def finish(cls, status: str, execution_time: str) -> None:
        """Mark job as done and capture summary values for the dashboard."""
        with cls._lock:
            cls._running = False
            cls._status = status
            cls._finished_at = datetime.now()
            cls._progress = 100.0 if status == "completed" else cls._progress
            cls._last_run_time = (
                cls._started_at.strftime("%Y-%m-%d %H:%M:%S") if cls._started_at else "N/A"
            )
            cls._last_status = status
            cls._last_updated_records = cls._success
            cls._last_execution_time = execution_time


    @classmethod
    def request_stop(cls) -> None:
        with cls._lock:
            if cls._running:
                cls._stop_requested = True
                cls._status = "stopping"

    @classmethod
    def is_stop_requested(cls) -> bool:
        with cls._lock:
            return cls._stop_requested

    # -----------------------------------------------------------------------
    # Query helpers (called by Flask routes)
    # -----------------------------------------------------------------------

    @classmethod
    def is_running(cls) -> bool:
        with cls._lock:
            return cls._running

    @classmethod
    def get_logs(cls) -> List[str]:
        with cls._lock:
            return list(cls._logs)

    @classmethod
    def get(cls) -> Dict[str, Any]:
        """Return a snapshot of the current state as a plain dict."""
        with cls._lock:
            return {
                "running": cls._running,
                "status": cls._status,
                "progress": cls._progress,
                "total": cls._total,
                "processed": cls._processed,
                "success": cls._success,
                "failed": cls._failed,
                "remaining": max(cls._total - cls._processed, 0),
                "current_username": cls._current_username,
                "last_run_time": cls._last_run_time,
                "last_status": cls._last_status,
                "last_updated_records": cls._last_updated_records,
                "last_execution_time": cls._last_execution_time,
                "success_pct": (
                    round(cls._success / cls._total * 100, 1) if cls._total else 0
                ),
                "stop_requested": cls._stop_requested,
                "failed_pct": (
                    round(cls._failed / cls._total * 100, 1) if cls._total else 0
                ),
            }
