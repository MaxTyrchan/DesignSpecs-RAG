import os
from pathlib import Path
from typing import List, Dict, Any
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat
from helpers import partitioning
from helpers import chunking
from PIL import Image
import base64


class DocumentProcessor:
    def __init__(self):
        # Set environment variables for OCR
        os.environ["OCR_AGENT"] = "unstructured.partition.utils.ocr_models.tesseract_ocr.OCRAgentTesseract"

    def process_pdf(self, file_path: str) -> Dict[str, List[Any]]:
        """
        Process a PDF file and extract text, tables, and images.

        Args:
            file_path: Path to the PDF file

        Returns:
            Dictionary containing lists of extracted texts, tables, and images
        """
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_picture_description = True
        pipeline_options.generate_picture_images = True
        pipeline_options.images_scale = 2
        pipeline_options.do_picture_classification = True

        converter = DocumentConverter(format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        })

        try:
            result = converter.convert(file_path)
            doc = result.document
        except Exception as e:
            raise Exception(f"Error converting document: {e}")
        try:
            partitioned_data = partitioning(doc)
        except Exception as e:
            raise Exception(f"Error partitioning document: {e}")
        # Since the partitioning step already divides an entire document into its structural elements.
        # Individual elements will only be split if they exceed the desired maximum chunk size.
        # Two or more consecutive text elements that will together fit within max_characters will be combined.
        # Extract content using Unstructured

    def save_uploaded_file(self, file_content: bytes, filename: str) -> str:
        """
        Save an uploaded file to the assets directory.

        Args:
            file_content: Binary content of the file
            filename: Name of the file

        Returns:
            Path where the file was saved
        """
        # Create assets directory if it doesn't exist
        assets_dir = Path("backend/assets")
        assets_dir.mkdir(parents=True, exist_ok=True)

        # Save the file
        file_path = assets_dir / filename
        with open(file_path, "wb") as f:
            f.write(file_content)

        return str(file_path)
