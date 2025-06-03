from fastapi import APIRouter, HTTPException
from services.initialize import retriever, llm
from services.qa_service import QAService

# Initialize the router
router = APIRouter()


@router.post("/ask")
async def ask_question(question: str):
    """
    Answer a question about the uploaded documents.

    Returns:
        Answer and relevant context from the documents
    """

    # Initialize qa service
    qa_service = QAService()
    qa_service.set_retriever(retriever)
    qa_service.set_llm(llm)

    try:
        result = await qa_service.answer_question(question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
