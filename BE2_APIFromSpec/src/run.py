"""
Store API - Main entry point.

Run with:
    python run.py

Swagger UI available at:
    http://localhost:5000/swagger/index.html

API base path:
    http://localhost:5000/api/v1/

Environment variables:
    DATABASE_URL - PostgreSQL connection string
                   (e.g. postgresql://user:pass@localhost:5432/store_api)
                   Falls back to SQLite if not set.
    FLASK_ENV   - development / production / testing
    PORT        - Server port (default: 5000)
"""
import os

from app import create_app

config_name = os.environ.get("FLASK_ENV", "development")
app = create_app(config_name)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
