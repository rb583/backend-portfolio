import json
import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime


# ─────────────────────────────────────────────
# Flask App
# ─────────────────────────────────────────────
app = Flask(__name__)

# Allow frontend from Vercel
CORS(app)

CORS(app, origins=[
    "https://frontend-1-xi-five.vercel.app"
])


# ─────────────────────────────────────────────
# Data file path
# ─────────────────────────────────────────────
DATA_FILE = os.path.join(
    os.path.dirname(__file__),
    "data.json"
)


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        return {}

    except json.JSONDecodeError:
        return {}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


# ─────────────────────────────────────────────
# Root Route
# ─────────────────────────────────────────────
@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "message": "Portfolio Backend API running ✅"
    })


# ─────────────────────────────────────────────
# API STATUS
# ─────────────────────────────────────────────
@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": "online",
        "message": "Portfolio API is running ✅",
        "timestamp": datetime.utcnow().isoformat()
    })


# ─────────────────────────────────────────────
# ABOUT
# ─────────────────────────────────────────────
@app.route("/api/about", methods=["GET"])
def about():
    data = load_data()
    return jsonify(data.get("about", {}))


# ─────────────────────────────────────────────
# SKILLS
# ─────────────────────────────────────────────
@app.route("/api/skills", methods=["GET"])
def skills():
    data = load_data()
    return jsonify(data.get("skills", {}))


# ─────────────────────────────────────────────
# PROJECTS
# ─────────────────────────────────────────────
@app.route("/api/projects", methods=["GET"])
def projects():
    data = load_data()
    return jsonify(data.get("projects", []))


# ─────────────────────────────────────────────
# CONTACT FORM
# ─────────────────────────────────────────────
@app.route("/api/contact", methods=["POST"])
def contact():

    body = request.get_json()

    if not body:
        return jsonify({
            "error": "No data received"
        }), 400

    name = body.get("name", "").strip()
    email = body.get("email", "").strip()
    message = body.get("message", "").strip()

    # Validation
    if not name or not email or not message:
        return jsonify({
            "error": "All fields are required"
        }), 400

    if "@" not in email or "." not in email:
        return jsonify({
            "error": "Invalid email address"
        }), 400

    data = load_data()

    # Ensure messages exists
    if "messages" not in data:
        data["messages"] = []

    # Create message entry
    entry = {
        "id": len(data["messages"]) + 1,
        "name": name,
        "email": email,
        "message": message,
        "received": datetime.utcnow().isoformat()
    }

    data["messages"].append(entry)

    save_data(data)

    print(f"[NEW MESSAGE] From: {name} <{email}>")

    return jsonify({
        "success": True,
        "message": "Message received!"
    }), 201


# ─────────────────────────────────────────────
# GET ALL MESSAGES
# ─────────────────────────────────────────────
@app.route("/api/messages", methods=["GET"])
def get_messages():

    data = load_data()

    messages = data.get("messages", [])

    return jsonify({
        "count": len(messages),
        "messages": messages
    })


# ─────────────────────────────────────────────
# Run locally
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
