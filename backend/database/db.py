"""
CyberShield AI - Database Module
SQLite database interface for storing analysis history and dashboard statistics.
Uses parameterized queries to prevent SQL injection vulnerabilities.
"""

import os
import sqlite3
import json
from datetime import datetime, timedelta, timezone

# Database file location: stored locally inside backend/database/cybershield.db
DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "cybershield.db")


def get_db():
    """
    Establish and return a connection to the SQLite database.
    Configures Row factory for dictionary-like column access.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Enable foreign keys and safe concurrent pragmas
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """
    Initialize SQLite tables if they do not already exist.
    Creates scan_history table with proper indexes for fast sorting and filtering.
    """
    os.makedirs(DB_DIR, exist_ok=True)
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS scan_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_type TEXT NOT NULL,
                target_summary TEXT NOT NULL,
                risk_level TEXT NOT NULL,
                risk_score INTEGER NOT NULL,
                details_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        # Create indexes for frequently queried columns
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_scan_type ON scan_history(scan_type)"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_created_at ON scan_history(created_at)"
        )
        conn.commit()


def add_scan_record(scan_type: str, target_summary: str, risk_level: str, risk_score: int, details: dict) -> int:
    """
    Add a new scan result record into the database.
    NEVER store sensitive payloads (e.g. passwords, full email bodies).
    Only sanitized summary strings and structured indicators are persisted.

    :param scan_type: Type of scan ('url', 'email', 'message', 'score')
    :param target_summary: Sanitized summary (e.g., domain name or subject line)
    :param risk_level: 'safe', 'low', 'medium', or 'high'
    :param risk_score: Integer 0-100
    :param details: Dictionary containing indicators and recommendations
    :return: Inserted record ID
    """
    details_str = json.dumps(details)
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO scan_history (scan_type, target_summary, risk_level, risk_score, details_json, created_at)
            VALUES (?, ?, ?, ?, ?, datetime('now'))
            """,
            (scan_type, target_summary, risk_level, int(risk_score), details_str),
        )
        conn.commit()
        return cursor.lastrowid


def get_scan_history(scan_type: str = None, sort_order: str = "desc", limit: int = 50, offset: int = 0) -> list:
    """
    Fetch paginated scan history records with optional type filtering and sorting.

    :param scan_type: Optional filter by scan_type ('url', 'email', 'message', 'score')
    :param sort_order: 'asc' for oldest first, 'desc' for newest first (default)
    :param limit: Maximum records to return (capped at 100 for safety)
    :param offset: Number of records to skip
    :return: List of record dictionaries
    """
    # Enforce strict bounds
    limit = max(1, min(limit, 100))
    offset = max(0, offset)
    direction = "ASC" if str(sort_order).lower() == "asc" else "DESC"

    query = "SELECT id, scan_type, target_summary, risk_level, risk_score, details_json, created_at FROM scan_history"
    params = []

    if scan_type:
        query += " WHERE scan_type = ?"
        params.append(scan_type)

    query += f" ORDER BY created_at {direction} LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()

        results = []
        for row in rows:
            record = dict(row)
            try:
                record["details"] = json.loads(record["details_json"])
            except Exception:
                record["details"] = {}
            del record["details_json"]
            results.append(record)

        return results


def delete_scan_record(record_id: int) -> bool:
    """
    Delete a single scan record by ID.

    :param record_id: Target record ID
    :return: True if record was deleted, False otherwise
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM scan_history WHERE id = ?", (int(record_id),))
        conn.commit()
        return cursor.rowcount > 0


def clear_history() -> int:
    """
    Remove all scan history records.

    :return: Count of deleted rows
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM scan_history")
        deleted_count = cursor.rowcount
        conn.commit()
        return deleted_count


def get_dashboard_stats() -> dict:
    """
    Calculate high-level dashboard metrics for analytics and visualizations:
    - total_scans
    - suspicious_count (risk_level in 'medium', 'high')
    - recent_scans (latest 10 entries)
    - scans_by_type (count grouped by scan_type)
    - scans_by_day (scans per day for the last 7 days)
    """
    with get_db() as conn:
        cursor = conn.cursor()

        # Total scans
        cursor.execute("SELECT COUNT(*) AS total FROM scan_history")
        total_scans = cursor.fetchone()["total"]

        # Suspicious scans count (medium and high risk)
        cursor.execute(
            "SELECT COUNT(*) AS suspicious FROM scan_history WHERE risk_level IN ('medium', 'high')"
        )
        suspicious_count = cursor.fetchone()["suspicious"]

        # Scans grouped by type
        cursor.execute(
            "SELECT scan_type, COUNT(*) as count FROM scan_history GROUP BY scan_type"
        )
        scans_by_type = {row["scan_type"]: row["count"] for row in cursor.fetchall()}

        # Recent scans (latest 10)
        cursor.execute(
            """
            SELECT id, scan_type, target_summary, risk_level, risk_score, details_json, created_at
            FROM scan_history
            ORDER BY created_at DESC
            LIMIT 10
            """
        )
        recent_rows = cursor.fetchall()
        recent_scans = []
        for row in recent_rows:
            r = dict(row)
            try:
                r["details"] = json.loads(r["details_json"])
            except Exception:
                r["details"] = {}
            del r["details_json"]
            recent_scans.append(r)

        # Scans grouped by day for last 7 days
        # Pre-populate dictionary for the past 7 days to guarantee continuous charts
        today = datetime.now(timezone.utc).date()
        date_keys = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
        scans_by_day = {d: 0 for d in date_keys}

        cursor.execute(
            """
            SELECT strftime('%Y-%m-%d', created_at) AS scan_date, COUNT(*) AS count
            FROM scan_history
            WHERE created_at >= date('now', '-6 days')
            GROUP BY scan_date
            """
        )
        for row in cursor.fetchall():
            s_date = row["scan_date"]
            if s_date in scans_by_day:
                scans_by_day[s_date] = row["count"]

        # Format scans_by_day as a sorted list for frontend consumption
        day_series = [{"date": d, "count": scans_by_day[d]} for d in date_keys]

        return {
            "total_scans": total_scans,
            "suspicious_count": suspicious_count,
            "safe_count": max(0, total_scans - suspicious_count),
            "scans_by_type": scans_by_type,
            "scans_by_day": day_series,
            "recent_scans": recent_scans,
        }
