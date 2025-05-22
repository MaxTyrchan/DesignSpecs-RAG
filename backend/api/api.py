from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services import convert_document

app = FastAPI()

# Enable CORS for frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/add-documents/")
async def add_documents(documents: list[DocumentModel]):
    try:
        for doc in documents:
            convert_document(doc)
        return {"message": "Documents added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/chat/")
async def response(msg: str):
    result = chain.invoke(msg)
    return result