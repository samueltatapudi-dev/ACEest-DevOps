import pytest


@pytest.fixture()
def client():
    from app import app
    with app.test_client() as c:
        yield c


def test_workouts_initially_empty(client):
    resp = client.get("/workouts")
    assert resp.status_code == 200
    assert resp.get_json() == {"workouts": []}


def test_workouts_rejects_negative_duration(client):
    resp = client.post("/workouts", json={"workout": "run", "duration": -5})
    assert resp.status_code == 400
    data = resp.get_json()
    assert "error" in data


def test_workouts_add_and_list(client):
    # add a valid workout
    resp = client.post("/workouts", json={"workout": "run", "duration": 30})
    assert resp.status_code == 201
    item = resp.get_json()
    assert item == {"workout": "run", "duration": 30}

    # now list should include it
    resp2 = client.get("/workouts")
    assert resp2.status_code == 200
    assert {"workout": "run", "duration": 30} in resp2.get_json()["workouts"]
