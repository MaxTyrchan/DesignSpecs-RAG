import os
from pathlib import Path
from typing import List, Dict, Any
from unstructured.partition.pdf import partition_pdf
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
        # Extract content using Unstructured
        chunks = partition_pdf(
            filename=file_path,
            infer_table_structure=True,
            strategy="hi_res",
            extract_image_block_types=["Image"],
            extract_image_block_to_payload=True,
            chunking_strategy='by_title',
            max_characters=50000
        )

        # Initialize containers
        tables = []
        texts = []
        images = []

        # Process each chunk
        for chunk in chunks:
            if "CompositeElement" in str(type(chunk)):
                # Extract tables
                # Create a copy to iterate
                for el in chunk.metadata.orig_elements[:]:
                    if "Table" in str(type(el)):
                        tables.append(el.metadata.text_as_html)
                        chunk.metadata.orig_elements.remove(el)
                    elif "Image" in str(type(el)):
                        images.append(el.metadata.image_base64)
                        chunk.metadata.orig_elements.remove(el)

                # Add remaining content as text
                if chunk.metadata.orig_elements:
                    texts.append(str(chunk))

        return {
            "texts": texts,
            "tables": tables,
            "images": images
        }

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
