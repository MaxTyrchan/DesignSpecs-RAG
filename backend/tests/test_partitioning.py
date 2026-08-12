import pytest
import base64
from unittest.mock import Mock, MagicMock, patch
from docling_core.types.doc.document import DoclingDocument
from docling_core.types.doc.labels import DocItemLabel
from services.helpers.partitioning import partitioning
from services.helpers.chunking import Chunker


class TestPartitioning:
    """Test suite for document partitioning functionality."""

    @pytest.fixture
    def mock_chunker(self):
        """Create a mock chunker for testing."""
        chunker = Mock(spec=Chunker)
        chunker.hybrid_chunker = Mock()
        chunker.hybrid_chunker.contextualize = Mock(
            return_value="Contextualized text")
        return chunker

    @pytest.fixture
    def mock_doc(self):
        """Create a mock DoclingDocument for testing."""
        doc = Mock(spec=DoclingDocument)
        doc.tables = []
        doc.pictures = []
        return doc

    @pytest.fixture
    def mock_chunk(self):
        """Create a mock chunk with metadata."""
        chunk = Mock()
        chunk.text = "Sample chunk text"
        chunk.meta = Mock()
        chunk.meta.doc_items = []
        return chunk

    def test_partitioning_empty_document(self, mock_doc, mock_chunker):
        """Test partitioning with an empty document raises ValueError."""
        # Setup empty document
        mock_chunker.chunking.return_value = []

        # Should raise ValueError for empty content
        with pytest.raises(ValueError, match="No content was extracted from the document"):
            partitioning(mock_doc, mock_chunker)

    def test_partitioning_with_text_chunks(self, mock_doc, mock_chunker):
        """Test partitioning document with text chunks."""
        # Setup text chunk
        chunk = Mock()
        chunk.text = "Sample text content"
        chunk.meta = Mock()

        # Create mock doc item with TEXT label
        doc_item = Mock()
        doc_item.label = DocItemLabel.TEXT
        chunk.meta.doc_items = [doc_item]

        mock_chunker.chunking.return_value = [chunk]
        mock_chunker.hybrid_chunker.contextualize.return_value = "Contextualized text"

        result = partitioning(mock_doc, mock_chunker)

        assert len(result["texts"]) == 1
        assert len(result["texts_summaries"]) == 1
        assert result["texts"][0] == chunk
        assert result["texts_summaries"][0] == "Contextualized text"
        assert len(result["tables"]) == 0
        assert len(result["images"]) == 0

    def test_partitioning_with_table_chunks(self, mock_doc, mock_chunker):
        """Test partitioning document with table chunks."""
        # Setup table chunk
        chunk = Mock()
        chunk.text = "Table content"
        chunk.meta = Mock()

        # Create mock doc item with TABLE label
        doc_item = Mock()
        doc_item.label = DocItemLabel.TABLE
        chunk.meta.doc_items = [doc_item]

        mock_chunker.chunking.return_value = [chunk]
        mock_chunker.hybrid_chunker.contextualize.return_value = "Table summary"

        result = partitioning(mock_doc, mock_chunker)

        assert len(result["tables_summaries"]) == 1
        assert result["tables_summaries"][0] == "Table summary"
        assert len(result["texts"]) == 0

    def test_partitioning_with_picture_chunks(self, mock_doc, mock_chunker):
        """Test partitioning document with picture chunks."""
        # Setup picture chunk
        chunk = Mock()
        chunk.text = "Picture content"
        chunk.meta = Mock()

        # Create mock doc item with PICTURE label
        doc_item = Mock()
        doc_item.label = DocItemLabel.PICTURE
        chunk.meta.doc_items = [doc_item]

        mock_chunker.chunking.return_value = [chunk]

        # Picture chunks break early, so should raise ValueError for empty content
        with pytest.raises(ValueError, match="No content was extracted from the document"):
            partitioning(mock_doc, mock_chunker)

    def test_partitioning_with_tables(self, mock_doc, mock_chunker):
        """Test partitioning document with table extraction."""
        # Setup chunk with table item
        chunk = Mock()
        chunk.text = "| Column 1 | Column 2 |\n|----------|----------|\n| Data 1   | Data 2   |"
        chunk.meta = Mock()

        # Create a doc_item with TABLE label
        table_doc_item = Mock()
        table_doc_item.label = DocItemLabel.TABLE
        chunk.meta.doc_items = [table_doc_item]

        mock_chunker.chunking.return_value = [chunk]
        mock_chunker.hybrid_chunker.contextualize.return_value = "Table summary"

        result = partitioning(mock_doc, mock_chunker)

        assert len(result["tables"]) == 1
        assert "Column 1" in result["tables"][0].text
        assert len(result["tables_summaries"]) == 1
        assert result["tables_summaries"][0] == "Table summary"

    def test_partitioning_with_images_with_descriptions(self, mock_doc, mock_chunker):
        """Test partitioning document with images that have descriptions."""
        # Setup image with description
        picture = Mock()
        mock_image = Mock()
        picture.get_image.return_value = mock_image

        # Mock annotation with description
        annotation = Mock()
        annotation.kind = "description"
        annotation.text = "Image description"
        picture.annotations = [annotation]

        # Mock base64 encoding
        picture._image_to_base64.return_value = "base64encodedimage"

        mock_doc.pictures = [picture]

        # Setup minimal chunk to avoid empty content error
        chunk = Mock()
        chunk.text = "Sample text"
        chunk.meta = Mock()
        doc_item = Mock()
        doc_item.label = DocItemLabel.TEXT
        chunk.meta.doc_items = [doc_item]
        mock_chunker.chunking.return_value = [chunk]

        with patch('base64.b64decode', return_value=b'decoded_image_data'):
            result = partitioning(mock_doc, mock_chunker)

        assert len(result["images"]) == 1
        assert len(result["images_summaries"]) == 1
        assert result["images"][0] == "base64encodedimage"
        assert result["images_summaries"][0] == "Image description"

    def test_partitioning_with_images_without_descriptions(self, mock_doc, mock_chunker):
        """Test partitioning document with images without descriptions."""
        # Setup image without description
        picture = Mock()
        mock_image = Mock()
        picture.get_image.return_value = mock_image
        picture.annotations = []  # No annotations

        mock_doc.pictures = [picture]

        # Setup minimal chunk to avoid empty content error
        chunk = Mock()
        chunk.text = "Sample text"
        chunk.meta = Mock()
        doc_item = Mock()
        doc_item.label = DocItemLabel.TEXT
        chunk.meta.doc_items = [doc_item]
        mock_chunker.chunking.return_value = [chunk]

        result = partitioning(mock_doc, mock_chunker)

        # Images without descriptions should not be added
        assert len(result["images"]) == 0
        assert len(result["images_summaries"]) == 0

    def test_partitioning_chunking_error_handling(self, mock_doc, mock_chunker):
        """Test error handling during chunking process."""
        # Make chunking raise an exception
        mock_chunker.chunking.side_effect = Exception("Chunking failed")

        # Should still try to extract tables and images, but raise ValueError for empty content
        with pytest.raises(ValueError, match="No content was extracted from the document"):
            partitioning(mock_doc, mock_chunker)

    def test_partitioning_table_extraction_error_handling(self, mock_doc, mock_chunker):
        """Test error handling during table extraction."""
        # Setup table that will raise exception
        table = Mock()
        table.export_to_markdown.side_effect = Exception("Table export failed")
        mock_doc.tables = [table]

        # Setup minimal chunk to avoid empty content error
        chunk = Mock()
        chunk.text = "Sample text"
        chunk.meta = Mock()
        doc_item = Mock()
        doc_item.label = DocItemLabel.TEXT
        chunk.meta.doc_items = [doc_item]
        mock_chunker.chunking.return_value = [chunk]

        # Should not raise exception, just skip failed table
        result = partitioning(mock_doc, mock_chunker)
        assert len(result["tables"]) == 0

    def test_partitioning_image_extraction_error_handling(self, mock_doc, mock_chunker):
        """Test error handling during image extraction."""
        # Setup image that will raise exception
        picture = Mock()
        picture.get_image.side_effect = Exception("Image extraction failed")
        mock_doc.pictures = [picture]

        # Setup minimal chunk to avoid empty content error
        chunk = Mock()
        chunk.text = "Sample text"
        chunk.meta = Mock()
        doc_item = Mock()
        doc_item.label = DocItemLabel.TEXT
        chunk.meta.doc_items = [doc_item]
        mock_chunker.chunking.return_value = [chunk]

        # Should not raise exception, just skip failed image
        result = partitioning(mock_doc, mock_chunker)
        assert len(result["images"]) == 0

    def test_partitioning_base64_decode_error_handling(self, mock_doc, mock_chunker):
        """Test error handling during base64 decoding."""
        # Setup image with description but invalid base64
        picture = Mock()
        mock_image = Mock()
        picture.get_image.return_value = mock_image

        annotation = Mock()
        annotation.kind = "description"
        annotation.text = "Image description"
        picture.annotations = [annotation]

        picture._image_to_base64.return_value = "invalid_base64"
        mock_doc.pictures = [picture]

        # Setup minimal chunk to avoid empty content error
        chunk = Mock()
        chunk.text = "Sample text"
        chunk.meta = Mock()
        doc_item = Mock()
        doc_item.label = DocItemLabel.TEXT
        chunk.meta.doc_items = [doc_item]
        mock_chunker.chunking.return_value = [chunk]

        with patch('base64.b64decode', side_effect=Exception("Invalid base64")):
            result = partitioning(mock_doc, mock_chunker)

        # Should not add image due to decode error, but should still add description
        assert len(result["images"]) == 0
        assert len(result["images_summaries"]) == 1
        assert result["images_summaries"][0] == "Image description"

    def test_partitioning_mixed_content_types(self, mock_doc, mock_chunker):
        """Test partitioning document with mixed content types."""
        # Setup mixed chunks
        text_chunk = Mock()
        text_chunk.text = "Text content"
        text_chunk.meta = Mock()
        text_doc_item = Mock()
        text_doc_item.label = DocItemLabel.TEXT
        text_chunk.meta.doc_items = [text_doc_item]

        table_chunk = Mock()
        table_chunk.text = "Table content"
        table_chunk.meta = Mock()
        table_doc_item = Mock()
        table_doc_item.label = DocItemLabel.TABLE
        table_chunk.meta.doc_items = [table_doc_item]

        mock_chunker.chunking.return_value = [text_chunk, table_chunk]
        mock_chunker.hybrid_chunker.contextualize.side_effect = [
            "Text summary", "Table summary"]

        # Setup table
        table = Mock()
        table.export_to_markdown.return_value = "| Data |"
        mock_doc.tables = [table]

        result = partitioning(mock_doc, mock_chunker)

        assert len(result["texts"]) == 1
        assert len(result["texts_summaries"]) == 1
        assert len(result["tables_summaries"]) == 1
        assert len(result["tables"]) == 1
        assert result["texts"][0] == text_chunk
        assert result["texts_summaries"][0] == "Text summary"
        assert result["tables_summaries"][0] == "Table summary"
