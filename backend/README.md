# Backend

## Setup

### Local
1. Create a `.env` file in the backend directory:
```bash
# Chat Model
AZURE_OPENAI_API_KEY
# Azure Endpoint
AZURE_OPENAI_ENDPOINT
# Embeddings Model
AZURE_OPENAI_EMBEDDINGS_ENDPOINT
# LangSmith Endpoint
LANGSMITH_ENDPOINT
# LangSmith Project Name
LANGSMITH_PROJECT
# LangSmith API Key
LANGSMITH_API_KEY
```

1. Activate the virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Start the application

```bash
python main.py
```

4. Run tests:

```bash
cd backend
# Run basic tests
python -m pytest tests/test_qa_basic.py -v --no-cov

# Run all tests  
python -m pytest tests/ -v

# Run with coverage (if pytest-cov is installed)
python -m pytest tests/ -v --cov=.
```

8. Shutdown the application

```bash
control + C
```

9. Run the litellm proxy

```bash
litellm --config litellm_config.yaml --detailed_debug
```
