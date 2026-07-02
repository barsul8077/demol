"""
database_module.py - Database helpers for the web dashboard.

Provides:
  - ensure_update_history_table()   : create table if needed
  - record_update_history(...)      : insert a run record
  - fetch_update_history(limit)     : retrieve past records
  - fetch_last_run()                : convenience for the dashboard card
"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime
from typing import Any, Dict, List, Optional

from config.config_loader import Config
from utils.logger import logger


def get_connection():
    """Create a MySQL connection using the project's config."""
    return mysql.connector.connect(
        host=Config.DB_HOST,
        database=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        autocommit=False,
    )


def test_database_connection() -> None:
    """Raise if the database cannot be reached."""
    connection = None
    try:
        connection = get_connection()
        if not connection.is_connected():
            raise RuntimeError("Database connection did not open.")
        logger.info("Database connection is healthy.")
    finally:
        if connection is not None and connection.is_connected():
            connection.close()


def ensure_update_history_table() -> None:
    """Create the update_history table if it doesn't exist."""
    query = '''
        CREATE TABLE IF NOT EXISTS update_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            start_time DATETIME NOT NULL,
            end_time DATETIME NULL,
            status VARCHAR(20) NOT NULL,
            updated_records INT DEFAULT 0,
            execution_time VARCHAR(50) NULL,
            log_file VARCHAR(255) NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    '''
    connection = None
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query)
        connection.commit()
    except Error as exc:
        logger.error("Could not ensure update_history table: %s", exc)
        raise
    finally:
        if connection is not None and connection.is_connected():
            connection.close()


def record_update_history(
    start_time: datetime,
    end_time: datetime,
    status: str,
    updated_records: int,
    execution_time: str,
    log_file: Optional[str],
) -> None:
    """Insert one execution record into update_history."""
    query = '''
        INSERT INTO update_history
            (start_time, end_time, status, updated_records, execution_time, log_file)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''
    connection = None
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                query,
                (start_time, end_time, status, updated_records, execution_time, log_file),
            )
        connection.commit()
    except Error as exc:
        logger.error("Could not record update history: %s", exc)
        raise
    finally:
        if connection is not None and connection.is_connected():
            connection.close()


def fetch_update_history(limit: int = 50) -> List[Dict[str, Any]]:
    """Return the most recent execution records, newest first."""
    query = '''
        SELECT id, start_time, end_time, status, updated_records, execution_time, log_file
        FROM update_history
        ORDER BY start_time DESC
        LIMIT %s
    '''
    connection = None
    try:
        connection = get_connection()
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query, (limit,))
            return cursor.fetchall()
    except Error as exc:
        logger.error("Could not fetch update history: %s", exc)
        return []
    finally:
        if connection is not None and connection.is_connected():
            connection.close()


def fetch_last_run() -> Optional[Dict[str, Any]]:
    """Return the single most recent execution record, or None."""
    records = fetch_update_history(limit=1)
    return records[0] if records else None


def count_influencers() -> int:
    """Return the total number of rows in the insta_influencers table."""
    query = "SELECT COUNT(*) AS total FROM insta_influencers"
    connection = None
    try:
        connection = get_connection()
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query)
            row = cursor.fetchone()
            return row["total"] if row else 0
    except Error as exc:
        logger.error("Could not count influencers: %s", exc)
        return 0
    finally:
        if connection is not None and connection.is_connected():
            connection.close()
