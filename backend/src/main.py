from unstructured.partition.pdf import partition_pdf
import pytest
from services.categorizer import categorize

file_path = "src/assets/Table.pdf"

# Partition the PDF file into elements via ocr
#The hi_res_model_name parameter supports the yolox and detectron2_onnx arguments
pdf_elements = partition_pdf(filename=file_path,
                             strategy='hi_res',
                             infer_table_structure=True,
                             hi_res_model_name='yolox',
                             extract_image_block_types=['Image'],
                             #extract_image_block_to_payload=True, #If True, will extract base64 for API usage
                             chunking_strategy='by_title',          # splitting strategy for the document (related elements are now grouped together)
                             max_characters=10000,                  # defaults to 500
                             combine_text_under_n_chars=2000,       # defaults to 0
                             new_after_n_chars=6000,)


# Create a dictionary of the unique elements
print(categorize(pdf_elements))

# Next we can focus on handling the different types of elements such as text, image, table, etc.

# if __name__ == '__main__':
#     pytest.main(['test/'])