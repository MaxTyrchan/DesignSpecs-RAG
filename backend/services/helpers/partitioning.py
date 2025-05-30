from docling.datamodel.base_models import DoclingDocument
from docling_core.types.doc.labels import DocItemLabel
import base64
from helpers.chunking import Chunker


def partitioning(doc: DoclingDocument):
    """
    This function is used to partition the data into different sets.
    """
    # Partition the document into different sets
    partitioned_data = {
        "texts": [],
        "texts_summaries": [],
        "images": [],
        "images_summaries": [],
        "tables": [],
        "tables_summaries": []
    }

    chunker = Chunker()

    # Chunking
    try:
        chunks = chunker.chunking(doc)
        for chunk in enumerate(chunks):
            ser_txt = chunker.hybrid_chunker.contextualize(chunk=chunk)
            for it in chunk.meta.doc_items:
                if it.label == DocItemLabel.PICTURE:
                    break
                if it.label == DocItemLabel.TABLE:
                    partitioned_data["tables_summaries"].append(ser_txt)
                    break
                if it.label == DocItemLabel.TEXT:
                    partitioned_data["texts"].append(chunk.text)
                    partitioned_data["texts_summaries"].append(ser_txt)
                    break
    except Exception as e:
        print(f"Error chunking: {e}")

    # Table extraction
    try:
        for table in doc.tables:
            partitioned_data["tables"].append(table.export_to_markdown(doc))
    except Exception as e:
        print(f"Error partitioning tables: {e}")

    # Image extraction
    try:
        for picture in doc.pictures:
            img = picture.get_image(doc)
            if any(annotation.kind == "description" for annotation in picture.annotations):
                try:
                    b64 = picture._image_to_base64(img)
                    decoded_image = base64.b64decode(b64, validate=True)
                    if decoded_image:
                        partitioned_data["images"].append(b64)
                except Exception as e:
                    print(f"Error decoding image: {e}")
                for annotation in picture.annotations:
                    if annotation.kind == "description":
                        partitioned_data["images_summaries"].append(
                            annotation.text)
            else:
                pass
    except Exception as e:
        print(f"Error partitioning images: {e}")

    return partitioned_data
