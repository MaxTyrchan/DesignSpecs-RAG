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

    def __init__(self):
        self.text_item = "text_item"

    def embed_pdf(self, partitioned_data, retriever: MultiVectorRetriever):
        try:
            # Add texts
            doc_ids = [str(uuid.uuid4()) for _ in partitioned_data["texts"]]
            summary_texts = [
                Document(page_content=summary, metadata={retriever.id_key: doc_ids[i], self.text_item: partitioned_data["texts"][i]}) for i, summary in enumerate(partitioned_data["texts_summaries"])
            ]
            retriever.vectorstore.add_documents(summary_texts)
            retriever.docstore.mset(
                list(zip(doc_ids, partitioned_data["texts"])))

            # Add tables
            table_ids = [str(uuid.uuid4()) for _ in partitioned_data["tables"]]
            summary_tables = [
                Document(page_content=summary, metadata={retriever.id_key: table_ids[i]}) for i, summary in enumerate(partitioned_data["tables_summaries"])
            ]
            retriever.vectorstore.add_documents(summary_tables)
            retriever.docstore.mset(
                list(zip(table_ids, partitioned_data["tables"])))

            # Add image summaries
            img_ids = [str(uuid.uuid4()) for _ in partitioned_data["images"]]
            summary_img = [
                Document(page_content=summary, metadata={retriever.id_key: img_ids[i]}) for i, summary in enumerate(partitioned_data["images_summaries"])
            ]
            retriever.vectorstore.add_documents(summary_img)
            retriever.docstore.mset(
                list(zip(img_ids, partitioned_data["images"])))
        except Exception as e:
            raise Exception(f"Error embedding document: {e}")
