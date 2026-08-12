import base64
from docling_core.types.doc.document import DoclingDocument
from docling_core.types.doc.labels import DocItemLabel
from .chunking import Chunker


def partitioning(doc: DoclingDocument, chunker: Chunker):
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

    # Chunking
    try:
        chunks = chunker.chunking(doc)
        for chunk in chunks:
            ser_txt = chunker.hybrid_chunker.contextualize(chunk=chunk)
            for it in chunk.meta.doc_items:
                if it.label == DocItemLabel.TABLE:
                    partitioned_data["tables"].append(chunk)
                    partitioned_data["tables_summaries"].append(ser_txt)
                elif it.label == DocItemLabel.TEXT:
                    # chunk.text to only include the text | chunk for text and metadata
                    partitioned_data["texts"].append(chunk)
                    partitioned_data["texts_summaries"].append(ser_txt)
                else:
                    pass
    except Exception as e:
        print(f"Error chunking: {e}")

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

    # Validate that we have content
    if not any(partitioned_data.values()):
        raise ValueError("No content was extracted from the document")

    return partitioned_data
