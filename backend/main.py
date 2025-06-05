"""
Main entry point for the application.
Import initialize first to ensure all instances are properly initialized
before importing other modules.
"""

# First, import initialize to set up all instances
from services.initialize import *
from services.document_processor import DocumentProcessor
from services.qa_service import QAService
import uvicorn
import pytest
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langfuse import Langfuse
from api.upload import router as upload_router
from api.qa import router as qa_router
from api.evaluation import router as evaluation_router
from langchain.storage import LocalFileStore
from langchain.storage._lc_store import create_kv_docstore


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
app.include_router(evaluation_router, prefix="/api", tags=["Evaluation"])

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
