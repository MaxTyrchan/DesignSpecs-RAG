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
