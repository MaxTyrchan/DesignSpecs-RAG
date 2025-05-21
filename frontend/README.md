# Frontend

## Quickstart Setup

### 1. Install dependencies

```shell
npm install
```

### 2. Run

```shell
npm run dev
```

### 3. Navigate to [http://localhost:3000](http://localhost:3000).

## Overview

This frontend is intended to serve as an example interface for interacting with the RAG.

### Pages

- Chat: [http://localhost:3000/](http://localhost:3000/)
- Document Store: [http://localhost:3000/documents](http://localhost:3000/documents)
- Evaluation: [http://localhost:3000/evaluation](http://localhost:3000/evaluation)

### Main Components

- `app/components/chat.tsx` - handles chat rendering.
- `app/components/file-viewer.tsx` - handles uploading, fetching, and deleting files.

### Endpoints

- `api/` - `POST`: create assistant (only used at startup)
- `api/threads` - `POST`: create new thread
- `api/threads/[threadId]/messages` - `POST`: send message
- `api/files` - `GET`/`POST`/`DELETE`: fetch, upload, and delete assistant files for file search
