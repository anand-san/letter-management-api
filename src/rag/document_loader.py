import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from rag.indexer import load_embedding_model, EmbeddingModelSource
from langchain.schema.document import Document


def recursive_chunk_documents(documents):
    chunker = RecursiveCharacterTextSplitter(chunk_size=256,
                                             chunk_overlap=30,
                                             length_function=len,
                                             is_separator_regex=False)
    return chunker.split_documents(documents)


def semantic_chunk_documents(documents: list[Document]):
    embed = load_embedding_model(EmbeddingModelSource.OPEN_AI)
    chunker = SemanticChunker(embed)
    return chunker.split_documents(documents)


def load_docs_from_directory(directory: str = "documents"):
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(directory, filename))
            documents.extend(loader.load())
    return documents


def load_file_template(filename: str):
    prompt_text = ""
    file_path = os.path.join("templates", filename)
    with open(file_path, 'r') as file:
        prompt_text = file.read()
    return prompt_text
