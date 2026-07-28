import io

import pytest

from app import create_app

API_URL = "/api/brand-guidelines/upload"


@pytest.fixture
def client():
    flask_app = create_app()
    flask_app.config["TESTING"] = True  # setup
    with flask_app.test_client() as client:
        yield client


## Why does the test client function need to be a generator?
# To setup and teardown the test client cleanly
# Everything before `yield` is the setup
# Everything after is the teardown
# use yield when you want a sequence of values, but don't need them in memory
# all at the same time.
def make_file(content: bytes, filename: str, content_type: str):
    return (io.BytesIO(content), filename, content_type)


def test_missing_file(client):
    response = client.post(API_URL)

    assert response.status_code == 400
    assert response.json == {"success": False, "message": "No file data provided"}


def test_non_pdf_file(client):
    response = client.post(
        API_URL, data={"file": make_file(b"fake", "logo.jpg", "image/jpeg")}
    )

    assert response.status_code == 400
    assert response.json == {"success": False, "message": "File has to be a pdf"}


def test_oversized_file(client):
    big = b"%PDF-1.4 " + b"x" * (11 * 1024 * 1024)

    response = client.post(
        API_URL, data={"file": make_file(big, "big.pdf", "application/pdf")}
    )

    assert response.status_code == 413
    assert response.json == {"success": False, "message": "File is too large"}
