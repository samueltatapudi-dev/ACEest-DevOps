from flask import Flask, jsonify, request


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def index():
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

        duration = data.get("duration", None)
        if not isinstance(duration, int):
            return jsonify({"error": "'duration' must be an integer"}), 400
        if duration < 0:
            return jsonify({"error": "'duration' must be non-negative"}), 400

        # Reject duplicate workout names (case-insensitive, whitespace-insensitive)
        normalized = workout.lower()
        if any((w.get("workout", "").strip().lower() == normalized) for w in _workouts):
            return jsonify({"error": "workout already exists"}), 400

        item = {"workout": workout, "duration": duration}
        _workouts.append(item)
        return jsonify(item), 201

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
