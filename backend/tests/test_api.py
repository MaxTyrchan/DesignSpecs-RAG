import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import os


def test_health_check(test_client):
    """Test the health check endpoint"""
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
    """Test uploading an invalid file type"""
    files = {"file": ("test.txt", b"test content", "text/plain")}
    response = test_client.post("/api/upload", files=files)

    assert response.status_code == 400
    assert "Only PDF files are allowed" in response.json()["detail"]


@pytest.mark.asyncio
async def test_ask_question(test_client):
    """Test the question answering endpoint"""
    question = "What is in the document?"
    response = test_client.post("/api/ask", json={"question": question})

    assert response.status_code == 200
    assert "answer" in response.json()
    assert "context" in response.json()


def test_ask_question_error_handling(test_client, monkeypatch):
    """Test error handling in the question answering endpoint"""
    async def mock_answer_question(*args, **kwargs):
        raise Exception("Test error")

    # Mock the answer_question method to raise an exception
    monkeypatch.setattr(
        "services.qa_service.QAService.answer_question", mock_answer_question)

    response = test_client.post("/api/ask", json={"question": "test"})
    assert response.status_code == 500
    assert "Test error" in response.json()["detail"]
