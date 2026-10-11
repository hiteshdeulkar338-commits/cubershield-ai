"""
CyberShield AI - History and Dashboard Routes
Provides access to past scan logs, analytics statistics, and data lifecycle management.
"""

from flask import Blueprint, request, jsonify
from database.db import (
    get_scan_history,
    delete_scan_record,
    clear_history,
    get_dashboard_stats
)

history_bp = Blueprint("history", __name__)


@history_bp.route("/history", methods=["GET"])
def fetch_history():
    """
    GET /api/history
    Retrieve paginated scan history with optional type filter and order.
    Query parameters:
    - type: url | email | message | score
    - sort: date_asc | date_desc
    - limit: integer (default 20, max 100)
    - offset: integer (default 0)
    """
    scan_type = request.args.get("type", None)
    if scan_type and scan_type.lower() in ("all", ""):
        scan_type = None

    sort_param = request.args.get("sort", "date_desc").lower()
    sort_order = "asc" if sort_param == "date_asc" else "desc"

    try:
        limit = int(request.args.get("limit", 20))
    except ValueError:
        limit = 20

    try:
        offset = int(request.args.get("offset", 0))
    except ValueError:
        offset = 0

    try:
        records = get_scan_history(
            scan_type=scan_type,
            sort_order=sort_order,
            limit=limit,
            offset=offset
        )
        return jsonify({
            "success": True,
            "records": records,
            "count": len(records),
            "limit": limit,
            "offset": offset
        }), 200

    except Exception as e:
        return jsonify({"success": False, "error": f"Failed to fetch history: {str(e)}"}), 500


@history_bp.route("/dashboard-stats", methods=["GET"])
def fetch_dashboard_stats():
    """
    GET /api/dashboard-stats
    Fetch aggregate statistics for the dashboard visualization and summary cards.
    """
    try:
        stats = get_dashboard_stats()
        return jsonify({
            "success": True,
            "stats": stats
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": f"Failed to retrieve dashboard stats: {str(e)}"}), 500


@history_bp.route("/history/<int:record_id>", methods=["DELETE"])
def delete_single_record(record_id: int):
    """
    DELETE /api/history/<int:id>
    Delete an individual scan history record.
    """
    try:
        deleted = delete_scan_record(record_id)
        if deleted:
            return jsonify({
                "success": True,
                "message": f"Scan record {record_id} successfully deleted"
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": f"Record with ID {record_id} not found"
            }), 404
    except Exception as e:
        return jsonify({"success": False, "error": f"Failed to delete record: {str(e)}"}), 500


@history_bp.route("/history", methods=["DELETE"])
def clear_all_history():
    """
    DELETE /api/history
    Clear the entire scan history.
    """
    try:
        count = clear_history()
        return jsonify({
            "success": True,
            "message": f"All scan history cleared ({count} records removed)",
            "deleted_count": count
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": f"Failed to clear history: {str(e)}"}), 500
