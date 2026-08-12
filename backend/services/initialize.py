import os
from pathlib import Path
from dotenv import load_dotenv
import chromadb
from langchain.storage import LocalFileStore
from langchain_chroma import Chroma
from langchain_litellm import ChatLiteLLM
from langchain_openai import AzureOpenAIEmbeddings
from datetime import datetime
from .helpers.embedding import Embedding
from .helpers.chunking import Chunker
from .qa_service import QAService
from langchain.retrievers.multi_vector import MultiVectorRetriever
from .helpers.reranker import Reranker

# Load environment variables first
load_dotenv()


def get_env_variable(var_name: str) -> str:
    value = os.getenv(var_name)
    if value is None:
        raise ValueError(f"Environment variable '{var_name}' not found.")
    return value


# Initialize environment variables
bosch_api_key = get_env_variable("AZURE_BOSCH_API_KEY")
bosch_endpoint = get_env_variable("AZURE_BOSCH_ENDPOINT")
bosch_embeddings_endpoints = get_env_variable(
    "AZURE_BOSCH_EMBEDDINGS_ENDPOINT")
bosch_embeddings_api_key = get_env_variable("AZURE_BOSCH_EMBEDDINGS_API_KEY")


azure_api_key = get_env_variable("AZURE_OPENAI_API_KEY")
azure_endpoint = get_env_variable("AZURE_OPENAI_ENDPOINT")
azure_embeddings_endpoint = get_env_variable(
    "AZURE_OPENAI_EMBEDDINGS_ENDPOINT")
azure_eval_endpoint = get_env_variable("AZURE_OPENAI_EVAL_ENDPOINT")
azure_endpoint_fallback = get_env_variable(
    "AZURE_OPENAI_ENDPOINT_FALLBACK")

llm = ChatLiteLLM(
    api_key=bosch_api_key,
    api_base=bosch_endpoint,
    model="azure/gpt-5.2",
)

embeddingModel = AzureOpenAIEmbeddings(
    model="text-embedding-3-large",
    azure_endpoint=bosch_embeddings_endpoints,
    openai_api_key=bosch_embeddings_api_key,
    openai_api_version="2023-05-15",  # Updated to newer stable version
)

file_store = LocalFileStore("./db/docs")

# Initialize chunker
chunker = Chunker()

# Initialize embeddings instance
# TODO: Use a Multimodal Embedding if available
embeddings = Embedding(embeddingModel)

# Ensure the database directory exists with proper permissions
db_path = Path("./db/chroma")
db_path.mkdir(parents=True, exist_ok=True)

# Initialize Chroma with persistent storage and proper settings
chroma_client = chromadb.PersistentClient(
    path=str(db_path),
    settings=chromadb.Settings(
        allow_reset=True,
        is_persistent=True,
        anonymized_telemetry=False
    )
)

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

# Initialize retriever with fixed bytes handling
retriever = MultiVectorRetriever(
    vectorstore=vectorstore,
    docstore=file_store,
    # Retrieve more documents to include tables and images
    search_kwargs={"k": 10}
)

# Initialize QA services
qa_service = QAService()
qa_service.set_retriever(retriever)
qa_service.set_llm(llm)

# Initialize Reranker
reranker = Reranker()
