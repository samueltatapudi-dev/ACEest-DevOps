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

## Project Summary

This project is a small web application built with Python and Flask. It exposes a simple “workouts” API and also includes a minimal web page you can open in your browser to add and view workouts.

What you can do with it
- Open the app in your browser at `http://localhost:5000` and use a simple page to add a workout (name + duration in minutes) and see the list.
- Use tools like curl or Postman to call the API endpoints directly:
  - `GET /health` — quick health check
  - `GET /workouts` — list workouts
  - `POST /workouts` — add a workout with JSON: `{ "workout": "run", "duration": 30 }`

How the code works (in plain terms)
- The main program is `app.py`.
  - It creates a Flask app (a small web server) in a function called `create_app()`.
  - When you run `python app.py`, the server starts on your computer and listens on port 5000.
  - The page at `/` returns a simple HTML interface (`templates/ui.html`) that uses JavaScript to call the API.
  - The API keeps workouts in memory (a Python list) while the app is running.
  - API rules for adding a workout:
    - `workout` must be a non-empty text and not longer than 100 characters.
    - `duration` must be an integer number of minutes, 0 or more, and not more than 1440 (24 hours).
    - You cannot add two workouts with the same name (not case-sensitive); this prevents duplicates like "Run" and " run ".

How to run it (two simple options)
1) Python (no Docker)
   - Install Python 3.12+, open a terminal, and run:
     - `python -m venv .venv` (create a virtual environment)
     - Windows: `.venv\Scripts\Activate`  |  macOS/Linux: `source .venv/bin/activate`
     - `pip install -r requirements.txt`
     - `python app.py`
     - Open `http://localhost:5000` in your browser.
2) Docker (if you have Docker installed)
   - `docker build -t aceest-app .`
   - `docker run --rm -p 5000:5000 aceest-app`
   - Open `http://localhost:5000` in your browser.

Quality checks (tests and CI)
- Automated tests live in the `tests/` folder and check that the API rules work (e.g., rejecting negative duration, preventing duplicates, etc.).
- GitHub Actions (CI) runs these tests automatically on every push, both on the host and inside a Docker container.

Configuration (optional)
- You can change limits without editing code by setting environment variables:
  - `MAX_DURATION` (default 1440)
  - `MAX_NAME_LEN` (default 100)
  - `PORT` (default 5000)

What this project intentionally keeps simple
- No database: data is stored in memory and will reset when the app restarts.
- No login/auth: anyone who can reach the server can add workouts.

Ideas for future improvements
- Add a database (SQLite/Postgres) so data persists after restart.
- Add user accounts or authentication.
- Add input forms with nicer styling and more UI features.


