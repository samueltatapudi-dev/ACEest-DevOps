# ACEest Fitness – DevOps Assignment 1

[![CI](https://github.com/samueltatapudi-dev/ACEest-DevOps/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/samueltatapudi-dev/ACEest-DevOps/actions/workflows/ci.yml)

A Flask web application for the **ACEest Fitness** scenario.
This project demonstrates **core DevOps practices**: version control with GitHub, automated testing with Pytest, containerization using Docker, and CI/CD automation via GitHub Actions.

---

## 📌 Features

* Minimal Flask web app with:

  * `GET /health` — service health check
  * `GET /workouts` — list workouts
  * `POST /workouts` — add a workout (JSON body: `{ "workout": "run", "duration": 30 }`)
  * `/` — simple HTML page (`templates/ui.html`) to view/add workouts
* In-memory data (resets on restart)
* Validation rules:

  * Name ≤ 100 chars, no duplicates (case/whitespace-insensitive)
  * Duration between 0–1440 minutes (24 hours)

---

## 🚀 Getting Started

### Option 1: Run Locally (Python)

1. Clone the repo:

   ```bash
   git clone https://github.com/samueltatapudi-dev/ACEest-DevOps.git
   cd ACEest-DevOps
   ```
2. Create a virtual environment:

   * **Windows (PowerShell)**

     ```bash
     python -m venv .venv; .venv\Scripts\Activate
     ```
   * **macOS/Linux**

     ```bash
     python -m venv .venv && source .venv/bin/activate
     ```
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:

   ```bash
   python app.py
   ```

   Open `http://localhost:5000` in your browser.

---

### Option 2: Run with Docker

1. Build the image:

   ```bash
   docker build -t aceest-app .
   ```
2. Run the container:

   ```bash
   docker run --rm -p 5000:5000 aceest-app
   ```
3. Access the app at `http://localhost:5000`.

---

## 🧪 Testing

Run tests locally with:

```bash
pytest -q tests/
```

In Docker:

```bash
docker build -t aceest-app-test .
docker run --rm aceest-app-test pytest -q tests/
```

Tests validate:

* `/health` returns OK
* Workouts API accepts valid input and rejects invalid cases
* Duplicate prevention works

---

## ⚙️ CI/CD with GitHub Actions

Workflow file: `.github/workflows/ci.yml`

On **every push**:

1. **Unit Tests** — Runs `pytest` on the host environment.
2. **Docker Build & Test** — Builds the image and runs `pytest` inside the container.

✅ Ensures code quality, consistency, and reliability before deployment.

---

## 📂 Project Structure

```
.
├── app.py                 # Flask app
├── requirements.txt       # Dependencies
├── Dockerfile             # Container definition
├── templates/ui.html      # Minimal web UI
├── tests/                 # Pytest test cases
└── .github/workflows/ci.yml  # GitHub Actions CI/CD
```

---

## ⚡ Configuration

Environment variables (optional):

* `PORT` (default: 5000)
* `MAX_NAME_LEN` (default: 100)
* `MAX_DURATION` (default: 1440)

Example:

```bash
PORT=8000 MAX_NAME_LEN=50 python app.py
```

---

## 🎯 Project Summary

This project demonstrates the **full DevOps workflow**:

* Code tracked in **Git/GitHub**
* Automated validation with **Pytest**
* Portable builds with **Docker**
* Continuous validation via **GitHub Actions**

It delivers a complete, reproducible pipeline from **development → testing → containerization → CI/CD**, aligned with DevOps best practices and assignment goals.
