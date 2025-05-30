import uvicorn
import pytest
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langfuse import Langfuse
import os
from dotenv import load_dotenv
from api.upload import router as upload_router
from api.qa import router as qa_router
import chromadb
from langchain.storage import LocalFileStore
from langchain.storage._lc_store import create_kv_docstore
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain.retrievers.multi_vector import MultiVectorRetriever
from datetime import datetime
from fastapi import APIRouter
from services.document_processor import DocumentProcessor
from services.qa_service import QAService

# Load environment variables
load_dotenv()


def get_env_variable(var_name: str) -> str:
    value = os.getenv(var_name)
    if value is None:
        raise ValueError(f"Environment variable '{var_name}' not found.")
    return value


# Initialize environment variables
azure_api_key = get_env_variable("AZURE_OPENAI_API_KEY")
azure_endpoint = get_env_variable("AZURE_OPENAI_ENDPOINT")
azure_embedding_deployment = get_env_variable("AZURE_EMBEDDING_DEPLOYMENT")
langfuse_secret_key = get_env_variable("LANGFUSE_SECRET_KEY")
langfuse_public_key = get_env_variable("LANGFUSE_PUBLIC_KEY")
langfuse_host = "http://localhost:3000"

embeddings = AzureOpenAIEmbeddings(
    model="text-embedding-3-large",
    api_version="2024-12-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_EMBEDDINGS_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)

llm = AzureChatOpenAI(api_version="2024-12-01-preview",
                      azure_endpoint=azure_endpoint,
                      api_key=azure_api_key,
                      temperature=0,
                      model="gpt-4o")

vectorstore = chromadb.Client().get_or_create_collection(
    name="DesignSpecsRAG", embedding_function=embeddings, metadata={"created": str(datetime.now())})

file_store = LocalFileStore("./db/docs")

retriever = MultiVectorRetriever(
    vectorstore=vectorstore,
    docstore=file_store,
)

qa_service = QAService(vectorstore)

document_processor = DocumentProcessor()

# Instantiate the LocalFileStore with the root path if it has no LocalFileStore inside
if not os.Path("db/docs").exists():  # Check if directory exists
    os.Path("db/docs").mkdir(parents=True, exist_ok=True)
    create_kv_docstore(file_store)
    file_store = LocalFileStore("./db/docs")

# Initialize Langfuse
langfuse = Langfuse(
    secret_key=langfuse_secret_key,
    public_key=langfuse_public_key,
    host=langfuse_host
)

# Initialize the router
router = APIRouter()

# Initialize FastAPI app
app = FastAPI(
    title="DesignSpecs RAG API",
    description="API for processing design specification documents and answering questions",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload_router, prefix="/api", tags=["Document Upload"])
app.include_router(qa_router, prefix="/api", tags=["Question Answering"])

# Health check endpoint


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == '__main__':
    pytest.main(['test/'])
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Enable auto-reload during development
    )
