import pytest
from pathlib import Path
import os
from services.document_processor import DocumentProcessor


def test_save_uploaded_file(test_document_processor, test_pdf_file):
    """Test saving an uploaded file"""
    with open(test_pdf_file, 'rb') as f:
        content = f.read()

    filename = "test.pdf"
    saved_path = test_document_processor.save_uploaded_file(content, filename)

    assert os.path.exists(saved_path)
    assert saved_path == str(test_document_processor.assets_dir / filename)


def test_process_pdf(test_document_processor, test_pdf_file):
    """Test PDF processing"""
    try:
        test_document_processor.process_pdf(test_pdf_file)
    except Exception as e:
        pytest.fail(f"PDF processing failed: {str(e)}")


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
