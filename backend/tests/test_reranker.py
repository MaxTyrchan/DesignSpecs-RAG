import pytest
from unittest.mock import Mock, patch
from langchain.schema.document import Document
from services.helpers.reranker import Reranker


class TestReranker:
    """Test suite for document reranking functionality."""

    @pytest.fixture
    def sample_documents(self):
        """Create sample documents for testing."""
        return [
            Document(page_content="First document content",
                     metadata={"id": "1"}),
            Document(page_content="Second document content",
                     metadata={"id": "2"}),
            Document(page_content="Third document content",
                     metadata={"id": "3"}),
            Document(page_content="Fourth document content",
                     metadata={"id": "4"}),
        ]

    def test_reranker_initialization_default_model(self):
        """Test reranker initialization with default model."""
        with patch('services.helpers.reranker.FlashrankRerank') as mock_flashrank:
            reranker = Reranker()

            assert reranker.model == "rank-T5-flan"
            mock_flashrank.assert_called_once_with(model="rank-T5-flan")

    def test_reranker_initialization_custom_model(self):
        """Test reranker initialization with custom model."""
        custom_model = "custom-model"

        with patch('services.helpers.reranker.FlashrankRerank') as mock_flashrank:
            reranker = Reranker(model=custom_model)

            assert reranker.model == custom_model
            mock_flashrank.assert_called_once_with(model=custom_model)

    def test_rerank_documents_empty_list(self):
        """Test reranking with empty document list."""
        with patch('services.helpers.reranker.FlashrankRerank'):
            reranker = Reranker()
            result = reranker.rerank_documents("test query", [])

            assert result == []

    def test_rerank_documents_success(self, sample_documents):
        """Test successful document reranking."""
        with patch('services.helpers.reranker.FlashrankRerank') as mock_flashrank_class:
            # Setup mock compressor
            mock_compressor = Mock()
            reranked_docs = [sample_documents[2], sample_documents[0],
                             sample_documents[1], sample_documents[3]]
            mock_compressor.compress_documents.return_value = reranked_docs
            mock_flashrank_class.return_value = mock_compressor

            reranker = Reranker()
            result = reranker.rerank_documents("test query", sample_documents)

            assert len(result) == 4
            assert result == reranked_docs
            mock_compressor.compress_documents.assert_called_once_with(
                documents=sample_documents,
                query="test query"
            )

    def test_rerank_documents_with_top_n_limit(self, sample_documents):
        """Test document reranking with top_n limit."""
        with patch('services.helpers.reranker.FlashrankRerank') as mock_flashrank_class:
            # Setup mock compressor
            mock_compressor = Mock()
            reranked_docs = [sample_documents[2], sample_documents[0],
                             sample_documents[1], sample_documents[3]]
            mock_compressor.compress_documents.return_value = reranked_docs
            mock_flashrank_class.return_value = mock_compressor

            reranker = Reranker()
            result = reranker.rerank_documents(
                "test query", sample_documents, top_n=2)

            assert len(result) == 2
            assert result == reranked_docs[:2]
            mock_compressor.compress_documents.assert_called_once_with(
                documents=sample_documents,
                query="test query"
            )

    def test_rerank_documents_with_top_n_none(self, sample_documents):
        """Test document reranking with top_n as None."""
        with patch('services.helpers.reranker.FlashrankRerank') as mock_flashrank_class:
            # Setup mock compressor
            mock_compressor = Mock()
            reranked_docs = [sample_documents[1],
                             sample_documents[3]]  # Compressed result
            mock_compressor.compress_documents.return_value = reranked_docs
            mock_flashrank_class.return_value = mock_compressor

            reranker = Reranker()
            result = reranker.rerank_documents(
                "test query", sample_documents, top_n=None)

            assert len(result) == 2
            assert result == reranked_docs
            mock_compressor.compress_documents.assert_called_once_with(
                documents=sample_documents,
                query="test query"
            )

    def test_rerank_documents_exception_handling_with_top_n(self, sample_documents):
        """Test exception handling during reranking with top_n fallback."""
        with patch('services.helpers.reranker.FlashrankRerank') as mock_flashrank_class:
            # Setup mock compressor that raises exception
            mock_compressor = Mock()
            mock_compressor.compress_documents.side_effect = Exception(
                "Reranking failed")
            mock_flashrank_class.return_value = mock_compressor

            reranker = Reranker()
            result = reranker.rerank_documents(
                "test query", sample_documents, top_n=2)

            # Should fallback to original documents with top_n limit
            assert len(result) == 2
            assert result == sample_documents[:2]

    def test_rerank_documents_exception_handling_without_top_n(self, sample_documents):
        """Test exception handling during reranking without top_n fallback."""
        with patch('services.helpers.reranker.FlashrankRerank') as mock_flashrank_class:
            # Setup mock compressor that raises exception
            mock_compressor = Mock()
            mock_compressor.compress_documents.side_effect = Exception(
                "Reranking failed")
            mock_flashrank_class.return_value = mock_compressor

            reranker = Reranker()
            result = reranker.rerank_documents("test query", sample_documents)

            # Should fallback to all original documents
            assert len(result) == len(sample_documents)
            assert result == sample_documents

    def test_rerank_documents_logs_error_on_exception(self, sample_documents):
        """Test that errors are properly logged during exception handling."""
        with patch('services.helpers.reranker.FlashrankRerank') as mock_flashrank_class, \
                patch('services.helpers.reranker.logger') as mock_logger:

            # Setup mock compressor that raises exception
            mock_compressor = Mock()
            exception_msg = "Reranking service unavailable"
            mock_compressor.compress_documents.side_effect = Exception(
                exception_msg)
            mock_flashrank_class.return_value = mock_compressor

            reranker = Reranker()
            reranker.rerank_documents("test query", sample_documents)

            # Verify error was logged
            mock_logger.error.assert_called_once()
            logged_message = mock_logger.error.call_args[0][0]
            assert "Error during document reranking" in logged_message

    def test_rerank_documents_prints_success_message(self, sample_documents):
        """Test that success message is printed after reranking."""
        with patch('services.helpers.reranker.FlashrankRerank') as mock_flashrank_class, \
                patch('builtins.print') as mock_print:

            # Setup mock compressor
            mock_compressor = Mock()
            reranked_docs = [sample_documents[0],
                             sample_documents[2]]  # 2 docs returned
            mock_compressor.compress_documents.return_value = reranked_docs
            mock_flashrank_class.return_value = mock_compressor

            reranker = Reranker()
            reranker.rerank_documents("test query", sample_documents)

            # Verify success message was printed
            mock_print.assert_called_once()
            printed_message = mock_print.call_args[0][0]
            assert "Reranked 4 documents to top 2" in printed_message

    def test_rerank_documents_no_print_with_top_n(self, sample_documents):
        """Test that no print occurs when top_n is specified."""
        with patch('services.helpers.reranker.FlashrankRerank') as mock_flashrank_class, \
                patch('builtins.print') as mock_print:

            # Setup mock compressor
            mock_compressor = Mock()
            reranked_docs = [sample_documents[0],
                             sample_documents[2], sample_documents[1]]
            mock_compressor.compress_documents.return_value = reranked_docs
            mock_flashrank_class.return_value = mock_compressor

            reranker = Reranker()
            reranker.rerank_documents("test query", sample_documents, top_n=2)

            # Should not print when top_n is specified
            mock_print.assert_not_called()

    def test_rerank_documents_single_document(self):
        """Test reranking with a single document."""
        single_doc = [
            Document(page_content="Single document", metadata={"id": "1"})]

        with patch('services.helpers.reranker.FlashrankRerank') as mock_flashrank_class:
            # Setup mock compressor
            mock_compressor = Mock()
            mock_compressor.compress_documents.return_value = single_doc
            mock_flashrank_class.return_value = mock_compressor

            reranker = Reranker()
            result = reranker.rerank_documents("test query", single_doc)

            assert len(result) == 1
            assert result == single_doc
            mock_compressor.compress_documents.assert_called_once_with(
                documents=single_doc,
                query="test query"
            )

    def test_rerank_documents_with_zero_top_n(self, sample_documents):
        """Test reranking with top_n=0."""
        with patch('services.helpers.reranker.FlashrankRerank') as mock_flashrank_class:
            # Setup mock compressor
            mock_compressor = Mock()
            reranked_docs = [sample_documents[1], sample_documents[0]]
            mock_compressor.compress_documents.return_value = reranked_docs
            mock_flashrank_class.return_value = mock_compressor

            reranker = Reranker()
            result = reranker.rerank_documents(
                "test query", sample_documents, top_n=0)

            assert len(result) == 0
            assert result == []
            mock_compressor.compress_documents.assert_called_once_with(
                documents=sample_documents,
                query="test query"
            )
