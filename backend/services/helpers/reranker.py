from typing import List, Optional
from langchain_community.document_compressors import FlashrankRerank
from langchain.schema.document import Document
import logging

logger = logging.getLogger(__name__)


class Reranker:
    """
    Reranking service using FlashRank.
    """

    def __init__(self, model: str = "rank-T5-flan"):
        self.model = model
        self.compressor = FlashrankRerank(model=self.model)

    def rerank_documents(self, query: str, documents: List[Document], top_n: Optional[int] = None) -> List[Document]:
        if not documents:
            return []

        try:
            compressed_docs = self.compressor.compress_documents(
                documents=documents,
                query=query
            )

            if top_n is not None:
                return compressed_docs[:top_n]
            print(
                f"Reranked {len(documents)} documents to top {len(compressed_docs)}")
            return compressed_docs

        except Exception as e:
            logger.error(f"Error during document reranking: {e}")
            # Fallback: return original documents
            if top_n is not None:
                return documents[:top_n]
            return documents
