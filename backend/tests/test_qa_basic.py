"""
Simplified unit tests for the QA service.
"""

import pytest
from unittest.mock import Mock
from services.qa_service import QAService


class TestQAServiceBasic:
    """Basic test suite for QA service functionality."""

    def test_qa_service_initialization(self):
        """Test QA service initialization."""
        qa_service = QAService()
        assert qa_service.retriever is None
        assert qa_service.llm is None
        assert qa_service.reranker is None
        assert qa_service.tracer is not None

    def test_set_retriever(self):
        """Test setting retriever."""
        qa_service = QAService()
        mock_retriever = Mock()
        qa_service.set_retriever(mock_retriever)
        assert qa_service.retriever == mock_retriever

    def test_set_llm(self):
        """Test setting LLM."""
        qa_service = QAService()
        mock_llm = Mock()
        qa_service.set_llm(mock_llm)
        assert qa_service.llm == mock_llm

    def test_set_reranker(self):
        """Test setting reranker."""
        qa_service = QAService()
        mock_reranker = Mock()
        qa_service.set_reranker(mock_reranker)
        assert qa_service.reranker == mock_reranker

    def test_build_prompt_basic(self):
        """Test basic prompt building functionality."""
        context = {
            "texts": [{"content": "Test content", "metadata": {"page": 1}}],
            "tables": [],
            "images": []
        }

        kwargs = {"context": context, "question": "Test question?"}
        prompt = QAService.build_prompt(kwargs)

        assert prompt is not None
        assert len(prompt.messages) == 1
        # Check that our content appears in the prompt
        content_str = str(prompt.messages[0].content)
        assert "Test content" in content_str
        assert "Test question?" in content_str

    @pytest.mark.asyncio
    async def test_answer_question_error_handling(self):
        """Test error handling in answer_question when components are not set up."""
        qa_service = QAService()

        # Don't set up any dependencies - this should trigger error handling
        result = await qa_service.answer_question("Test question")

        # Should return error message
        assert "technical difficulties" in result["answer"]
        assert result["context"] == {"images": [], "tables": [], "texts": []}
