import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_upload_invalid_file_type():
    """Ensure unsupported file types return HTTP 415."""
    response = client.post(
        "/upload",
        files={"file": ("test.txt", b"plain text content", "text/plain")}
    )
    assert response.status_code == 415
    assert "Unsupported file type" in response.json()["detail"]


def test_upload_missing_file():
    """Ensure missing file payload returns HTTP 422 Unprocessable Entity."""
    response = client.post("/upload")
    assert response.status_code == 422
