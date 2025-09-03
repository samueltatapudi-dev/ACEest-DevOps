import pytest


@pytest.fixture()
def client():
    from app import create_app
    app = create_app()
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


def test_workouts_missing_body_returns_400(client):
    # No JSON body
    resp = client.post("/workouts")
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_workouts_empty_workout_rejected(client):
    resp = client.post("/workouts", json={"workout": "   ", "duration": 10})
    assert resp.status_code == 400
    assert "error" in resp.get_json()


@pytest.mark.parametrize("bad_duration", ["30", 30.5, None])
def test_workouts_non_integer_duration_rejected(client, bad_duration):
    resp = client.post("/workouts", json={"workout": "run", "duration": bad_duration})
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_workouts_missing_duration_key_rejected(client):
    resp = client.post("/workouts", json={"workout": "run"})
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_workouts_large_duration_allowed(client):
    # Large but valid integer should be accepted up to default cap (1440)
    large = 1440
    resp = client.post("/workouts", json={"workout": "ultra", "duration": large})
    assert resp.status_code == 201
    assert resp.get_json() == {"workout": "ultra", "duration": large}


def test_workouts_duration_over_cap_rejected(client):
    resp = client.post("/workouts", json={"workout": "marathon", "duration": 1441})
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_workouts_name_length_cap(client):
    long_name = "x" * 101
    resp = client.post("/workouts", json={"workout": long_name, "duration": 10})
    assert resp.status_code == 400
    assert "error" in resp.get_json()


def test_workouts_reject_duplicate_names(client):
    # Currently not implemented: expecting to fail in CI
    first = client.post("/workouts", json={"workout": "run", "duration": 15})
    assert first.status_code == 201
    # Duplicate name should be rejected (feature gap)
    dup = client.post("/workouts", json={"workout": "run", "duration": 20})
    assert dup.status_code == 400
    assert "error" in dup.get_json()
