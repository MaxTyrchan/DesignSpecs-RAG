"""
Test configuration and fixtures for the RAG application.
"""

from services.document_processor import DocumentProcessor
from services.qa_service import QAService
from main import app
import pytest
import os
import tempfile
import shutil
from pathlib import Path
from typing import Generator
from unittest.mock import Mock, AsyncMock
from fastapi.testclient import TestClient

# Set test environment variables before importing the app
os.environ["TESTING"] = "true"
os.environ["CHROMA_DB_PATH"] = tempfile.mkdtemp()


@pytest.fixture(scope="session")
def test_client():
    """Create a test client for the FastAPI app."""
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def mock_qa_service():
    """Create a mock QA service for testing."""
    mock_service = Mock(spec=QAService)
    mock_service.answer_question = AsyncMock()
    mock_service.set_retriever = Mock()
    mock_service.set_llm = Mock()
    mock_service.set_reranker = Mock()
    return mock_service


@pytest.fixture
def mock_document_processor():
    """Create a mock document processor for testing."""
    mock_processor = Mock(spec=DocumentProcessor)
    mock_processor.process_pdf = AsyncMock()
    mock_processor.create_vector_store = Mock()
    return mock_processor


@pytest.fixture
def sample_pdf_path(temp_dir):
    """Create a sample PDF file for testing."""
    pdf_path = temp_dir / "sample.pdf"
    # Create a minimal PDF file content (this is a simplified example)
    with open(pdf_path, "wb") as f:
        f.write(b"%PDF-1.4\n%EOF")
    return pdf_path


@pytest.fixture
def sample_question():
    """Sample question for testing QA functionality."""
    return "What is the operating voltage of the device?"


@pytest.fixture
def sample_qa_response():
    """Sample QA response for testing."""
    return {
        "answer": "The operating voltage is 5V DC.",
        "context": {
            "images": [],
            "tables": [{"content": "Voltage: 5V\nCurrent: 1A", "metadata": {"page": 1}}],
            "texts": [{"content": "Device specifications include 5V operating voltage.", "metadata": {"page": 1}}]
        }
    }


@pytest.fixture(autouse=True)
def cleanup_env():
    """Clean up environment after each test."""
    yield
    # Clean up any test artifacts
    test_db_path = os.environ.get("CHROMA_DB_PATH")
    if test_db_path and os.path.exists(test_db_path):
        shutil.rmtree(test_db_path, ignore_errors=True)
