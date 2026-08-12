import pytest
import json
import uuid
from unittest.mock import Mock, MagicMock, patch
from langchain.schema.document import Document
from langchain.retrievers.multi_vector import MultiVectorRetriever
from services.helpers.embedding import Embedding


class TestEmbedding:
    """Test suite for embedding functionality."""

    @pytest.fixture
    def mock_embedding_model(self):
        """Create a mock embedding model."""
        model = Mock()
        model.embed_query.return_value = [0.1, 0.2, 0.3]
        model.embed_documents.return_value = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        return model

    @pytest.fixture
    def embedding_instance(self, mock_embedding_model):
        """Create an Embedding instance with mock model."""
        return Embedding(mock_embedding_model)

    @pytest.fixture
    def mock_retriever(self):
        """Create a mock MultiVectorRetriever."""
        retriever = Mock(spec=MultiVectorRetriever)
        retriever.id_key = "doc_id"
        retriever.vectorstore = Mock()
        retriever.docstore = Mock()
        retriever.vectorstore.add_documents = Mock()
        retriever.docstore.mset = Mock()
        return retriever

    @pytest.fixture
    def sample_partitioned_data(self):
        """Create sample partitioned data for testing."""
        # Create mock chunks for texts
        chunk1 = Mock()
        chunk1.text = "First text chunk"
        chunk1.export_json_dict.return_value = {
            "text": "First text chunk", "metadata": {}}

        chunk2 = Mock()
        chunk2.text = "Second text chunk"
        chunk2.export_json_dict.return_value = {
            "text": "Second text chunk", "metadata": {}}

        # Create mock chunks for tables
        table1 = Mock()
        table1.export_json_dict.return_value = {
            "text": "| Col1 | Col2 |\n|------|------|\n| A    | B    |", "label": "table"}

        table2 = Mock()
        table2.export_json_dict.return_value = {
            "text": "| X | Y |\n|---|---|\n| 1 | 2 |", "label": "table"}

        return {
            "texts": [chunk1, chunk2],
            "texts_summaries": ["Summary of first text", "Summary of second text"],
            "tables": [table1, table2],
            "tables_summaries": ["Table 1 summary", "Table 2 summary"],
            "images": ["base64image1", "base64image2"],
            "images_summaries": ["Image 1 description", "Image 2 description"]
        }

    def test_embedding_initialization(self, mock_embedding_model):
        """Test Embedding class initialization."""
        embedding = Embedding(mock_embedding_model)

        assert embedding.embeddings == mock_embedding_model
        assert embedding.text_item == "text_item"

    def test_call_method(self, embedding_instance, mock_embedding_model):
        """Test the __call__ method delegates to embed_documents."""
        input_texts = ["text1", "text2"]
        expected_embeddings = [[0.1, 0.2], [0.3, 0.4]]
        mock_embedding_model.embed_documents.return_value = expected_embeddings

        result = embedding_instance(input_texts)

        assert result == expected_embeddings
        mock_embedding_model.embed_documents.assert_called_once_with(
            input_texts)

    def test_name_method(self, embedding_instance):
        """Test the name method returns correct name."""
        result = embedding_instance.name()
        assert result == "AzureOpenAIEmbeddings"

    def test_embed_query(self, embedding_instance, mock_embedding_model):
        """Test embed_query method."""
        query = "test query"
        expected_embedding = [0.1, 0.2, 0.3]
        mock_embedding_model.embed_query.return_value = expected_embedding

        result = embedding_instance.embed_query(query)

        assert result == expected_embedding
        mock_embedding_model.embed_query.assert_called_once_with(query)

    def test_embed_documents(self, embedding_instance, mock_embedding_model):
        """Test embed_documents method."""
        texts = ["doc1", "doc2"]
        expected_embeddings = [[0.1, 0.2], [0.3, 0.4]]
        mock_embedding_model.embed_documents.return_value = expected_embeddings

        result = embedding_instance.embed_documents(texts)

        assert result == expected_embeddings
        mock_embedding_model.embed_documents.assert_called_once_with(texts)

    @patch('uuid.uuid4')
    def test_embed_pdf_texts_only(self, mock_uuid, embedding_instance, mock_retriever):
        """Test embed_pdf with only text content."""
        # Setup UUIDs
        mock_uuid.side_effect = [
            Mock(return_value="text-uuid-1"),
            Mock(return_value="text-uuid-2")
        ]
        mock_uuid.return_value.__str__ = lambda x: f"uuid-{id(x)}"

        # Create chunks
        chunk1 = Mock()
        chunk1.text = "Text 1"
        chunk1.export_json_dict.return_value = {"text": "Text 1"}

        chunk2 = Mock()
        chunk2.text = "Text 2"
        chunk2.export_json_dict.return_value = {"text": "Text 2"}

        partitioned_data = {
            "texts": [chunk1, chunk2],
            "texts_summaries": ["Summary 1", "Summary 2"],
            "tables": [],
            "tables_summaries": [],
            "images": [],
            "images_summaries": []
        }

        embedding_instance.embed_pdf(partitioned_data, mock_retriever)

        # embed_pdf always calls add_documents 3 times (texts, tables, images) even if empty
        assert mock_retriever.vectorstore.add_documents.call_count == 3
        assert mock_retriever.docstore.mset.call_count == 3

        # Check that only the first call (texts) has documents
        calls = mock_retriever.vectorstore.add_documents.call_args_list
        text_docs = calls[0][0][0]  # First call, first argument
        table_docs = calls[1][0][0]  # Second call, first argument
        image_docs = calls[2][0][0]  # Third call, first argument

        assert len(text_docs) == 2
        assert len(table_docs) == 0
        assert len(image_docs) == 0
        assert text_docs[0].page_content == "Summary 1"
        assert text_docs[1].page_content == "Summary 2"

    @patch('uuid.uuid4')
    def test_embed_pdf_tables_only(self, mock_uuid, embedding_instance, mock_retriever):
        """Test embed_pdf with only table content."""
        # Setup UUIDs
        mock_uuid.side_effect = [
            Mock(return_value=f"table-uuid-{i}") for i in range(2)]

        # Create mock table objects with export_json_dict method
        table1 = Mock()
        table1.export_json_dict.return_value = {
            "text": "Table 1 content", "label": "table"}
        table2 = Mock()
        table2.export_json_dict.return_value = {
            "text": "Table 2 content", "label": "table"}

        partitioned_data = {
            "texts": [],
            "texts_summaries": [],
            "tables": [table1, table2],
            "tables_summaries": ["Table summary 1", "Table summary 2"],
            "images": [],
            "images_summaries": []
        }

        embedding_instance.embed_pdf(partitioned_data, mock_retriever)

        # embed_pdf always calls add_documents 3 times (texts, tables, images) even if empty
        assert mock_retriever.vectorstore.add_documents.call_count == 3
        assert mock_retriever.docstore.mset.call_count == 3

        # Check that only the second call (tables) has documents
        calls = mock_retriever.vectorstore.add_documents.call_args_list
        text_docs = calls[0][0][0]  # First call
        table_docs = calls[1][0][0]  # Second call
        image_docs = calls[2][0][0]  # Third call

        assert len(text_docs) == 0
        assert len(table_docs) == 2
        assert len(image_docs) == 0

    @patch('uuid.uuid4')
    def test_embed_pdf_images_only(self, mock_uuid, embedding_instance, mock_retriever):
        """Test embed_pdf with only image content."""
        # Setup UUIDs
        mock_uuid.side_effect = [
            Mock(return_value=f"image-uuid-{i}") for i in range(2)]

        partitioned_data = {
            "texts": [],
            "texts_summaries": [],
            "tables": [],
            "tables_summaries": [],
            "images": ["image1", "image2"],
            "images_summaries": ["Image desc 1", "Image desc 2"]
        }

        embedding_instance.embed_pdf(partitioned_data, mock_retriever)

        # embed_pdf always calls add_documents 3 times (texts, tables, images) even if empty
        assert mock_retriever.vectorstore.add_documents.call_count == 3
        assert mock_retriever.docstore.mset.call_count == 3

        # Check that only the third call (images) has documents
        calls = mock_retriever.vectorstore.add_documents.call_args_list
        text_docs = calls[0][0][0]  # First call
        table_docs = calls[1][0][0]  # Second call
        image_docs = calls[2][0][0]  # Third call

        assert len(text_docs) == 0
        assert len(table_docs) == 0
        assert len(image_docs) == 2

    @patch('uuid.uuid4')
    def test_embed_pdf_mixed_content(self, mock_uuid, embedding_instance, mock_retriever, sample_partitioned_data):
        """Test embed_pdf with mixed content types."""
        # Setup UUIDs for all content types
        # 2 texts + 2 tables + 2 images
        uuid_values = [f"uuid-{i}" for i in range(6)]
        mock_uuid.side_effect = [Mock(return_value=uid) for uid in uuid_values]

        embedding_instance.embed_pdf(sample_partitioned_data, mock_retriever)

        # Should call add_documents and mset for each content type
        assert mock_retriever.vectorstore.add_documents.call_count == 3  # texts, tables, images
        assert mock_retriever.docstore.mset.call_count == 3

    def test_embed_pdf_exception_handling(self, embedding_instance, mock_retriever):
        """Test embed_pdf exception handling."""
        # Make vectorstore raise exception
        mock_retriever.vectorstore.add_documents.side_effect = Exception(
            "Vectorstore error")

        # Create proper mock chunk with export_json_dict method
        chunk = Mock()
        chunk.export_json_dict.return_value = {"text": "Test text"}

        partitioned_data = {
            "texts": [chunk],
            "texts_summaries": ["Summary"],
            "tables": [],
            "tables_summaries": [],
            "images": [],
            "images_summaries": []
        }

        with pytest.raises(Exception, match="Error embedding document: Vectorstore error"):
            embedding_instance.embed_pdf(partitioned_data, mock_retriever)

    @patch('uuid.uuid4')
    def test_embed_pdf_text_metadata_structure(self, mock_uuid, embedding_instance, mock_retriever):
        """Test that text documents have correct metadata structure."""
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="test-uuid")

        chunk = Mock()
        chunk.text = "Test text"
        chunk.export_json_dict.return_value = {
            "text": "Test text", "metadata": {}}

        partitioned_data = {
            "texts": [chunk],
            "texts_summaries": ["Test summary"],
            "tables": [],
            "tables_summaries": [],
            "images": [],
            "images_summaries": []
        }

        embedding_instance.embed_pdf(partitioned_data, mock_retriever)

        # Check metadata structure for text documents (first call)
        calls = mock_retriever.vectorstore.add_documents.call_args_list
        text_docs = calls[0][0][0]  # First call - texts

        assert len(text_docs) == 1
        text_doc = text_docs[0]

        assert text_doc.metadata["content_type"] == "text"
        assert mock_retriever.id_key in text_doc.metadata
        # text_item was removed from metadata, only content_type and id_key remain

    @patch('uuid.uuid4')
    def test_embed_pdf_table_metadata_structure(self, mock_uuid, embedding_instance, mock_retriever):
        """Test that table documents have correct metadata structure."""
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="test-uuid")

        # Create mock table object with export_json_dict method
        table = Mock()
        table.export_json_dict.return_value = {
            "text": "| A | B |\n|---|---|\n| 1 | 2 |", "label": "table"}

        partitioned_data = {
            "texts": [],
            "texts_summaries": [],
            "tables": [table],
            "tables_summaries": ["Table summary"],
            "images": [],
            "images_summaries": []
        }

        embedding_instance.embed_pdf(partitioned_data, mock_retriever)

        # Check metadata structure for table documents (second call)
        calls = mock_retriever.vectorstore.add_documents.call_args_list
        table_docs = calls[1][0][0]  # Second call - tables

        assert len(table_docs) == 1
        table_doc = table_docs[0]

        assert table_doc.metadata["content_type"] == "table"
        assert mock_retriever.id_key in table_doc.metadata
        # table_content was removed from metadata, only content_type and id_key remain

    @patch('uuid.uuid4')
    def test_embed_pdf_image_metadata_structure(self, mock_uuid, embedding_instance, mock_retriever):
        """Test that image documents have correct metadata structure."""
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="test-uuid")

        partitioned_data = {
            "texts": [],
            "texts_summaries": [],
            "tables": [],
            "tables_summaries": [],
            "images": ["base64image"],
            "images_summaries": ["Image description"]
        }

        embedding_instance.embed_pdf(partitioned_data, mock_retriever)

        # Check metadata structure for image documents
        vectorstore_call = mock_retriever.vectorstore.add_documents.call_args[0][0]
        image_doc = vectorstore_call[0]

        assert image_doc.metadata["content_type"] == "image"
        assert mock_retriever.id_key in image_doc.metadata

    @patch('uuid.uuid4')
    @patch('json.dumps')
    def test_embed_pdf_docstore_text_encoding(self, mock_json_dumps, mock_uuid, embedding_instance, mock_retriever):
        """Test that text chunks are properly JSON encoded for docstore."""
        mock_uuid.return_value = Mock()
        mock_uuid.return_value.__str__ = Mock(return_value="test-uuid")
        mock_json_dumps.return_value = '{"text": "encoded"}'

        chunk = Mock()
        chunk.text = "Test text"
        chunk.export_json_dict.return_value = {"text": "Test text"}

        partitioned_data = {
            "texts": [chunk],
            "texts_summaries": ["Summary"],
            "tables": [],
            "tables_summaries": [],
            "images": [],
            "images_summaries": []
        }

        embedding_instance.embed_pdf(partitioned_data, mock_retriever)

        # Verify JSON encoding was called
        mock_json_dumps.assert_called_once_with({"text": "Test text"})

        # Check docstore was called with encoded data (first call for texts)
        docstore_calls = mock_retriever.docstore.mset.call_args_list
        text_docstore_call = docstore_calls[0][0][0]  # First call - texts
        assert len(text_docstore_call) == 1
        assert text_docstore_call[0][1] == b'{"text": "encoded"}'
