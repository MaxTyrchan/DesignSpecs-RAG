import os
from docling.chunking import HybridChunker
import tiktoken
from docling_core.transforms.chunker.tokenizer.openai import OpenAITokenizer
from docling_core.transforms.chunker.hierarchical_chunker import (
    ChunkingDocSerializer,
    ChunkingSerializerProvider,
)
from docling_core.transforms.serializer.markdown import MarkdownTableSerializer
from docling_core.transforms.serializer.markdown import MarkdownParams
from typing import Any
from docling_core.transforms.serializer.base import (
    BaseDocSerializer,
    SerializationResult,
)
from docling_core.transforms.serializer.common import create_ser_result
from docling_core.transforms.serializer.markdown import MarkdownPictureSerializer
from docling_core.types.doc.document import (
    PictureClassificationData,
    PictureDescriptionData,
    PictureItem,
    PictureMoleculeData,
)
from docling_core.types.doc.document import DoclingDocument


class SerializerProvider(ChunkingSerializerProvider):
    def get_serializer(self, doc):
        return ChunkingDocSerializer(
            doc=doc,
            # configuring a different table serializer
            table_serializer=MarkdownTableSerializer(),
            # Leave out images eventually because we already have them in the image_summaries
            # params=MarkdownParams(
            # image_placeholder="<!-- image -->",
            # ),
        )


class Chunker(SerializerProvider):
    def __init__(self, tokenizer):
        self.hybrid_chunker = HybridChunker(
            tokenizer=tokenizer,
            merge_peers=True,  # optional, defaults to True
            serializer_provider=SerializerProvider(),
        )

    def chunking(self, doc: DoclingDocument):
        chunks = list(self.hybrid_chunker.chunk(dl_doc=doc))
        return chunks
