# ACEest-DevOps

Beginner-friendly DevOps scaffold for building, testing, containerizing, and deploying a simple Python app.

---

## Folder Structure

```
.
|- app/            # Application code (app.py)
|- tests/          # Pytest tests
|- k8s/            # Kubernetes manifests
|- Dockerfile      # Container build recipe
`- Jenkinsfile     # CI/CD pipeline
```

Note: `tests/test_app.py` expects `app/app.py` to expose a Flask app object named `app` (import path: `from app import app`).

---

## Prerequisites

- Python 3.10+
- Docker Desktop
- kubectl (and a cluster such as Minikube or Docker Desktop Kubernetes)
- Git

---

## Run Locally

```
python -m venv .venv
.venv\Scripts\Activate
pip install -r requirements.txt  # or: pip install flask pytest
python app/app.py
```

---

## Test

```
pytest
```

The sample test performs a GET request to `/` using Flask’s test client and expects HTTP 200.

---

## Docker

```
docker build -t aceest:local .
docker run --rm -p 5000:5000 aceest:local
```

---

## Jenkins (Pipeline)

The included `Jenkinsfile` defines four stages:

- Test: `pytest`
- Build: `docker build -t aceest:${BUILD_NUMBER} .`
- Push: tag and push `samueltatapudi/aceest:${BUILD_NUMBER}`
- Deploy: `kubectl apply -f k8s/`

Configure credentials for Docker Hub and ensure the Jenkins agent has Docker and kubectl available.

---

## Kubernetes

Apply all manifests in `k8s/`:

```
kubectl apply -f k8s/
kubectl get pods,svc -A
```

Ensure your kube-context points to a running cluster.
