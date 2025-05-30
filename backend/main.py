import uvicorn
import pytest
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langfuse import Langfuse
import os
from dotenv import load_dotenv
from api.upload import router as upload_router
from api.qa import router as qa_router
from langchain.storage import LocalFileStore
from langchain.storage._lc_store import create_kv_docstore
from services.dependencies import *


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
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Enable auto-reload during development
    )
