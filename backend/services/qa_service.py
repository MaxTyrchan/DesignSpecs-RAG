from typing import Dict, Any, List
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from base64 import b64decode
from langchain.schema.document import Document
from langchain_core.output_parsers import StrOutputParser
from langchain.callbacks.tracers import LangChainTracer
import os
import json
import logging

logger = logging.getLogger(__name__)


class QAService:
    def __init__(self):
        self.retriever = None
        self.llm = None
        self.reranker = None
        self.tracer = LangChainTracer(
            project_name=os.getenv("LANGSMITH_PROJECT"))

    def set_retriever(self, retriever):
        self.retriever = retriever

    def set_llm(self, llm):
        self.llm = llm

    def set_reranker(self, reranker):
        self.reranker = reranker

    def _apply_reranking(self, docs: List[Document], query: str, k: int) -> List[Document]:
        try:
            return self.reranker.rerank_documents(
                query=query, documents=docs, top_n=k
            )
        except Exception as e:
            return docs[:k]

    @staticmethod
    def parse_docs(docs):
        '''Split base64-encoded images and everything else (texts/tables) into ContentItem format'''
        b64_images = []
        texts = []
        tables = []

        # Unpack the tuple (uuid, content)
        for doc_id, doc_content in enumerate(docs):

            if hasattr(doc_content, 'page_content'):
                # It's a Document object
                content_str = doc_content.page_content
                metadata = getattr(doc_content, 'metadata', {})
            elif isinstance(doc_content, bytes):
                # It's raw bytes from docstore
                content_str = doc_content.decode('utf-8')
                metadata = {}
            elif hasattr(doc_content, 'export_json_dict'):
                # It's a DoclingDocument object
                content_str = json.dumps(doc_content.export_json_dict())
                metadata = {}
            elif isinstance(doc_content, str):
                # It's a string
                content_str = doc_content
                metadata = {}
            else:
                print(f"DEBUG: Unexpected doc type: {type(doc_content)}")
                content_str = str(doc_content)
                metadata = {}

            if isinstance(content_str, str) and content_str.startswith("b'") and content_str.endswith("'"):
                # Remove the b' prefix and ' suffix to get the actual content
                try:
                    content_str = content_str[2:-1]
                    # Handle escaped characters
                    content_str = content_str.encode().decode('unicode_escape')
                except Exception as e:
                    print(
                        f"Failed to extract from byte string representation: {e}")

            # Check if it's a base64-encoded image
            try:
                # Try to decode as base64 first - if this works, it's an image
                b64decode(content_str, validate=True)
                image_item = {
                    "content": content_str,
                    "metadata": {
                        "chunk_id": f"img_{doc_id}",
                        "content_type": "image",
                        "source": metadata.get("source", "unknown"),
                        **metadata
                    }
                }
                b64_images.append(image_item)
            except:
                # If base64 decode fails, it's a JSON-encoded chunk (text or table)
                try:
                    # Try to parse as JSON (chunk data)
                    doc_json = json.loads(content_str)
                    content_text = doc_json.get('text', content_str)
                    basechunk_meta = doc_json.get('meta', {})

                    # Check if it's a table using the metadata
                    doc_items = basechunk_meta.get('doc_items', [])
                    has_table = any(item.get('label') ==
                                    'table' for item in doc_items)

                    content_item = {
                        "content": content_text,
                        "metadata": {
                            "chunk_id": f"text_{doc_id}",
                            "content_type": metadata.get("content_type", "text"),
                            "source": metadata.get("source", basechunk_meta.get("origin", {}).get("filename", "unknown")),
                            "basechunk_meta": basechunk_meta,
                            **metadata
                        }
                    }

                    # Determine if it's a table or text based on metadata analysis
                    if has_table or "table" in metadata.get("content_type", "").lower():
                        tables.append(content_item)
                    else:
                        texts.append(content_item)

                except json.JSONDecodeError:
                    # If it's not JSON, treat as plain text or table based on metadata and content
                    content_item = {
                        "content": content_str,
                        "metadata": {
                            "chunk_id": f"text_{doc_id}",
                            "content_type": metadata.get("content_type", "text"),
                            "source": metadata.get("source", "unknown"),
                            **metadata
                        }
                    }

                    # Check if it's a table based on content_type or content pattern
                    is_table = "table" in metadata.get(
                        "content_type", "").lower()

                    # Fallback: detect table-like content (simple heuristic)
                    if not is_table and not metadata.get("content_type"):
                        # Check for table-like patterns: lines with | separators
                        lines = content_str.strip().split('\n')
                        if len(lines) >= 2:  # At least header and one row
                            # Check if multiple lines contain | characters
                            table_lines = [
                                line for line in lines if '|' in line and line.count('|') >= 2]
                            if len(table_lines) >= 2:  # Header + at least one data row
                                is_table = True

                    if is_table:
                        tables.append(content_item)
                    else:
                        texts.append(content_item)

        return {"images": b64_images, "texts": texts, "tables": tables}

    @staticmethod
    def build_prompt(kwargs):
        docs_by_type = kwargs["context"]
        user_question = kwargs["question"]

        context_text = ""

        # Process texts (they are now ContentItem objects)
        if len(docs_by_type["texts"]) > 0:
            context_text += "Text Content:\n"
            for text_item in docs_by_type["texts"]:
                content_text = text_item["content"]
                context_text += content_text + "\n"
            context_text += "\n"

        # Process tables (they are now ContentItem objects)
        if len(docs_by_type.get("tables", [])) > 0:
            context_text += "Table Content:\n"
            for table_item in docs_by_type["tables"]:
                content_text = table_item["content"]
                context_text += content_text + "\n"
            context_text += "\n"

        # Construct prompt with context (including images)
        prompt_template = f"""
            Answer the question based only on the following context, which includes text, tables, and images (if present).

            Context: {context_text}

            Question: {user_question}
            """

        prompt_content = [{"type": "text", "text": prompt_template}]

        # Add images (they are now ContentItem objects)
        if len(docs_by_type["images"]) > 0:
            for image_item in docs_by_type["images"]:
                image_content = image_item["content"]
                prompt_content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_content}"},
                })

        return ChatPromptTemplate.from_messages([HumanMessage(content=prompt_content)])

    async def answer_question(self, question: str) -> Dict[str, Any]:
        """
        Args:
        question: The question to answer

        Returns:
        Dictionary containing the answer and relevant context
        """
        try:
            docs = await self.retriever._aget_relevant_documents(
                query=question, run_manager=self.tracer)

            reranked_docs = self._apply_reranking(
                docs=docs, query=question, k=10)

            # Convert the list to a Runnable that returns the list
            docs_runnable = RunnableLambda(lambda _: reranked_docs)

            # Response with sources
            chain_with_sources = {
                "context": docs_runnable | RunnableLambda(self.parse_docs),
                "question": RunnablePassthrough(),
            } | RunnablePassthrough().assign(
                response=(
                    RunnableLambda(self.build_prompt)
                    | self.llm
                    | StrOutputParser()
                )
            )

            response = await chain_with_sources.ainvoke(input=question, config={"callbacks": [self.tracer]})

            return {
                "answer": response['response'],
                "context": response['context']
            }

        except Exception as e:
            print(f"Error during chain invocation: {e}")
            return {
                "answer": "I apologize, but I'm currently experiencing technical difficulties. Both primary and fallback services are unavailable. Please try again later.",
                "context": {"images": [], "tables": [], "texts": []}
            }
