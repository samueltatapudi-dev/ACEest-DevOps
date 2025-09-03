import os
from flask import Flask, jsonify, request, render_template


def create_app() -> Flask:
    app = Flask(__name__)

    # Config with environment overrides
    max_duration = int(os.environ.get("MAX_DURATION", 1440))
    max_name_len = int(os.environ.get("MAX_NAME_LEN", 100))

    @app.get("/")
    def index():
        # Serve the UI at root
        return render_template("ui.html")

    @app.get("/api")
    def api_index():
        # Previous JSON index preserved under /api
        return jsonify({"app": "ACEest Fitness", "message": "Welcome"})

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    # Simple in-memory workouts list for demo purposes
    _workouts: list[dict] = []

    @app.get("/workouts")
    def list_workouts():
        return jsonify({"workouts": _workouts}), 200

    @app.post("/workouts")
    def add_workout():
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"error": "Invalid or missing JSON body"}), 400

        workout = str(data.get("workout", "")).strip()
        if not workout:
            return jsonify({"error": "'workout' is required"}), 400
        if len(workout) > max_name_len:
            return jsonify({"error": f"'workout' length must be <= {max_name_len}"}), 400

        duration = data.get("duration", None)
        if not isinstance(duration, int):
            return jsonify({"error": "'duration' must be an integer"}), 400
        if duration < 0:
            return jsonify({"error": "'duration' must be non-negative"}), 400
        if duration > max_duration:
            return jsonify({"error": f"'duration' must be <= {max_duration}"}), 400

        # Reject duplicate workout names (case-insensitive, whitespace-insensitive)
        normalized = workout.lower()
        if any((w.get("workout", "").strip().lower() == normalized) for w in _workouts):
            return jsonify({"error": "workout already exists"}), 400

        item = {"workout": workout, "duration": duration}
        _workouts.append(item)
        return jsonify(item), 201

    @app.get("/ui")
    def ui():
        return render_template("ui.html")

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


 #ADD TEST CASE FOR DUPLICATE WORKOUT NAMES
 
