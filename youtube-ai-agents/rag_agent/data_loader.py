from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import SentenceSplitter
from langchain_ollama import ChatOllama, OllamaEmbeddings
from dotenv import load_dotenv

load_dotenv()

local_llm: ChatOllama = ChatOllama(model="llama3.2")
local_embed: OllamaEmbeddings = OllamaEmbeddings(model="mxbai-embed-large")

EMBED_MODEL = ""
EMBED_DIM = 1024

splitter = SentenceSplitter(chunk_overlap=100, chunk_size=500)


def load_and_chunk_pdf(path: str):
    docs = PDFReader().load_data(file=path)
    text = [d.text for d in docs if getattr(d, "text", None)]
    chunks = []
    for t in text:
        chunks.extend(splitter.split_text(t))
    return chunks


def embed_texts(texts: list[str]) -> list[list[float]]:
    embeded_docs = local_embed.embed_documents(texts=texts)
    return embeded_docs
