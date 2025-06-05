import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import os


def test_health_check(test_client):
    """Test the health check endpoint."""
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_upload_valid_pdf(test_client, test_pdf_file):
    """Test uploading a valid PDF file"""
    with open(test_pdf_file, "rb") as f:
        files = {"file": ("test.pdf", f, "application/pdf")}
        response = test_client.post("/api/upload", files=files)

    assert response.status_code == 200
    assert "message" in response.json()
    assert "filename" in response.json()
    assert response.json()["filename"] == "test.pdf"


def test_upload_invalid_file_type(test_client):
    """Test uploading a file with invalid type."""
    # Create a text file
    content = b"This is not a PDF"
    files = {"file": ("test.txt", content, "text/plain")}

    response = test_client.post("/api/upload", files=files)
    assert response.status_code == 400
    assert "Only PDF files are allowed" in response.json()["detail"]


def test_upload_empty_file(test_client):
    """Test uploading an empty file."""
    files = {"file": ("test.pdf", b"", "application/pdf")}

    response = test_client.post("/api/upload", files=files)
    assert response.status_code == 400  # Changed from 500 to 400
    assert "Empty file" in response.json()["detail"]


def test_upload_large_file(test_client):
    """Test uploading a file that's too large."""
    # Create a large file (e.g., 11MB)
    content = b"0" * (11 * 1024 * 1024)  # 11MB
    files = {"file": ("large.pdf", content, "application/pdf")}

    response = test_client.post("/api/upload", files=files)
    assert response.status_code == 400  # Changed from 413 to 400
    assert "File too large" in response.json()["detail"]


def test_qa_endpoint_no_question(test_client):
    """Test QA endpoint without a question."""
    response = test_client.post(
        "/api/qa/ask", json={})  # Updated endpoint path
    assert response.status_code == 422  # Unprocessable Entity


def test_qa_endpoint_empty_question(test_client):
    """Test QA endpoint with empty question."""
    response = test_client.post(
        "/api/qa/ask", json={"question": ""})  # Updated endpoint path
    assert response.status_code == 400
    assert "Question cannot be empty" in response.json()["detail"]


def test_qa_endpoint_with_question(test_client):
    """Test QA endpoint with a valid question."""
    response = test_client.post(
        # Updated endpoint path
        "/api/qa/ask", json={"question": "What is this document about?"})
    assert response.status_code == 200
    assert "answer" in response.json()
    assert "sources" in response.json()


def test_cors_headers(test_client):
    """Test that CORS headers are properly set."""
    response = test_client.options("/api/upload")
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "*"


@pytest.mark.asyncio
async def test_ask_question(test_client):
    """Test the question answering endpoint."""
    response = test_client.post(
        "/api/qa/ask",
        json={"question": "What is this document about?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data


def test_ask_question_error_handling(test_client, monkeypatch):
    """Test error handling in the question answering endpoint."""
    async def mock_answer_question(*args, **kwargs):
        raise Exception("Test error")

    # Mock the answer_question method to raise an exception
    monkeypatch.setattr(
        "services.qa_service.QAService.answer_question", mock_answer_question)

    response = test_client.post(
        "/api/qa/ask", json={"question": "test"})  # Updated endpoint path
    assert response.status_code == 500
    assert "error" in response.json()["detail"].lower()


def test_evaluation_endpoint(test_client):
    """Test the evaluation data endpoint."""
    response = test_client.get("/api/evaluation")
    assert response.status_code == 200
    data = response.json()
    assert "metrics" in data
    assert "pairs" in data
