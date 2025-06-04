import logging
from pathlib import Path
from typing import List, Dict, Any
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat
from .helpers.partitioning import partitioning
from .helpers.embedding import Embedding
from .helpers.chunking import Chunker
from langchain.retrievers.multi_vector import MultiVectorRetriever
import os

# Set up logging
logger = logging.getLogger(__name__)


class DocumentProcessor:
    def __init__(self):
        logger.info("Initializing DocumentProcessor")
        self.pipeline_options = PdfPipelineOptions()
        self.pipeline_options.do_picture_description = True
        self.pipeline_options.generate_picture_images = True
        self.pipeline_options.images_scale = 2
        self.pipeline_options.do_picture_classification = True

        logger.info("Setting up document converter")
        self.converter = DocumentConverter(format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=self.pipeline_options)
        })

        # Get the path relative to the backend directory
        current_dir = Path(__file__).parent  # services directory
        backend_dir = current_dir.parent     # backend directory
        self.assets_dir = backend_dir / "assets"

    def process_pdf(self, file_path: str, embeddings: Embedding, chunker: Chunker, retriever: MultiVectorRetriever) -> Dict[str, List[Any]]:
        """
        Process a PDF file and extract text, tables, and images.

        Args:
            file_path: Path to the PDF file

        Returns:
            Dictionary containing lists of extracted texts, tables, and images
        """
        logger.info(f"Starting PDF processing for file: {file_path}")

        # Convert document
        try:
            logger.info("Converting document")
            result = self.converter.convert(file_path)
            doc = result.document
            if not doc:
                raise ValueError("Document conversion produced no output")
            logger.info("Document converted successfully")
        except Exception as e:
            logger.error(f"Error converting document: {str(e)}", exc_info=True)
            raise Exception(f"Error converting document: {str(e)}")

        # Partition document
        try:
            logger.info("Partitioning document")
            partitioned_data = partitioning(doc, chunker)
            if not partitioned_data:
                raise ValueError("Document partitioning produced no data")
            logger.info("Document partitioned successfully")
        except Exception as e:
            logger.error(
                f"Error partitioning document: {str(e)}", exc_info=True)
            raise Exception(f"Error partitioning document: {str(e)}")

        # Embed document
        try:
            logger.info("Embedding document")
            embeddings.embed_pdf(partitioned_data, retriever)
            logger.info("Document embedded successfully")
        except Exception as e:
            logger.error(f"Error embedding document: {str(e)}", exc_info=True)
            raise Exception(f"Error embedding document: {str(e)}")

    def save_uploaded_file(self, file_content: bytes, filename: str) -> str:
        """
        Save an uploaded file to the assets/pdfs directory.

        Args:
            file_content: Binary content of the file
            filename: Name of the file

        Returns:
            Path where the file was saved
        """
        logger.info(f"Saving file: {filename}")

        try:
            # Create assets/pdfs directory if it doesn't exist
            pdf_dir = self.assets_dir / "pdfs"
            pdf_dir.mkdir(parents=True, exist_ok=True)

            # Save the file
            file_path = pdf_dir / filename
            with open(file_path, "wb") as f:
                f.write(file_content)

            logger.info(f"File saved successfully at: {file_path}")
            return str(file_path)
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}", exc_info=True)
            raise Exception(f"Error saving file: {str(e)}")
