import pytest
from langfuse import Langfuse
import os
from dotenv import load_dotenv

load_dotenv()

def get_env_variable(var_name: str) -> str:
    value = os.getenv(var_name)
    if value is None:
        raise ValueError(f"Environment variable '{var_name}' not found.")
    return value


azure_api_key = get_env_variable("AZURE_OPENAI_API_KEY")
azure_endpoint = get_env_variable("AZURE_OPENAI_ENDPOINT")
langfuse_secret_key = get_env_variable("LANGFUSE_SECRET_KEY")
langfuse_public_key = get_env_variable("LANGFUSE_PUBLIC_KEY")
langfuse_host = "http://localhost:3000"

langfuse = Langfuse(
    secret_key=langfuse_secret_key,
    public_key=langfuse_public_key,
    host=langfuse_host
)


# if __name__ == '__main__':
#     pytest.main(['test/'])
