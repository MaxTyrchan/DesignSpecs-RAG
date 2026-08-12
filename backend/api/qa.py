from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.initialize import (qa_service)

# Initialize the router
router = APIRouter()

# Define the request model


class QuestionRequest(BaseModel):
    question: str


@router.post("/ask")
async def ask_question(request: QuestionRequest):
    try:
        result = await qa_service.answer_question(request.question)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
