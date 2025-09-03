import pytest


@pytest.fixture()
def client():
    from app import create_app
    app = create_app()
    with app.test_client() as c:
        yield c


def test_health_ok(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_index(client):
    resp = client.get("/api")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["app"] == "ACEest Fitness"
    assert "Welcome" in data["message"]
