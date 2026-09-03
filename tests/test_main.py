from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_home_page():
    response = client.get("/")

    assert response.status_code == 200
    assert "FastAPI File Upload" in response.text