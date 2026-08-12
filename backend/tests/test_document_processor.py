"""
Unit tests for the document processor service.
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch
from services.document_processor import DocumentProcessor


class TestDocumentProcessor:
    """Test suite for document processor functionality."""

    def test_document_processor_initialization(self):
        """Test document processor initialization."""
        processor = DocumentProcessor()
        assert processor is not None

    def test_process_pdf_file_not_found(self):
        """Test processing non-existent PDF file."""
        processor = DocumentProcessor()

        # Create mock embeddings, chunker, and retriever
        mock_embeddings = Mock()
        mock_chunker = Mock()
        mock_retriever = Mock()

        with pytest.raises(Exception):
            processor.process_pdf("non_existent_file.pdf",
                                  mock_embeddings, mock_chunker, mock_retriever)

    def test_process_pdf_invalid_file(self, temp_dir):
        """Test processing invalid PDF file."""
        processor = DocumentProcessor()

        # Create an invalid PDF file
        invalid_pdf = temp_dir / "invalid.pdf"
        with open(invalid_pdf, "w") as f:
            f.write("This is not a PDF")

        # Create mock embeddings, chunker, and retriever
        mock_embeddings = Mock()
        mock_chunker = Mock()
        mock_retriever = Mock()

        # Should handle the error gracefully
        with pytest.raises(Exception):
            processor.process_pdf(
                str(invalid_pdf), mock_embeddings, mock_chunker, mock_retriever)

    @patch('services.document_processor.partitioning')
    def test_process_pdf_success(self, mock_partitioning, temp_dir):
        """Test successful PDF processing."""
        processor = DocumentProcessor()

        # Create a mock PDF file
        pdf_file = temp_dir / "test.pdf"
        with open(pdf_file, "wb") as f:
            f.write(b"%PDF-1.4\n%EOF")

        # Create mock embeddings, chunker, and retriever
        mock_embeddings = Mock()
        mock_embeddings.embed_pdf = Mock()
        mock_chunker = Mock()
        mock_retriever = Mock()

        # Mock the document converter at the instance level
        mock_result = Mock()
        mock_result.document = Mock()
        processor.converter.convert = Mock(return_value=mock_result)

        # Mock the partitioning function
        mock_partitioning.return_value = {
            "texts": [], "tables": [], "images": []}

        # Should not raise an exception
        processor.process_pdf(str(pdf_file), mock_embeddings,
                              mock_chunker, mock_retriever)

        processor.converter.convert.assert_called_once_with(str(pdf_file))
        mock_partitioning.assert_called_once()
        mock_embeddings.embed_pdf.assert_called_once()

    def test_save_uploaded_file(self, temp_dir):
        """Test saving uploaded file."""
        processor = DocumentProcessor()
        # Override assets_dir for testing
        processor.assets_dir = temp_dir

        file_content = b"PDF content"
        filename = "test.pdf"

        result = processor.save_uploaded_file(file_content, filename)

        expected_path = temp_dir / "pdfs" / filename
        assert result == str(expected_path)
        assert expected_path.exists()
        assert expected_path.read_bytes() == file_content
