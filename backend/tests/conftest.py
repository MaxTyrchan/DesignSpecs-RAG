import pytest
import tempfile
import shutil
from pathlib import Path
from fastapi.testclient import TestClient
import chromadb
from chromadb.config import Settings
from fastapi import FastAPI
import os
from langchain_openai import AzureOpenAIEmbeddings
from services.helpers.embedding import Embedding
from services.helpers.chunking import Chunker
from services.document_processor import DocumentProcessor
from main import app
from docling_core.transforms.chunker.tokenizer.openai import OpenAITokenizer
import tiktoken

from api.qa import router as qa_router
from api.upload import router as upload_router
from api.evaluation import router as evaluation_router


@pytest.fixture(scope="session")
def app():
    """Create a FastAPI test application"""
    app = FastAPI()
    app.include_router(upload_router, prefix="/api")
    app.include_router(qa_router, prefix="/api")
    app.include_router(evaluation_router, prefix="/api")

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
    """Use the MTS2916A.pdf file from test assets for testing"""
    pdf_path = Path("tests/test_assets/MTS2916A.pdf")
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


@pytest.fixture
def test_pdf_path():
    """Get the path to the test PDF file"""
    test_assets_dir = Path("tests/test_assets")
    test_assets_dir.mkdir(parents=True, exist_ok=True)
    return test_assets_dir / "MTS2916A.pdf"


@pytest.fixture
def mock_azure_embeddings():
    """Create a mock AzureOpenAIEmbeddings instance"""
    class MockAzureEmbeddings:
        def embed_documents(self, texts: list[str]) -> list[list[float]]:
            # Return mock embeddings of dimension 1536 (same as text-embedding-3-large)
            return [[0.1] * 1536 for _ in texts]

        def embed_query(self, text: str) -> list[float]:
            return [0.1] * 1536

    return MockAzureEmbeddings()


@pytest.fixture
def mock_embeddings(mock_azure_embeddings):
    """Create a mock Embedding instance"""
    return Embedding(mock_azure_embeddings, name="mock_embeddings")


@pytest.fixture
def tokenizer():
    """Create an OpenAI tokenizer instance"""
    return OpenAITokenizer(
        tokenizer=tiktoken.encoding_for_model("gpt-4"),
        max_tokens=128 * 1024,
    )


@pytest.fixture
def chunker(tokenizer):
    """Create a Chunker instance"""
    return Chunker(tokenizer)


@pytest.fixture
def document_processor():
    """Create a DocumentProcessor instance"""
    processor = DocumentProcessor()
    processor.assets_dir = Path("tests/test_assets")
    return processor
