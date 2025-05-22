import uuid
from langchain_chroma import Chroma
from langchain.storage import InMemoryStore
from langchain.schema.document import Document
from langchain_openai import AzureOpenAIEmbeddings
from langchain.retrievers.multi_vector import MultiVectorRetriever

azure_embeddings_endpoint = os.getenv("AZURE_OPENAI_EMBEDDINGS_ENDPOINT")

embeddings = AzureOpenAIEmbeddings(
    model="text-embedding-3-large",
    api_version="2024-12-01-preview",
    azure_endpoint=azure_embeddings_endpoint,
    api_key=azure_api_key,
)