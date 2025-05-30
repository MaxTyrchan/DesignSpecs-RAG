# Backend

## Setup

### Docker

1. Pull the ChromaDB Docker image

```bash
docker pull chromadb/chroma
```

2. Run the ChromaDB Docker container

```bash
docker run -d -p 8000:8000 chromadb/chroma
```

3. Verify that the ChromaDB server is running

```bash
curl http://localhost:8000
```

### Local

1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Start the ChromaDB server

```bash
chroma run --path ./db/chroma
```

3. Run the application

```bash
uvicorn main:app --reload
```