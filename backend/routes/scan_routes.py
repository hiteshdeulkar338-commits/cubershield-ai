"""
CyberShield AI - Scan & Threat Analysis Routes
Handles endpoints for URL heuristic scanning, email phishing checks,
SMS/messaging fraud detection, and cybersecurity posture scoring.
"""

from flask import Blueprint, request, jsonify
from services.url_analyzer import UrlAnalyzer
from services.email_analyzer import EmailAnalyzer
from services.message_analyzer import MessageAnalyzer
from services.score_calculator import SecurityScoreCalculator
from database.db import add_scan_record

scan_bp = Blueprint("scan", __name__)

url_analyzer = UrlAnalyzer()
email_analyzer = EmailAnalyzer()
message_analyzer = MessageAnalyzer()
score_calculator = SecurityScoreCalculator()


@scan_bp.route("/scan-url", methods=["POST"])
def scan_url():
    """
    POST /api/scan-url
    Analyze URL for security risks, homograph attacks, brand spoofing, and malicious patterns.
    """
    data = request.get_json(silent=True) or {}
    url = data.get("url", "").strip()

    if not url:
        return jsonify({"success": False, "error": "URL field is required"}), 400

    if len(url) > 2048:
        return jsonify({"success": False, "error": "URL exceeds maximum allowed length of 2048 characters"}), 400

    try:
        analysis = url_analyzer.analyze(url)

        # Persist summary to scan history.
        # Store only hostname as summary to prevent saving dangerous URLs directly.
        add_scan_record(
            scan_type="url",
            target_summary=analysis.get("hostname", "unknown_host"),
            risk_level=analysis.get("risk_level", "safe"),
            risk_score=analysis.get("risk_score", 0),
            details={
                "hostname": analysis.get("hostname"),
                "indicator_count": len(analysis.get("indicators", [])),
                "indicators": analysis.get("indicators", []),
                "recommendations": analysis.get("recommendations", [])
            }
        )

        return jsonify({
            "success": True,
            "analysis": analysis
        }), 200

    except Exception as e:
        return jsonify({"success": False, "error": f"Analysis failed: {str(e)}"}), 500


@scan_bp.route("/analyze-email", methods=["POST"])
def analyze_email():
    """
    POST /api/analyze-email
    Evaluate email subject, sender, and content for phishing and social engineering indicators.
    """
    data = request.get_json(silent=True) or {}
    subject = str(data.get("subject", "")).strip()
    sender = str(data.get("sender", "")).strip()
    body = str(data.get("body", "")).strip()

    if not subject or not sender or not body:
        return jsonify({"success": False, "error": "All fields (subject, sender, body) are required"}), 400

    if len(body) > 10000:
        return jsonify({"success": False, "error": "Email body exceeds maximum allowed size (10,000 characters)"}), 400

    if len(subject) > 500 or len(sender) > 320:
        return jsonify({"success": False, "error": "Subject or sender exceeds maximum length limits"}), 400

    try:
        analysis = email_analyzer.analyze(subject, sender, body)

        # Store only subject line summary (max 80 chars), NEVER full email body
        summary = subject[:80] + ("..." if len(subject) > 80 else "")
        add_scan_record(
            scan_type="email",
            target_summary=f"{sender} - {summary}",
            risk_level=analysis.get("risk_level", "safe"),
            risk_score=analysis.get("risk_score", 0),
            details={
                "sender": analysis.get("sender"),
                "subject": summary,
                "indicator_count": len(analysis.get("indicators", [])),
                "indicators": analysis.get("indicators", []),
                "recommendations": analysis.get("recommendations", [])
            }
        )

        return jsonify({
            "success": True,
            "analysis": analysis
        }), 200

    except Exception as e:
        return jsonify({"success": False, "error": f"Email analysis failed: {str(e)}"}), 500


@scan_bp.route("/analyze-message", methods=["POST"])
def analyze_message():
    """
    POST /api/analyze-message
    Inspect SMS/WhatsApp/Telegram messages for smishing, UPI payment scams, and OTP fraud.
    """
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    msg_type = str(data.get("type", "sms")).strip().lower()

    if not message:
        return jsonify({"success": False, "error": "Message content is required"}), 400

    if len(message) > 5000:
        return jsonify({"success": False, "error": "Message exceeds maximum size (5000 characters)"}), 400

    if msg_type not in ("sms", "whatsapp", "telegram", "other"):
        msg_type = "sms"

    try:
        analysis = message_analyzer.analyze(message, msg_type)

        # Store only first 50 characters as preview summary, NEVER entire message
        preview = message[:50].replace("\n", " ") + ("..." if len(message) > 50 else "")
        add_scan_record(
            scan_type="message",
            target_summary=f"[{msg_type.upper()}] {preview}",
            risk_level=analysis.get("risk_level", "safe"),
            risk_score=analysis.get("risk_score", 0),
            details={
                "msg_type": msg_type,
                "preview": preview,
                "indicator_count": len(analysis.get("indicators", [])),
                "indicators": analysis.get("indicators", []),
                "recommendations": analysis.get("recommendations", [])
            }
        )

        return jsonify({
            "success": True,
            "analysis": analysis
        }), 200

    except Exception as e:
        return jsonify({"success": False, "error": f"Message analysis failed: {str(e)}"}), 500


@scan_bp.route("/security-score", methods=["POST"])
def security_score():
    """
    POST /api/security-score
    Evaluate user cybersecurity habits and return a categorized health score and action plan.
    """
    data = request.get_json(silent=True) or {}
    answers = data.get("answers")

    if not isinstance(answers, dict):
        return jsonify({"success": False, "error": "Field 'answers' must be a JSON object"}), 400

    try:
        score_data = score_calculator.calculate(answers)

        # Categorize risk level from overall score
        overall = score_data.get("overall", 0)
        if overall >= 75:
            risk_level = "safe"
        elif overall >= 55:
            risk_level = "low"
        elif overall >= 40:
            risk_level = "medium"
        else:
            risk_level = "high"

        # Record assessment result
        add_scan_record(
            scan_type="score",
            target_summary=f"Security Posture Score: {overall}/100 ({score_data.get('rating')})",
            risk_level=risk_level,
            risk_score=overall,
            details={
                "overall": overall,
                "rating": score_data.get("rating"),
                "categories": score_data.get("categories"),
                "strengths_count": len(score_data.get("strengths", [])),
                "improvements_count": len(score_data.get("improvements", []))
            }
        )

        return jsonify({
            "success": True,
            "score": score_data
        }), 200

    except Exception as e:
        return jsonify({"success": False, "error": f"Score calculation failed: {str(e)}"}), 500
