from docling.chunking import HybridChunker
import tiktoken
from docling_core.transforms.chunker.tokenizer.openai import OpenAITokenizer

tokenizer = OpenAITokenizer(
    tokenizer=tiktoken.encoding_for_model("gpt-4o"),
    max_tokens=128 * 1024,  # context window length required for OpenAI tokenizers
)

chunker = HybridChunker(
    tokenizer=tokenizer,
    merge_peers=True,  # optional, defaults to True
    )

def chunking(text: str):
    #TODO: Update Chunking Strategy!
    chunk_iter = chunker.chunk(dl_doc=doc)
    chunks = list(chunk_iter)
    chunks_summaries = []
    for chunk in chunks:
        ser_txts = chunker.contextualize(chunk=chunk)
        chunks_summaries.append(ser_txts)
    return chunks, chunks_summaries
