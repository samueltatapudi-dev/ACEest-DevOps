# ACEest Fitness - DevOps Assignment 2

End-to-end DevOps implementation for the ACEest Fitness platform covering CI/CD, automated testing, containerization, and progressive delivery.

Key assets:

- Flask API (`app.py`) with HTML UI (`templates/ui.html`)
- Tkinter legacy releases in `versions/`
- Pytest suites (`tests/`)
- Docker image definition (`Dockerfile`)
- Jenkins pipeline (`Jenkinsfile`)
- SonarQube project (`sonar-project.properties`)
- Kubernetes manifests for every rollout mode (`k8s/`)

---

## Repository Layout

```
.
|- app.py                        # Flask microservice
|- ACEest_Fitness.py             # Legacy desktop entry point (baseline)
|- versions/                     # Incremental desktop releases (V1.1 - V1.3)
|- templates/ui.html             # Minimal UI for the API
|- tests/                        # Pytest suites
|- Dockerfile                    # Runtime image
|- Jenkinsfile                   # Jenkins declarative pipeline
|- sonar-project.properties      # SonarQube multi-module settings
`- k8s/                          # Kubernetes manifests for each strategy
```

The `Upgrade/` folder keeps the assignment brief plus the untouched raw drops for audit purposes.

---

## Application Features

- `GET /health` - service liveness probe
- `GET /api` - JSON banner for clients
- `GET /workouts` - list in-memory workouts
- `POST /workouts` - add a workout (`{"workout": "run", "duration": 30}`)
- `/` or `/ui` - HTML page to add and sort workouts

Validation rules:

- `workout` must be non-empty, unique (case-insensitive) and 100 chars or less (overrides via `MAX_NAME_LEN`)
- `duration` must be an integer between 1 and 1440 (overrides via `MAX_DURATION`)

Example overrides:

```
PORT=5000 MAX_NAME_LEN=80 MAX_DURATION=720 python app.py
```

---

## Local Development

```powershell
python -m venv .venv
.venv\Scripts\Activate
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000`.

Tkinter versions live under `versions/` for packaging and demo purposes.

---

## Automated Testing

```
pytest -q
pytest --cov=app --cov-report=xml --junitxml=junit.xml
```

Pytest covers:

- Health endpoint
- Workout validation (duration caps, missing fields, duplicates)
- Happy-path add/list flows

`coverage.xml` feeds SonarQube quality gates.

---

## Docker Image

```
docker build -t aceest-fitness:local .
docker run --rm -p 5000:5000 aceest-fitness:local
```

Environment variables work inside the container the same way (`MAX_*` and `PORT`).

---

## Jenkins Pipeline

`Jenkinsfile` delivers the workflow requested in Assignment 2:

| Stage | Purpose |
| --- | --- |
| Checkout | Check out repo and display git status |
| Setup Python | Create a venv and install dependencies |
| Unit Tests | Run pytest with coverage + JUnit output |
| SonarQube Analysis | Run `sonar-scanner` (server: `SonarQubeServer`) |
| Quality Gate | Block the pipeline until Sonar passes |
| Build Docker Image | Build from `Dockerfile` |
| Push Docker Image | Optional, requires Docker Hub creds (`docker-hub`) |
| Package Legacy Desktop Version | Archive the selected Tkinter file from `versions/` |
| Deploy to Kubernetes | Optional, applies manifests from `k8s/` using `kubeconfig` credentials |

### Pipeline Parameters

- `LEGACY_VERSION`: Tkinter release to archive (choices cover V1.0 - V1.3)
- `RELEASE_VERSION`: tag for artifacts and container (default `v2.0.0`)
- `DOCKER_REPOSITORY`: full repository path (for example `docker.io/example/aceest-fitness`)
- `DEPLOY_STRATEGY`: manifest to apply (`base`, `blue-green`, `canary`, `rolling`, `shadow`, `ab`)
- `PUSH_IMAGE` / `DEPLOY_TO_K8S`: toggle image push and cluster deployment

Agent requirements: Docker CLI, Python 3.12+, `sonar-scanner`, and `kubectl`.

---

## SonarQube

`sonar-project.properties` defines two modules:

- `api` - Flask service and templates (sources) plus `tests/`
- `desktop` - Tkinter history inside `versions/`

Run locally:

```
sonar-scanner ^
  -Dsonar.host.url=https://sonar.example.com ^
  -Dsonar.login=<TOKEN> ^
  -Dsonar.projectVersion=v2.0.0
```

The Jenkins stage uses the configured server alias and waits on the quality gate before proceeding.

---

## Kubernetes Deployment Strategies

`k8s/` includes manifests for every rollout style mentioned in the assignment:

- `base.yaml` - single deployment and service for smoke tests or dev clusters
- `blue-green.yaml` - maintains `blue` (active) and `green` (preview) deployments with swap-able service selectors
- `canary.yaml` - stable plus canary deployments sharing a service (adjust replica counts for weight)
- `rolling.yaml` - tuned `RollingUpdate` example with 4 replicas
- `shadow.yaml` - separate shadow deployment plus ClusterIP service (`aceest-fitness-shadow`) for mirrored traffic
- `ab.yaml` - variant A/B deployments and an NGINX ingress splitting traffic by path or cookie

Minikube quick start:

```
minikube start
kubectl apply -f k8s/base.yaml
kubectl get svc -n aceest
minikube service -n aceest aceest-fitness --url
```

Swap to another strategy by applying the respective YAML after updating the image tags (for example with `kubectl set image deployment/aceest-fitness web=docker.io/<user>/aceest-fitness:v2.0.0 -n aceest`).

---

## Upgrade Artifacts

- `Upgrade/Introduction to DevOps-*.docx` - assignment brief
- `versions/*.py` - provided ACEest desktop versions that must be archived per release

Keep these files intact for audit trails and grading.

---

## Suggested Next Steps

1. Connect GitHub to Jenkins (webhook or poll SCM) for automatic pipeline runs.
2. Push container images to your Docker Hub namespace and update the Kubernetes manifests with real tags.
3. Deploy on Minikube/EKS/AKS/GKE using the provided manifests and capture service URLs plus rollout commands for your report.
4. Export Jenkins logs, SonarQube reports, and Docker Hub screenshots as evidence for Assignment 2 submission.
