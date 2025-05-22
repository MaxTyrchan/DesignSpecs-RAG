from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat
from helpers import partitioning
from helpers import chunking


def convert_document(pdf):
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_picture_description = True
    pipeline_options.generate_picture_images = True
    pipeline_options.images_scale = 2
    pipeline_options.do_picture_classification = True


    converter = DocumentConverter(format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    })

    try:
        result = converter.convert(pdf)
        doc = result.document
    except Exception as e:
        raise Exception(f"Error converting document: {e}")
    try:
        partitioned_data =  partitioning(doc)
    except Exception as e:
        raise Exception(f"Error partitioning document: {e}")
    # Since the partitioning step already divides an entire document into its structural elements. 
    # Individual elements will only be split if they exceed the desired maximum chunk size. 
    # Two or more consecutive text elements that will together fit within max_characters will be combined.