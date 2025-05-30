from fastapi import HTTPException
from main import qa_service, router


@router.post("/ask")
async def ask_question(question: str):
    """
    Answer a question about the uploaded documents.

    Returns:
        Answer and relevant context from the documents
    """
    try:
        result = await qa_service.answer_question(question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
