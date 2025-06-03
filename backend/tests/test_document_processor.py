import pytest
from pathlib import Path
import os
from services.document_processor import DocumentProcessor
from services.helpers.embedding import Embedding
from services.helpers.chunking import Chunker
from langchain.schema import Document


def test_document_processor_initialization():
    """Test that DocumentProcessor initializes correctly."""
    processor = DocumentProcessor()
    assert processor.pipeline_options.do_picture_description is True
    assert processor.pipeline_options.generate_picture_images is True
    assert processor.pipeline_options.images_scale == 2
    assert processor.pipeline_options.do_picture_classification is True
    assert isinstance(processor.assets_dir, Path)


def test_save_uploaded_file(document_processor, tmp_path):
    """Test saving an uploaded file."""
    # Override assets directory for testing
    document_processor.assets_dir = tmp_path

    # Create test file content
    test_content = b"Test PDF content"
    filename = "test.pdf"

    # Save the file
    file_path = document_processor.save_uploaded_file(test_content, filename)

    # Verify the file was saved correctly
    saved_file = Path(file_path)
    assert saved_file.exists()
    assert saved_file.read_bytes() == test_content


def test_save_uploaded_file_creates_directory(document_processor, tmp_path):
    """Test that save_uploaded_file creates the assets directory if it doesn't exist."""
    # Set a non-existent directory
    test_dir = tmp_path / "new_dir"
    document_processor.assets_dir = test_dir

    # Save a file
    test_content = b"Test PDF content"
    filename = "test.pdf"

    file_path = document_processor.save_uploaded_file(test_content, filename)

    # Verify directory was created
    assert test_dir.exists()
    assert test_dir.is_dir()


def test_process_pdf_with_invalid_file(document_processor, mock_embeddings, chunker, tmp_path):
    """Test that process_pdf handles invalid files appropriately."""
    # Create an invalid PDF file
    invalid_file = tmp_path / "invalid.pdf"
    invalid_file.write_bytes(b"Not a PDF file")

    class MockDocStore:
        def __init__(self):
            self.stored_items = {}

        def mset(self, items):
            for key, value in items:
                self.stored_items[key] = value

    class MockRetriever:
        id_key = "doc_id"

        def __init__(self):
            self.added_documents = []

        class MockVectorStore:
            def __init__(self):
                self.added_docs = []

            def add_documents(self, docs):
                self.added_docs.extend(docs)

        vectorstore = MockVectorStore()
        docstore = MockDocStore()

    with pytest.raises(Exception) as exc_info:
        document_processor.process_pdf(
            str(invalid_file),
            mock_embeddings,
            chunker,
            MockRetriever()
        )
    assert "Error converting document" in str(exc_info.value)


def test_process_pdf_file_not_found(document_processor, mock_embeddings, chunker):
    """Test that process_pdf handles non-existent files appropriately."""
    class MockDocStore:
        def __init__(self):
            self.stored_items = {}

        def mset(self, items):
            for key, value in items:
                self.stored_items[key] = value

    class MockRetriever:
        id_key = "doc_id"

        def __init__(self):
            self.added_documents = []

        class MockVectorStore:
            def __init__(self):
                self.added_docs = []

            def add_documents(self, docs):
                self.added_docs.extend(docs)

        vectorstore = MockVectorStore()
        docstore = MockDocStore()

    with pytest.raises(Exception) as exc_info:
        document_processor.process_pdf(
            "nonexistent.pdf",
            mock_embeddings,
            chunker,
            MockRetriever()
        )
    assert "Error converting document" in str(exc_info.value)


def test_process_pdf(document_processor, mock_embeddings, chunker, test_pdf_path):
    """Test processing a valid PDF file."""
    class MockDocStore:
        def __init__(self):
            self.stored_items = {}

        def mset(self, items):
            for key, value in items:
                self.stored_items[key] = value

    class MockRetriever:
        id_key = "doc_id"

        def __init__(self):
            self.added_documents = []

        class MockVectorStore:
            def __init__(self):
                self.added_docs = []

            def add_documents(self, docs):
                self.added_docs.extend(docs)

        vectorstore = MockVectorStore()
        docstore = MockDocStore()

    mock_retriever = MockRetriever()

    # Process the test PDF
    result = document_processor.process_pdf(
        str(test_pdf_path),
        mock_embeddings,
        chunker,
        mock_retriever
    )

    # Verify the result
    assert result is not None
    assert "texts" in result
    assert "texts_summaries" in result
    assert "tables" in result
    assert "tables_summaries" in result
    assert "images" in result
    assert "images_summaries" in result

    # Verify that text was extracted
    assert len(result["texts"]) > 0
    assert len(result["texts_summaries"]) > 0


def test_invalid_file_path(test_document_processor):
    """Test handling of invalid file path"""
    with pytest.raises(Exception):
        test_document_processor.process_pdf("nonexistent.pdf")


def test_assets_directory_creation(test_document_processor):
    """Test that assets directory is created if it doesn't exist"""
    # Delete the directory if it exists
    if test_document_processor.assets_dir.exists():
        test_document_processor.assets_dir.rmdir()

    # Try to save a file
    test_document_processor.save_uploaded_file(b"test content", "test.txt")

    assert test_document_processor.assets_dir.exists()
