from docling.datamodel.base_models import DoclingDocument
import base64
from helpers import chunking

def partitioning(doc: DoclingDocument):
    """
    This function is used to partition the data into different sets.
    """
        # Partition the document into different sets
    partitioned_data = {
            "text": [],
            "text_summaries": [],
            "images": [],
            "images_summaries": [],
            "tables": []
    }
    try:
        for table in doc.tables:
            partitioned_data["tables"].append(table.export_to_markdown(doc))
    except Exception as e:
        print(f"Error partitioning tables: {e}")
    try:
        for picture in doc.pictures:
            img = picture.get_image(doc)
        try:
            b64 = picture._image_to_base64(img)
            decoded_image = base64.b64decode(b64, validate=True)
            if decoded_image:
                partitioned_data["images"].append(b64)
        except Exception as e:
            print(f"Error decoding image: {e}")
        for annotation in picture.annotations:
              if annotation.kind == "description":
                   print(f"Image description: {annotation.text}")
                   partitioned_data["image_summaries"].append(annotation.text)
    except Exception as e:
        print(f"Error partitioning images: {e}")
    try:
        #TODO: Figure out to only pass text here!
        # Maybe use unstructured text here?
        result = chunking(doc)
        for chunk in enumerate(result.chunks):
            partitioned_data["texts"].append(chunk.text)
        partitioned_data["text_summaries"] = result.chunks_summaries
    except Exception as e:
        print(f"Error partitioning text: {e}")
    return partitioned_data