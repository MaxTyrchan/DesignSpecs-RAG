import pytest
import tempfile
import shutil
from pathlib import Path
from fastapi.testclient import TestClient
import chromadb
from chromadb.config import Settings
from fastapi import FastAPI

from api.qa import router as qa_router
from api.upload import router as upload_router
from services.document_processor import DocumentProcessor


@pytest.fixture(scope="session")
def app():
    """Create a FastAPI test application"""
    app = FastAPI()
    app.include_router(upload_router, prefix="/api")
    app.include_router(qa_router, prefix="/api")

    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    return app


@pytest.fixture(scope="session")
def test_db_path():
    """Create a temporary directory for test database"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture(scope="function")
def test_chroma_client(test_db_path):
    """Create a test ChromaDB client"""
    client = chromadb.Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=test_db_path
    ))
    yield client
    # Clean up collections after each test
    for collection in client.list_collections():
        client.delete_collection(collection.name)


@pytest.fixture(scope="function")
def test_client(app):
    """Create a FastAPI TestClient"""
    return TestClient(app)


@pytest.fixture(scope="function")
def test_pdf_file():
    """Use the existing MTS2916A.pdf file for testing"""
    pdf_path = Path("./assets/MTS2916A.pdf")
    if not pdf_path.exists():
        raise FileNotFoundError(f"Test PDF file not found at {pdf_path}")
    return str(pdf_path.absolute())


@pytest.fixture(scope="function")
def test_assets_dir():
    """Create a temporary assets directory"""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture(scope="function")
def test_document_processor(test_assets_dir):
    """Create a DocumentProcessor instance with test configuration"""
    processor = DocumentProcessor()
    processor.assets_dir = test_assets_dir
    return processor
