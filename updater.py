"""
updater.py - Thin wrapper that calls the existing ProfileService logic.

The existing business logic in services/profile_service.py is UNTOUCHED.
This module only orchestrates the call sequence and reports progress back
to UpdateState so the web dashboard can display live status.
"""

import os
import time
from datetime import datetime
from typing import Optional

from config.config_loader import Config
from utils.logger import configure_logging, logger
from services.profile_service import ProfileService
from web_state import UpdateState
import database_module as db_module


def _seconds_to_human(secs: float) -> str:
    """Convert a float number of seconds to a human-readable string."""
    secs = int(secs)
    if secs < 60:
        return f"{secs}s"
    elif secs < 3600:
        return f"{secs // 60}m {secs % 60}s"
    else:
        hours = secs // 3600
        mins = (secs % 3600) // 60
        return f"{hours}h {mins}m"


def run_update() -> None:
    """
    Entry point called from a background thread in app.py.

    Wraps the existing ProfileService.run_streamed_refresh() so that:
      - Live logs are fed into UpdateState
      - Progress counter is updated after each profile
      - Execution is recorded in the update_history MySQL table
      - A per-run log file is saved inside logs/
    """
    configure_logging()

    start_time: datetime = datetime.now()
    log_filename: str = start_time.strftime("%Y-%m-%d_%H-%M") + ".log"
    log_filepath: str = os.path.join(Config.LOG_DIR, log_filename)
    final_status: str = "failed"
    service: Optional[ProfileService] = None

    # Open a dedicated log file for this run
    os.makedirs(Config.LOG_DIR, exist_ok=True)
    log_fh = open(log_filepath, "w", encoding="utf-8")

    def _log(message: str) -> None:
        """Write to UpdateState, the run log file, and the Python logger."""
        UpdateState.add_log(message)
        log_fh.write(message + "\n")
        log_fh.flush()
        logger.info(message)

    try:
        _log("=" * 60)
        _log(f"Update run started at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        _log("=" * 60)

        # ------------------------------------------------------------------
        # Initialise ProfileService (existing logic — not modified)
        # ------------------------------------------------------------------
        _log("Initialising services and connecting to database...")
        service = ProfileService()
        _log("Database connection established.")

        # ------------------------------------------------------------------
        # Count total profiles so we can show progress correctly
        # ------------------------------------------------------------------
        _log("Fetching influencer list from database...")
        all_profiles = list(service.db_manager.iter_usernames())
        total = len(all_profiles)
        UpdateState.set_total(total)
        _log(f"Found {total} profile(s) to update.")

        if total == 0:
            _log("No profiles found. Nothing to do.")
            final_status = "completed"
            return

        # ------------------------------------------------------------------
        # Process each profile using the EXISTING _process_with_error_handling
        # ------------------------------------------------------------------
        run_start = time.time()
        for profile in all_profiles:
            username = profile["username"]
            _log(f"Processing @{username} ...")

            if UpdateState.is_stop_requested():
                _log("Stop request received. Aborting remaining profile updates...")
                final_status = "stopped"
                break

            result = service._process_with_error_handling(profile)

            success = result.get("status") == "success"
            UpdateState.increment_processed(username, success)

            if success:
                scraped = result.get("scraped", {})
                engagement = result.get("engagement", {})
                _log(
                    f"  @{username} updated | "
                    f"followers={scraped.get('followers', 'N/A')} | "
                    f"following={scraped.get('following', 'N/A')} | "
                    f"posts={scraped.get('posts', 'N/A')} | "
                    f"engagement={engagement.get('engagement_rate', 'N/A')}%"
                )
            else:
                _log(f"  @{username} FAILED: {result.get('error', 'Unknown error')}")

            # Brief breathing room between profiles
            time.sleep(0.1)

        elapsed = time.time() - run_start
        exec_time_str = _seconds_to_human(elapsed)
        state = UpdateState.get()
        final_status = "completed"

        _log("")
        _log("=" * 60)
        _log(f"Update completed in {exec_time_str}")
        _log(f"  Total    : {state['total']}")
        _log(f"  Success  : {state['success']}")
        _log(f"  Failed   : {state['failed']}")
        _log("=" * 60)

    except Exception as exc:
        elapsed = time.time() - (start_time.timestamp())
        exec_time_str = _seconds_to_human(elapsed)
        final_status = "failed"
        _log(f"FATAL ERROR: {exc}")
        logger.exception("run_update crashed")

    finally:
        log_fh.close()

        end_time = datetime.now()
        elapsed_secs = (end_time - start_time).total_seconds()
        exec_time_str = _seconds_to_human(elapsed_secs)

        # Mark job as done in UpdateState
        UpdateState.finish(final_status, exec_time_str)

        # Persist execution record in MySQL
        state = UpdateState.get()
        try:
            db_module.record_update_history(
                start_time=start_time,
                end_time=end_time,
                status=final_status,
                updated_records=state["success"],
                execution_time=exec_time_str,
                log_file=log_filename,
            )
        except Exception as db_exc:
            logger.error("Could not record update history: %s", db_exc)

        # Shut down scrapers / DB connections cleanly
        if service is not None:
            try:
                service.shutdown()
            except Exception:
                pass
