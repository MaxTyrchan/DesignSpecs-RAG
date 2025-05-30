from pathlib import Path
from typing import List, Dict, Any
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat
from services.helpers.partitioning import partitioning
from services.helpers.embedding import embedding


class DocumentProcessor:
    def __init__(self):
        self.pipeline_options = PdfPipelineOptions()
        self.pipeline_options.do_picture_description = True
        self.pipeline_options.generate_picture_images = True
        self.pipeline_options.images_scale = 2
        self.pipeline_options.do_picture_classification = True
        self.converter = DocumentConverter(format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=self.pipeline_options)
        })
        self.assets_dir = Path("backend/assets/pdfs")

    def process_pdf(self, file_path: str) -> Dict[str, List[Any]]:
        """
        Process a PDF file and extract text, tables, and images.

        Args:
            file_path: Path to the PDF file

        Returns:
            Dictionary containing lists of extracted texts, tables, and images
        """
        try:
            result = self.converter.convert(file_path)
            doc = result.document
        except Exception as e:
            raise Exception(f"Error converting document: {e}")
        try:
            partitioned_data = partitioning(doc)
        except Exception as e:
            raise Exception(f"Error partitioning document: {e}")
        try:
            embedding.embed_pdf(partitioned_data)
        except Exception as e:
            raise Exception(f"Error embedding document: {e}")

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
        self.assets_dir.mkdir(parents=True, exist_ok=True)

        # Save the file
        file_path = self.assets_dir / filename
        with open(file_path, "wb") as f:
            f.write(file_content)
        return str(file_path)
