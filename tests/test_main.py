from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_home_page():
    response = client.get("/")

    assert response.status_code == 200
    assert "FastAPI File Upload" in response.text

def test_file_too_large():
    large_file = b"x" * (10 * 1024 * 1024 + 1)

    response = client.post(
        "/upload",
        files={
            "file": (
                "large.txt",
                large_file,
                "text/plain"
            )
        }
    )

    assert response.status_code == 200
    assert response.json()["error"] == "File is too large"