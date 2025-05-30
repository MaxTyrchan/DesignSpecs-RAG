import pytest
from services.qa_service import QAService
import base64


def test_parse_answer():
    """Test parsing of answers with both text and base64 images"""
    # Create test data
    text = "This is a test answer"
    image_data = base64.b64encode(b"fake image data").decode()
    answers = [text, image_data]

    result = QAService.parse_answer(answers)

    assert "texts" in result
    assert "images" in result
    assert len(result["texts"]) == 1
    assert len(result["images"]) == 1
    assert result["texts"][0] == text
    assert result["images"][0] == image_data


def test_build_prompt():
    """Test prompt building with different types of content"""
    context = {
        "texts": ["Test context"],
        "images": [base64.b64encode(b"fake image data").decode()]
    }
    question = "Test question?"

    prompt = QAService.build_prompt({
        "context": context,
        "question": question
    })

    assert isinstance(prompt.messages[0].content, list)
    assert len(prompt.messages[0].content) == 2  # Text + image
    assert "Test context" in prompt.messages[0].content[0]["text"]
    assert "Test question?" in prompt.messages[0].content[0]["text"]
    assert prompt.messages[0].content[1]["type"] == "image_url"


@pytest.mark.asyncio
async def test_answer_question(monkeypatch):
    """Test the question answering functionality"""
    # Mock the retriever and llm responses
    async def mock_retriever(question):
        return ["Test context"]

    async def mock_llm(prompt):
        return "Test answer"

    qa_service = QAService()
    monkeypatch.setattr("main.retriever", mock_retriever)
    monkeypatch.setattr("main.llm", mock_llm)

    response = await qa_service.answer_question("Test question?")

    assert "answer" in response
    assert "context" in response
