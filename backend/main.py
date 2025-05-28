from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langfuse import Langfuse
import os
from dotenv import load_dotenv
from api.upload import router as upload_router
from api.qa import router as qa_router

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
langfuse_secret_key = get_env_variable("LANGFUSE_SECRET_KEY")
langfuse_public_key = get_env_variable("LANGFUSE_PUBLIC_KEY")
langfuse_host = "http://localhost:3000"

# Initialize Langfuse
langfuse = Langfuse(
    secret_key=langfuse_secret_key,
    public_key=langfuse_public_key,
    host=langfuse_host
)

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

# if __name__ == '__main__':
#     pytest.main(['test/'])
