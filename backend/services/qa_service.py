from typing import Dict, List, Any
import os
from openai import AzureOpenAI
from .vector_store import VectorStore


class QAService:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2024-02-15-preview",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )

    def _format_context(self, search_results: Dict[str, List[Dict[str, Any]]]) -> str:
        """
        Format search results into a context string for the LLM.
        """
        context = []

        # Add text content
        if search_results["texts"]:
            context.append("Text Content:")
            for result in search_results["texts"]:
                context.append(result["content"])

        # Add table content
        if search_results["tables"]:
            context.append("\nTable Content:")
            for result in search_results["tables"]:
                context.append(result["content"])

        return "\n\n".join(context)

    async def answer_question(self, question: str) -> Dict[str, Any]:
        """
        Answer a question using the vector store and Azure OpenAI.

        Args:
            question: The question to answer

        Returns:
            Dictionary containing the answer and relevant context
        """
        # Search for relevant content
        search_results = self.vector_store.search(question)
        context = self._format_context(search_results)

        # Generate system message
        system_message = """You are a helpful assistant that answers questions about technical documents. 
        Use the provided context to answer questions accurately and concisely. 
        If you cannot find the answer in the context, say so."""

        # Generate user message with context
        user_message = f"""Context:
        {context}
        
        Question: {question}
        
        Answer the question based on the context above. If the answer cannot be found in the context, say so."""

        # Get response from Azure OpenAI
        response = self.client.chat.completions.create(
            model="gpt-4",  # Use your deployed model name
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=0,
            max_tokens=500
        )

        return {
            "answer": response.choices[0].message.content,
            "context": search_results
        }
