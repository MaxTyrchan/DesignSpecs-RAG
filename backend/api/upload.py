import logging
from fastapi import APIRouter, UploadFile, HTTPException
from services.initialize import embeddings, chunker, retriever
from services.document_processor import DocumentProcessor
import os
from pathlib import Path
from fastapi.responses import FileResponse

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the router
router = APIRouter()


@router.get("/files")
async def list_files():
    """
    List all PDF files in the assets directory.

    Returns:
        List of file information
    """
    try:
        document_processor = DocumentProcessor()
        pdf_dir = Path(document_processor.assets_dir) / "pdfs"

        if not pdf_dir.exists():
            return []

        files = []
        for file_path in pdf_dir.glob("*.pdf"):
            stat = file_path.stat()
            files.append({
                "id": file_path.stem,
                "name": file_path.name,
                "size": stat.st_size,
                "type": "application/pdf",
                "uploadDate": stat.st_mtime
            })

        return files
    except Exception as e:
        logger.error(f"Error listing files: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{file_id}")
async def download_file(file_id: str):
    """
    Download a PDF file by its ID.

    Args:
        file_id: The ID (stem) of the file to download

    Returns:
        The PDF file
    """
    try:
        document_processor = DocumentProcessor()
        pdf_dir = Path(document_processor.assets_dir) / "pdfs"

        # Find the file with matching stem
        for file_path in pdf_dir.glob("*.pdf"):
            if file_path.stem == file_id:
                return FileResponse(
                    path=file_path,
                    media_type="application/pdf",
                    filename=file_path.name
                )

        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        logger.error(f"Error downloading file: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload")
async def upload_file(file: UploadFile):
    """
    Upload and process a PDF file.

    Args:
        file: The PDF file to upload

    Returns:
        Success message if the file is uploaded successfully
    """
    logger.info(f"Starting upload process for file: {file.filename}")

    # Initialize document processor and qa service
    document_processor = DocumentProcessor()

    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        logger.error(f"Invalid file type: {file.filename}")
        raise HTTPException(
            status_code=400, detail="Only PDF files are allowed")

    try:
        # Read file content
        logger.info("Reading file content")
        content = await file.read()

        # Save the file
        logger.info("Saving file to disk")
        file_path = document_processor.save_uploaded_file(
            content, file.filename)

        logger.info(f"File saved at: {file_path}")

        # Process the PDF
        logger.info("Starting PDF processing")
        try:
            document_processor.process_pdf(
                file_path, embeddings, chunker, retriever)
        except ValueError as ve:
            logger.error(f"Validation error during PDF processing: {str(ve)}")
            raise HTTPException(status_code=400, detail=str(ve))
        except Exception as e:
            logger.error(
                f"Error during PDF processing: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500, detail=f"Error processing PDF: {str(e)}")

        logger.info("PDF processing completed successfully")
        return {
            "message": "File processed successfully",
            "filename": file.filename,
        }

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
