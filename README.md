# ChatSheetPT

## From Docs to Dialogue: Talking to Design Specifications

ChatSheetPT, a domain-specific Retrieval-Augmented Generation (RAG) system developed to improve access to complex, multimodal design specifications in datasheets.
Datasheets containing design specifications of semiconductors are often lengthy collections of detailed textual descriptions, fragmented into various datasheets, and multimodal by combining tabular data and complex technical diagrams and illustrations, making them difficult to navigate and understand, particularly for non-experts.
To address this challenge, Chat-SheetPT integrates document classification, hybrid chunking, contextual embeddings, multimodal augmentation, and re-ranked retrieval to deliver context-aware, traceable, and multimodal answers to domain questions. The system is built in a modular
way, leveraging the LangChain framework and seamlessly replaceable Large Language Models via LiteLLM. It was evaluated through LLM-as-a-judge using correctness, helpfulness, groundedness, relevance, hallucination, and conciseness metrics.
In terms of helpfulness, groundedness, relevance, and hallucination, the results indicate a strong performance, while highlighting it’s current limitations in conciseness and correctness.  

## 🏗️ Architecture Overview

Architecture Chart: https://excalidraw.com/#json=3SJuJvtFE5d45sGEKiAX7,1wmmJtzm6ReUGIzgZAb1qA

```
┌─────────────────────┐    ┌──────────────────────┐  
│                     │    │                      │   
│   Frontend          │◄──►│   Backend            │
│   (React/Vite)      │    │   (FastAPI)          │    
│                     │    │                      │    
│   - Question UI     │    │   - Semantic Search  │   
│   - File Upload     │    │   - Document Upload  │   
│   - Evaluation      │    │   - Evaluation       │   
│                     │    │                      │    
└─────────────────────┘    └──────────────────────┘    
                                        │
                                        ▼
                           ┌──────────────────────┐
                           │                      │
                           │ ChromaDB & FileStore │
                           │ (Vector & Doc Store) │
                           │                      │
                           └──────────────────────┘
```

#### ⚠️ Disclaimer:

The API and frontend are showcase components built to demonstrate the RAG in the Jupyter Notebook.
GitHub Copilot was used during development for suggestions, error-handling, and improvements of the Full-Stack Web Application including Testing.
The architecture builds on LangChain’s semi-structured multimodal RAG (https://blog.langchain.dev/semi-structured-multi-modal-rag/) and was extended for performance improvements.
