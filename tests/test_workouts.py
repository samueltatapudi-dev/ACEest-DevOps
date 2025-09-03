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

