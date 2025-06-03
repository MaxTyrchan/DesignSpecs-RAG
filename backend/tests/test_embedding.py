import pytest
from services.helpers.embedding import Embedding


def test_embedding_initialization(mock_azure_embeddings):
    """Test that the Embedding class initializes correctly."""
    embedding = Embedding(mock_azure_embeddings, name="test_embeddings")
    assert embedding.name() == "test_embeddings"
    assert embedding.text_item == "text_item"
    assert embedding.inner == mock_azure_embeddings


def test_embedding_call_method(mock_embeddings):
    """Test that the __call__ method works correctly."""
    texts = ["This is a test", "This is another test"]
    embeddings = mock_embeddings(texts)
    assert len(embeddings) == 2
    assert len(embeddings[0]) == 1536  # text-embedding-3-large dimension
    assert len(embeddings[1]) == 1536


def test_embed_documents_method(mock_embeddings):
    """Test that the embed_documents method works correctly."""
    texts = ["This is a test", "This is another test"]
    embeddings = mock_embeddings.embed_documents(texts)
    assert len(embeddings) == 2
    assert len(embeddings[0]) == 1536
    assert len(embeddings[1]) == 1536


def test_embed_query_method(mock_embeddings):
    """Test that the embed_query method works correctly."""
    query = "This is a test query"
    embedding = mock_embeddings.embed_query(query)
    assert len(embedding) == 1536


def test_embed_pdf_with_empty_data(mock_embeddings):
    """Test that embed_pdf handles empty data correctly."""
    empty_data = {
        "texts": [],
        "texts_summaries": [],
        "images": [],
        "images_summaries": [],
        "tables": [],
        "tables_summaries": []
    }

    class MockDocStore:
        def __init__(self):
            self.stored_items = {}

        def mset(self, items):
            for key, value in items:
                self.stored_items[key] = value

    class MockRetriever:
        id_key = "doc_id"

        def __init__(self):
            self.added_documents = []
            self.mset_calls = []

        class MockVectorStore:
            def __init__(self):
                self.added_docs = []

            def add_documents(self, docs):
                self.added_docs.extend(docs)

        vectorstore = MockVectorStore()
        docstore = MockDocStore()

    mock_retriever = MockRetriever()

    # Should not raise any exceptions
    mock_embeddings.embed_pdf(empty_data, mock_retriever)


def test_embed_pdf_with_data(mock_embeddings):
    """Test that embed_pdf processes data correctly."""
    test_data = {
        "texts": ["text1", "text2"],
        "texts_summaries": ["summary1", "summary2"],
        "images": ["img1", "img2"],
        "images_summaries": ["img_summary1", "img_summary2"],
        "tables": ["table1", "table2"],
        "tables_summaries": ["table_summary1", "table_summary2"]
    }

    class MockDocStore:
        def __init__(self):
            self.stored_items = {}

        def mset(self, items):
            for key, value in items:
                self.stored_items[key] = value

    class MockRetriever:
        id_key = "doc_id"

        def __init__(self):
            self.added_documents = []
            self.mset_calls = []

        class MockVectorStore:
            def __init__(self):
                self.added_docs = []

            def add_documents(self, docs):
                self.added_docs.extend(docs)

        vectorstore = MockVectorStore()
        docstore = MockDocStore()

    mock_retriever = MockRetriever()

    # Should process all data without raising exceptions
    mock_embeddings.embed_pdf(test_data, mock_retriever)

    # Verify that documents were added to vectorstore and docstore
    # 2 texts + 2 tables + 2 images
    assert len(mock_retriever.vectorstore.added_docs) == 6
    assert len(mock_retriever.docstore.stored_items) == 6  # Same as above
