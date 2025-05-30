from services.document_processor import DocumentProcessor
from services.qa_service import QAService
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain.retrievers.multi_vector import MultiVectorRetriever
from datetime import datetime
import chromadb
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_env_variable(var_name: str) -> str:
    value = os.getenv(var_name)
    if value is None:
        raise ValueError(f"Environment variable '{var_name}' not found.")
    return value


# Initialize environment variables and services
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
