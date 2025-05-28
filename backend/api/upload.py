from fastapi import APIRouter, UploadFile, HTTPException
from ..services.document_processor import DocumentProcessor

router = APIRouter()
document_processor = DocumentProcessor()


@router.post("/upload")
async def upload_file(file: UploadFile):
    """
    Upload and process a PDF file.

    Args:
        file: The PDF file to upload

    Returns:
        Processed content from the PDF including texts, tables, and images
    """
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400, detail="Only PDF files are allowed")

    try:
        # Read file content
        content = await file.read()

        # Save the file
        file_path = document_processor.save_uploaded_file(
            content, file.filename)

        # Process the PDF
        result = document_processor.process_pdf(file_path)

        return {
            "message": "File processed successfully",
            "filename": file.filename,
            "content": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
