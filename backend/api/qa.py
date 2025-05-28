from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.qa_service import QAService
from ..services.vector_store import VectorStore

# Initialize services
vector_store = VectorStore()
qa_service = QAService(vector_store)

router = APIRouter()


class QuestionRequest(BaseModel):
    question: str


@router.post("/ask")
async def ask_question(request: QuestionRequest):
    """
    Answer a question about the uploaded documents.

    Args:
        request: QuestionRequest containing the question

    Returns:
        Answer and relevant context from the documents
    """
    try:
        result = await qa_service.answer_question(request.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
