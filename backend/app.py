"""
CyberShield AI - Main Flask Application Server
Clean, modular Flask application exposing cybersecurity REST APIs,
database connectivity, rate limiting, and static frontend hosting.
"""

import os
import sys
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

# Ensure backend root is on sys.path for robust absolute package resolution
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from database.db import init_db
from routes.scan_routes import scan_bp
from routes.history_routes import history_bp
from routes.education_routes import education_bp

# Load environment configuration (.env)
load_dotenv()

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)


def create_app():
    """
    Application factory pattern to configure and instantiate Flask application.
    """
    frontend_folder = os.path.abspath(os.path.join(CURRENT_DIR, "..", "frontend"))
    app = Flask(__name__, static_folder=frontend_folder, static_url_path="/")

    # Security and size configurations
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024  # 1MB max request size

    # CORS configuration - allow localhost development origins and wildcards for flexibility
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": [
                    "http://localhost:5000",
                    "http://127.0.0.1:5000",
                    "http://localhost:3000",
                    "http://127.0.0.1:3000",
                    "*"
                ]
            }
        }
    )

    # In-memory rate limiting to protect endpoints against brute force and automated scraping
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per hour", "50 per minute"],
        storage_uri="memory://"
    )

    # Initialize SQLite database schema
    init_db()

    # Register API blueprints
    app.register_blueprint(scan_bp, url_prefix="/api")
    app.register_blueprint(history_bp, url_prefix="/api")
    app.register_blueprint(education_bp, url_prefix="/api")

    # API Health Check Endpoint
    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "operational",
            "service": "CyberShield AI",
            "version": "1.0.0",
            "ai_mode": "rule-based" if not os.getenv("OPENAI_API_KEY") else "ai-enhanced"
        }), 200

    # Serve static frontend single page application
    @app.route("/")
    @app.route("/<path:path>")
    def serve_frontend(path=""):
        if path and os.path.exists(os.path.join(app.static_folder, path)):
            return app.send_static_file(path)
        index_file = os.path.join(app.static_folder, "index.html")
        if os.path.exists(index_file):
            return app.send_static_file("index.html")
        return jsonify({
            "service": "CyberShield AI API",
            "status": "operational",
            "message": "Frontend index.html not yet present. API endpoints are ready at /api/*",
            "health": "/api/health"
        }), 200

    # Global Error Handlers
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(429)
    def rate_limit(e):
        return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429

    @app.errorhandler(413)
    def too_large(e):
        return jsonify({"error": "Request too large. Maximum size is 1MB."}), 413

    @app.errorhandler(500)
    def server_error(e):
        logging.error(f"Server error: {e}")
        return jsonify({"error": "Internal server error"}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
