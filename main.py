import pytest
from langfuse import Langfuse
import os
from dotenv import load_dotenv

load_dotenv()

azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
langfuse_secret_key = os.getenv("LANGFUSE_SECRET_KEY")
langfuse_public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
langfuse_host = "http://localhost:3000"

langfuse = Langfuse(
    secret_key=langfuse_secret_key,
    public_key=langfuse_public_key,
    host=langfuse_host
)
# Next we can focus on handling the different types of elements such as text, image, table, etc.

# if __name__ == '__main__':
#     pytest.main(['test/'])
