import os
from pathlib import Path
from typing import Dict, Any

from flask import Flask, jsonify, request


VERSIONS_DIR = Path(__file__).resolve().parent.parent / "versions"
VERSION_FILE = Path(__file__).resolve().parent / "version.txt"


def _feature_flags(version_name: str) -> Dict[str, Any]:
    """Return a simple feature map derived from selected desktop version name.

    This does not attempt to parse the Tkinter apps. Instead, it toggles
    Flask features to conceptually mirror evolution across versions.
    """
    # Normalize input (e.g., ACEest_Fitness-V1.2.3.py -> V1.2.3)
    base = version_name.strip()
    if base.endswith(".py"):
        base = base[:-3]
    # Defaults (baseline)
    flags = {
        "categories": False,            # V1.1+
        "charts": False,                # V1.2+
        "pdf_export": False,            # V1.3
        "max_duration": 1440,
        "max_name_len": 100,
    }

    if "V1.1" in base:
        flags["categories"] = True
    if "V1.2" in base:
        flags["categories"] = True
        flags["charts"] = True
    if "V1.3" in base:
        flags["categories"] = True
        flags["charts"] = True
        flags["pdf_export"] = True
        flags["max_name_len"] = 120

    return flags


def _load_selected_version() -> str:
    # Priority 1: environment override
    env_ver = os.environ.get("ACEEST_VERSION") or os.environ.get("DESKTOP_VERSION")
    if env_ver:
        return env_ver
    # Priority 2: persisted file
    if VERSION_FILE.exists():
        return VERSION_FILE.read_text(encoding="utf-8").strip()
    # Fallback
    return "ACEest_Fitness-V1.1.py"


def _persist_selected_version(name: str) -> None:
    VERSION_FILE.write_text(name.strip(), encoding="utf-8")


def create_app() -> Flask:
    app = Flask(__name__)

    # In-memory data
    workouts: list[dict] = []

    # Versioning state
    app.config["ACEEST_VERSION"] = _load_selected_version()
    app.config["ACEEST_FLAGS"] = _feature_flags(app.config["ACEEST_VERSION"])

    def _validate_payload(data: dict) -> tuple[bool, str]:
        if not isinstance(data, dict):
            return False, "Invalid or missing JSON body"
        workout = str(data.get("workout", "")).strip()
        if not workout:
            return False, "'workout' is required"
        if len(workout) > int(app.config["ACEEST_FLAGS"].get("max_name_len", 100)):
            return False, "'workout' too long"
        duration = data.get("duration", None)
        if not isinstance(duration, int):
            return False, "'duration' must be an integer"
        if duration <= 0:
            return False, "'duration' must be > 0 minutes"
        if duration > int(app.config["ACEEST_FLAGS"].get("max_duration", 1440)):
            return False, "'duration' too large"
        # Reject duplicate names (case-insensitive)
        normalized = workout.lower()
        if any((w.get("workout", "").strip().lower() == normalized) for w in workouts):
            return False, "workout already exists"
        return True, ""

    @app.get("/")
    def index():
        ver = app.config["ACEEST_VERSION"]
        flags = app.config["ACEEST_FLAGS"]
        return (
            f"ACEest Fitness API (Flask)\n"
            f"Selected desktop version: {ver}\n"
            f"Features: {flags}",
            200,
            {"Content-Type": "text/plain; charset=utf-8"},
        )

    @app.get("/version")
    def version():
        return jsonify({
            "selected": app.config["ACEEST_VERSION"],
            "features": app.config["ACEEST_FLAGS"],
        })

    @app.post("/admin/select-version")
    def admin_select_version():
        data = request.get_json(silent=True) or {}
        name = str(data.get("name", "")).strip()
        if not name:
            return jsonify({"error": "'name' is required"}), 400
        # validate against available files in versions/
        if not (VERSIONS_DIR / name).exists():
            return jsonify({"error": "version file not found in versions/"}), 400
        _persist_selected_version(name)
        app.config["ACEEST_VERSION"] = name
        app.config["ACEEST_FLAGS"] = _feature_flags(name)
        return jsonify({"ok": True, "selected": name, "features": app.config["ACEEST_FLAGS"]})

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    @app.get("/workouts")
    def list_workouts():
        return jsonify({"workouts": workouts})

    @app.post("/workouts")
    def add_workout():
        data = request.get_json(silent=True) or {}
        ok, err = _validate_payload(data)
        if not ok:
            return jsonify({"error": err}), 400
        item = {"workout": data["workout"].strip(), "duration": int(data["duration"]) }
        # Optional categories: include only when explicitly provided
        if app.config["ACEEST_FLAGS"].get("categories") and str(data.get("category", "")).strip():
            item["category"] = str(data.get("category")).strip()
        workouts.append(item)
        return jsonify(item), 201

    return app
