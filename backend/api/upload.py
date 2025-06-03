import logging
from fastapi import APIRouter, UploadFile, HTTPException
from services.initialize import embeddings, chunker, retriever
from services.document_processor import DocumentProcessor

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the router
router = APIRouter()


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
