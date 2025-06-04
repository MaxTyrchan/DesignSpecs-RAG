"""
This module initializes all services in the correct order to avoid circular imports.
Import this module first in main.py before importing any other modules.
"""
import os
from pathlib import Path
from dotenv import load_dotenv
import tiktoken
import chromadb
from langchain.storage import LocalFileStore
from langchain_chroma import Chroma
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from datetime import datetime
from .helpers.embedding import Embedding
from .helpers.chunking import Chunker

# Load environment variables first
load_dotenv()


def get_env_variable(var_name: str) -> str:
    value = os.getenv(var_name)
    if value is None:
        raise ValueError(f"Environment variable '{var_name}' not found.")
    return value


# Initialize environment variables
azure_api_key = get_env_variable("AZURE_OPENAI_API_KEY")
azure_endpoint = get_env_variable("AZURE_OPENAI_ENDPOINT")
azure_embeddings_endpoint = get_env_variable(
    "AZURE_OPENAI_EMBEDDINGS_ENDPOINT")
langfuse_secret_key = get_env_variable("LANGFUSE_SECRET_KEY")
langfuse_public_key = get_env_variable("LANGFUSE_PUBLIC_KEY")
langfuse_host = "http://localhost:3000"


llm = AzureChatOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint=azure_endpoint,
    api_key=azure_api_key,
    temperature=0,
    model="gpt-4o"
)

embeddingModel = AzureOpenAIEmbeddings(
    model="text-embedding-3-large",
    api_version="2024-12-01-preview",
    azure_endpoint=azure_embeddings_endpoint,
    api_key=azure_api_key,
)

file_store = LocalFileStore("./db/docs")

# Initialize chunker
chunker = Chunker()

# Initialize embeddings instance
embeddings = Embedding(embeddingModel)

# Initialize Chroma
chroma_client = chromadb.Client()

collection = chroma_client.get_or_create_collection(
    name="DesignSpecsRAG",
    embedding_function=embeddings,
    metadata={"created": str(datetime.now())}
)

# Initialize vector store
vectorstore = Chroma(
    collection_name="DesignSpecsRAG",
    embedding_function=embeddings,
    client=chroma_client
)

# Initialize retriever
retriever = MultiVectorRetriever(
    vectorstore=vectorstore,
    docstore=file_store,
)
