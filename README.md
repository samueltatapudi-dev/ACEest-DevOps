# ACEest Fitness Flask App
[![CI](https://github.com/samueltatapudi-dev/ACEest-DevOps/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/samueltatapudi-dev/ACEest-DevOps/actions/workflows/ci.yml)

A minimal Flask application for the ACEest Fitness scenario, with unit tests, a minimal web UI, Docker containerization, and CI via GitHub Actions.

## Getting Started

Run locally with Python or with Docker.

### Option 1: Run with Python
1) Clone the repo and enter the folder
   - `git clone https://github.com/samueltatapudi-dev/ACEest-DevOps.git`
   - `cd ACEest-DevOps`
2) Create and activate a virtual environment
   - Windows (PowerShell): `python -m venv .venv; .venv\\Scripts\\Activate`
   - macOS/Linux: `python -m venv .venv && source .venv/bin/activate`
3) Install dependencies
   - `pip install -r requirements.txt`
4) Run the app
   - `python app.py`
   - Open `http://localhost:5000` for the web UI

Common API endpoints (for curl/Postman):
- `GET /health` — service health
- `GET /workouts` — list workouts
- `POST /workouts` — add a workout with JSON body `{ "workout": "run", "duration": 30 }`
- `GET /api` — JSON index info

Example curl:
```
curl http://localhost:5000/health
curl http://localhost:5000/workouts
curl -X POST http://localhost:5000/workouts \
  -H "Content-Type: application/json" \
  -d '{"workout":"run","duration":30}'
```

### Option 2: Run with Docker
1) Build the image: `docker build -t aceest-app .`
2) Run the container: `docker run --rm -p 5000:5000 aceest-app`
3) Open `http://localhost:5000` for the UI (endpoints above also available).

## CI/CD (GitHub Actions)

The workflow `.github/workflows/ci.yml` runs on every push:
- `unit-tests`: installs dependencies and runs `pytest -q tests/`.
- `docker-tests`: builds the image and runs `pytest -q tests/` inside the container.

## Project Structure

- `app.py`: Flask app, serves UI at `/`, JSON index at `/api`, health and workouts endpoints.
- `templates/ui.html`: Minimal HTML UI to list and add workouts.
- `tests/`: Pytest tests for health, index, workouts validation and flows.
- `requirements.txt`: Python dependencies.
- `Dockerfile`: Container image definition.
- `.github/workflows/ci.yml`: CI pipeline.

## Notes

- Data is in-memory and resets on restart.
- Duplicate workout names are rejected (case/whitespace-insensitive).


