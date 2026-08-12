import uuid
import os
import json
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
      - LangChain can call embed_query and embed_documents
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

    def embed_query(self, text: str):
        """Embed a single query text. Required by LangChain."""
        return self.embeddings.embed_query(text)

    def embed_documents(self, texts):
        """Embed multiple documents. Required by LangChain."""
        return self.embeddings.embed_documents(texts)

    def embed_pdf(self, partitioned_data, retriever: MultiVectorRetriever):
        try:
            # Add texts
            doc_ids = [str(uuid.uuid4()) for _ in partitioned_data["texts"]]
            summary_texts = [Document(page_content=summary, metadata={
                retriever.id_key: doc_ids[i], "content_type": "text"}) for i, summary in enumerate(partitioned_data["texts_summaries"])]
            # "text_meta": partitioned_data["texts"][i].meta}
            texts = [json.dumps(text.export_json_dict()).encode('utf-8')
                     for text in partitioned_data["texts"]]

            retriever.vectorstore.add_documents(summary_texts)
            retriever.docstore.mset(list(zip(doc_ids, texts)))

            # Add tables
            table_ids = [str(uuid.uuid4()) for _ in partitioned_data["tables"]]
            summary_tables = [Document(page_content=summary, metadata={
                retriever.id_key: table_ids[i], "content_type": "table"}) for i, summary in enumerate(partitioned_data["tables_summaries"])]
            # ,"table_meta": partitioned_data["tables"][i].meta
            tables = [json.dumps(table.export_json_dict()).encode('utf-8')
                      for table in partitioned_data["tables"]]

            retriever.vectorstore.add_documents(summary_tables)
            retriever.docstore.mset(list(zip(doc_ids, tables)))

            # Add image summaries
            img_ids = [str(uuid.uuid4()) for _ in partitioned_data["images"]]
            summary_img = [Document(page_content=summary, metadata={
                                    retriever.id_key: img_ids[i], "content_type": "image", }) for i, summary in enumerate(partitioned_data["images_summaries"])]
            images = [img.encode('utf-8')
                      for img in partitioned_data["images"]]

            retriever.vectorstore.add_documents(summary_img)
            retriever.docstore.mset(list(zip(img_ids, images)))
        except Exception as e:
            raise Exception(f"Error embedding document: {e}")
