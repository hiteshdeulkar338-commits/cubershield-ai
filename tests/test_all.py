"""
CyberShield AI - Automated Test Suite
Verifies all heuristic analyzers, database persistence, and API routes.
"""

import os
import sys
import unittest

# Ensure backend folder is on path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "backend"))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app import create_app
from services.url_analyzer import UrlAnalyzer
from services.email_analyzer import EmailAnalyzer
from services.message_analyzer import MessageAnalyzer
from services.score_calculator import SecurityScoreCalculator


class TestHeuristicAnalyzers(unittest.TestCase):
    def setUp(self):
        self.url_analyzer = UrlAnalyzer()
        self.email_analyzer = EmailAnalyzer()
        self.msg_analyzer = MessageAnalyzer()
        self.score_calc = SecurityScoreCalculator()

    def test_url_analyzer_suspicious(self):
        res = self.url_analyzer.analyze("http://secure-login-paypal.xyz")
        self.assertIn("risk_score", res)
        self.assertIn("risk_level", res)
        self.assertIn(res["risk_level"], ["medium", "high", "critical"])
        self.assertGreater(len(res["indicators"]), 0)

    def test_url_analyzer_safe(self):
        res = self.url_analyzer.analyze("https://www.google.com/search?q=cybersecurity")
        self.assertEqual(res["risk_level"], "safe")
        self.assertEqual(res["risk_score"], 0)

    def test_email_analyzer_phishing(self):
        res = self.email_analyzer.analyze(
            subject="Urgent: Your account is suspended!",
            sender="security-alert@paypa1.com",
            body="Immediate action required. Verify your password and OTP within 24 hours to prevent account deletion."
        )
        self.assertIn("risk_score", res)
        self.assertIn(res["risk_level"], ["medium", "high", "critical"])
        self.assertTrue(any("urgency" in str(ind).lower() or "threat" in str(ind).lower() or "spoof" in str(ind).lower() for ind in res["indicators"]))

    def test_message_analyzer_smishing(self):
        res = self.msg_analyzer.analyze(
            message="Dear user, your electricity power will be disconnected at 9:30 PM. Call official officer 9876543210 immediately.",
            msg_type="sms"
        )
        self.assertIn("risk_score", res)
        self.assertIn(res["risk_level"], ["medium", "high", "critical"])

    def test_score_calculator(self):
        answers = {
            "mfa_enabled": True,
            "unique_passwords": True,
            "uses_password_manager": True,
            "automatic_updates": True,
            "screen_lock_enabled": True,
            "regular_backups": True,
            "public_wifi_vpn": True,
            "phishing_vigilance": True
        }
        res = self.score_calc.calculate(answers)
        self.assertIn("overall", res)
        self.assertIn("categories", res)
        self.assertGreater(res["overall"], 80)


class TestAPIRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_health_check(self):
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "operational")

    def test_scan_url_endpoint(self):
        res = self.client.post("/api/scan-url", json={"url": "http://fake-bank-auth.xyz"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertIn("analysis", data)

    def test_analyze_email_endpoint(self):
        res = self.client.post("/api/analyze-email", json={
            "subject": "Important update",
            "sender": "noreply@security.net",
            "body": "Please review your pending notifications here."
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])

    def test_analyze_message_endpoint(self):
        res = self.client.post("/api/analyze-message", json={
            "message": "Click here to claim $500 gift card bonus instantly!",
            "type": "whatsapp"
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])

    def test_education_topics_endpoint(self):
        res = self.client.get("/api/education/topics")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertGreaterEqual(len(data["topics"]), 10)

    def test_glossary_endpoint(self):
        res = self.client.get("/api/glossary?q=phishing")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertGreaterEqual(data["total"], 1)

    def test_dashboard_stats_endpoint(self):
        res = self.client.get("/api/dashboard-stats")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertIn("total_scans", data["stats"])


if __name__ == "__main__":
    unittest.main()
