import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any
import os
from pathlib import Path


class VectorStore:
    def __init__(self):
        # Initialize ChromaDB client with persistence
        db_path = Path("backend/db/chroma")
        db_path.mkdir(parents=True, exist_ok=True)

        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=str(db_path)
        ))

        # Create collections for different types of content
        self.text_collection = self.client.get_or_create_collection("texts")
        self.table_collection = self.client.get_or_create_collection("tables")

    def add_document(self, document_id: str, content: Dict[str, List[Any]]):
        """
        Add document content to the vector store.

        Args:
            document_id: Unique identifier for the document
            content: Dictionary containing texts and tables
        """
        # Add texts
        if content["texts"]:
            self.text_collection.add(
                documents=content["texts"],
                metadatas=[{"document_id": document_id, "type": "text"}
                           for _ in content["texts"]],
                ids=[f"{document_id}_text_{i}" for i in range(
                    len(content["texts"]))]
            )

        # Add tables
        if content["tables"]:
            self.table_collection.add(
                documents=content["tables"],
                metadatas=[{"document_id": document_id, "type": "table"}
                           for _ in content["tables"]],
                ids=[f"{document_id}_table_{i}" for i in range(
                    len(content["tables"]))]
            )

    def search(self, query: str, n_results: int = 5) -> Dict[str, List[Dict[str, Any]]]:
        """
        Search for relevant content across all collections.

        Args:
            query: Search query
            n_results: Number of results to return per collection

        Returns:
            Dictionary containing search results from each collection
        """
        # Search texts
        text_results = self.text_collection.query(
            query_texts=[query],
            n_results=n_results
        )

        # Search tables
        table_results = self.table_collection.query(
            query_texts=[query],
            n_results=n_results
        )

        return {
            "texts": [
                {
                    "content": doc,
                    "metadata": meta,
                    "distance": dist
                }
                for doc, meta, dist in zip(
                    text_results["documents"][0],
                    text_results["metadatas"][0],
                    text_results["distances"][0]
                )
            ],
            "tables": [
                {
                    "content": doc,
                    "metadata": meta,
                    "distance": dist
                }
                for doc, meta, dist in zip(
                    table_results["documents"][0],
                    table_results["metadatas"][0],
                    table_results["distances"][0]
                )
            ]
        }
