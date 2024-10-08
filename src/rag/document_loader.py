import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain.schema.document import Document

from src.rag.indexer import load_embedding_model, EmbeddingModelSource


def recursive_chunk_documents(documents):
    try:
        chunker = RecursiveCharacterTextSplitter(chunk_size=256,
                                                 chunk_overlap=30,
                                                 length_function=len,
                                                 is_separator_regex=False)
        return chunker.split_documents(documents)
    except Exception as e:
        print(str(e))
        raise Exception("Failed to chunk documents")


def recursive_chunk_text(text_content: list[str], metadata: list[dict] = []):
    try:
        chunker = RecursiveCharacterTextSplitter(chunk_size=256,
                                                 chunk_overlap=64,
                                                 length_function=len,
                                                 is_separator_regex=False)
        return chunker.create_documents(text_content, metadatas=metadata)
    except Exception as e:
        print(str(e))
        raise Exception("Failed to chunk documents")


def semantic_chunk_documents(documents: list[Document]):
    try:
        embed = load_embedding_model(EmbeddingModelSource.OPEN_AI)
        chunker = SemanticChunker(embed)
        return chunker.split_documents(documents)
    except Exception as e:
        print(str(e))
        raise Exception("Failed to chunk documents")


def semantic_chunk_text(text_content: str, metadata: list[dict] = []):
    try:
        embed = load_embedding_model(EmbeddingModelSource.OPEN_AI)
        chunker = SemanticChunker(embed)
        return chunker.create_documents([text_content], metadatas=metadata)
    except Exception as e:
        print(str(e))
        raise Exception("Failed to chunk documents")


def load_file_template(filename: str):
    try:
        prompt_text = ""
        file_path = os.path.join("templates", filename)
        with open(file_path, 'r') as file:
            prompt_text = file.read()
        return prompt_text
    except Exception as e:
        print(str(e))
        raise Exception("Failed to load file template")
