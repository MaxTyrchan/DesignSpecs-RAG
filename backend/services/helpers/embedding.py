import uuid
import os
from langchain.schema.document import Document
from langchain_openai import AzureOpenAIEmbeddings
from dotenv import load_dotenv
from langchain.retrievers.multi_vector import MultiVectorRetriever

# Load environment variables
load_dotenv()


class Embedding:
    """
    Wraps AzureOpenAIEmbeddings (or any LangChain embedder) so that:
      - Chroma can call .name()
      - Chroma can call (input=[...]) to get embeddings
    """

    def __init__(self, embeddingModel):
        self.embeddings = embeddingModel
        self.text_item = "text_item"

    def __call__(self, input):
        # This method is called by Chroma to get embeddings
        return self.embeddings.embed_documents(input)

    def name(self):
        # Required by Chroma
        return "AzureOpenAIEmbeddings"

    def embed_documents(self, texts):
        # Delegate to the underlying embeddings model
        return self.embeddings.embed_documents(texts)

    def embed_query(self, text):
        # Delegate to the underlying embeddings model
        return self.embeddings.embed_query(text)

    def embed_pdf(self, partitioned_data, retriever: MultiVectorRetriever):
        try:
            # Add texts
            doc_ids = [str(uuid.uuid4()) for _ in partitioned_data["texts"]]
            summary_texts = [
                Document(page_content=summary, metadata={
                    retriever.id_key: doc_ids[i],
                    "content_type": "text",
                    self.text_item: partitioned_data["texts"][i]
                }) for i, summary in enumerate(partitioned_data["texts_summaries"])
            ]
            retriever.vectorstore.add_documents(summary_texts)
            retriever.docstore.mset(
                list(zip(doc_ids, [text.encode('utf-8') for text in partitioned_data["texts"]])))

            # Add tables
            table_ids = [str(uuid.uuid4()) for _ in partitioned_data["tables"]]
            summary_tables = [
                Document(page_content=summary, metadata={
                    retriever.id_key: table_ids[i],
                    "content_type": "table",
                    "table_content": partitioned_data["tables"][i]
                }) for i, summary in enumerate(partitioned_data["tables_summaries"])
            ]
            retriever.vectorstore.add_documents(summary_tables)
            retriever.docstore.mset(
                list(zip(table_ids, [table.encode('utf-8') for table in partitioned_data["tables"]])))

            # Add image summaries
            img_ids = [str(uuid.uuid4()) for _ in partitioned_data["images"]]
            summary_img = [
                Document(page_content=summary, metadata={
                    retriever.id_key: img_ids[i],
                    "content_type": "image",
                    "image_data": partitioned_data["images"][i]
                }) for i, summary in enumerate(partitioned_data["images_summaries"])
            ]
            retriever.vectorstore.add_documents(summary_img)
            retriever.docstore.mset(
                list(zip(img_ids, [img.encode('utf-8') for img in partitioned_data["images"]])))
        except Exception as e:
            raise Exception(f"Error embedding document: {e}")
