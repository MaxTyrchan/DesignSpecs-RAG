from fastapi import FastAPI, Request
from pydantic import BaseModel
from pipeline.rag import build_rag_chain
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Enable CORS for frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load RAG chain on startup
rag_chain = build_rag_chain()


class QueryInput(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/query")
def query(input: QueryInput):
    try:
        answer = rag_chain.invoke(input.question)
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
