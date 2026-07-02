"""
app.py - Main Flask application entry point.

Wires together routes, background worker, and serves the web dashboard.
Run with: python app.py
"""

import os
import threading
from datetime import datetime
from flask import Flask, render_template, jsonify, request

from config.config_loader import Config
from utils.logger import configure_logging, logger
from web_state import UpdateState
import database_module as db_module
import updater as updater_module


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )
    app.secret_key = os.urandom(24)

    # Ensure the update_history table exists on startup
    try:
        db_module.ensure_update_history_table()
        logger.info("update_history table is ready.")
    except Exception as exc:
        logger.error("Could not ensure update_history table: %s", exc)

    # Ensure logs directory exists
    os.makedirs(Config.LOG_DIR, exist_ok=True)

    # -----------------------------------------------------------------------
    # Routes
    # -----------------------------------------------------------------------

    @app.route("/", methods=["GET"])
    def index():
        """Dashboard home page."""
        last_run = db_module.fetch_last_run()
        return render_template("index.html", last_run=last_run)

    @app.route("/status", methods=["GET"])
    def status():
        """
        Return the current update job status as JSON.
        Polled by the frontend every 2 seconds via AJAX.
        """
        state = UpdateState.get()
        return jsonify(state)

    @app.route("/start-update", methods=["POST"])
    def start_update():
        """
        Kick off the updater in a background thread.
        Returns 409 if an update is already running.
        """
        if UpdateState.is_running():
            return jsonify({
                "success": False,
                "message": "Update is already running. Please wait for it to finish.",
            }), 409

        # Reset state for a fresh run
        UpdateState.reset()
        UpdateState.set_running(True)

        # Launch the updater in a daemon thread so Flask stays responsive
        worker = threading.Thread(
            target=updater_module.run_update,
            daemon=True,
        )
        worker.start()

        return jsonify({"success": True, "message": "Update started successfully."})

    @app.route("/stop-update", methods=["POST"])
    def stop_update():
        """Request the background updater task to stop."""
        if not UpdateState.is_running():
            return jsonify({
                "success": False,
                "message": "No update process is currently running.",
            }), 400
        UpdateState.request_stop()
        return jsonify({
            "success": True,
            "message": "Stop request submitted. Aborting execution...",
        })

    @app.route("/logs", methods=["GET"])
    def logs():
        """
        Return log lines accumulated since the last update started.
        Frontend polls this every 2 seconds.
        """
        return jsonify({"logs": UpdateState.get_logs()})

    @app.route("/history", methods=["GET"])
    def history():
        """History page showing all previous execution records."""
        records = db_module.fetch_update_history(limit=100)
        return render_template("history.html", records=records)

    @app.route("/history/api", methods=["GET"])
    def history_api():
        """Return history records as JSON."""
        records = db_module.fetch_update_history(limit=100)
        serialised = []
        for row in records:
            serialised.append({
                "id": row["id"],
                "start_time": (
                    row["start_time"].strftime("%Y-%m-%d %H:%M:%S")
                    if row["start_time"] else ""
                ),
                "end_time": (
                    row["end_time"].strftime("%Y-%m-%d %H:%M:%S")
                    if row["end_time"] else ""
                ),
                "status": row["status"],
                "updated_records": row["updated_records"],
                "execution_time": row["execution_time"],
                "log_file": row["log_file"],
            })
        return jsonify(serialised)

    @app.route("/logs/view/<path:filename>", methods=["GET"])
    def view_log_file(filename):
        """Return the contents of a specific log file as JSON."""
        safe_name = os.path.basename(filename)
        log_path = os.path.join(Config.LOG_DIR, safe_name)
        if not os.path.exists(log_path):
            return jsonify({"error": "Log file not found."}), 404
        with open(log_path, "r", encoding="utf-8", errors="replace") as fh:
            content = fh.read()
        return jsonify({"filename": safe_name, "content": content})

    return app


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    configure_logging()
    application = create_app()
    logger.info("Starting Flask web server on http://127.0.0.1:5000")
    application.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
