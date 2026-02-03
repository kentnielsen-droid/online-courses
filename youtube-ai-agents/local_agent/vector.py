from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

df = pd.read_excel("data/Q3-2025-financial-workbook.xlsx")
embeddings: OllamaEmbeddings = OllamaEmbeddings(model="mxbai-embed-large")

db_location = "data/chrome_langchain_db"
add_documents = not os.path.exists(db_location)

if add_documents:
    documents: list = []
    ids: list = []

    for i, row in df.iterrows():
        document: Document = Document(page_content=str(row), id=str(i))
        ids.append(str(i))
        documents.append(document)

vectore_store: Chroma = Chroma(
    collection_name="financial_reports",
    persist_directory=db_location,
    embedding_function=embeddings,
)

if add_documents:
    vectore_store.add_documents(documents=documents, ids=ids)

retriever = vectore_store.as_retriever(search_kwargs={"k": 10})
