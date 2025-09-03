# ACEest Fitness Flask App
[![CI](https://github.com/samueltatapudi-dev/ACEest-DevOps/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/samueltatapudi-dev/ACEest-DevOps/actions/workflows/ci.yml)

A minimal Flask application for the ACEest_Fitness and Gym scenario, with unit tests, Docker containerization, and CI via GitHub Actions.

## Local Setup

- Create/activate venv (Windows PowerShell):
  - `python -m venv .venv`
  - `.venv\\Scripts\\Activate`
- Install deps: `pip install -r requirements.txt`
- Run tests: `pytest -q`
- Run app: `python app.py` then open `http://localhost:5000/health`

## Docker

- Build: `docker build -t aceest-app .`
- Run app: `docker run --rm -p 5000:5000 aceest-app`
- Run tests in container: `docker run --rm aceest-app pytest -q`

## CI/CD (GitHub Actions)

The workflow `.github/workflows/ci.yml` runs on every push:
- Native Python job: installs dependencies and runs `pytest`.
- Docker job: builds the image and runs tests inside the container.

## Project Structure

- `app.py`: Flask app with `/` and `/health` endpoints.
- `tests/test_app.py`: Pytest unit tests.
- `requirements.txt`: Python dependencies.
- `Dockerfile`: Container image definition.
- `.github/workflows/ci.yml`: CI pipeline.

## Notes

The GUI script `ACEest_Fitness.py` is unrelated to the Flask web app but kept for reference.


