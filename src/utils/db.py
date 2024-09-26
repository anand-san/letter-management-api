from langchain_chroma import Chroma
from src.rag.indexer import load_embedding_model, EmbeddingModelSource
from langchain.schema.document import Document
from src.utils.get_env import get_env_var
import os
import shutil


CHROMA_PATH = get_env_var("CHROMA_PATH")


def get_chroma_instance():
    embeddings = load_embedding_model(EmbeddingModelSource.OLLAMA)
    return Chroma(
        persist_directory=CHROMA_PATH, embedding_function=embeddings
    )


def update_chroma_store(chunks: list[Document]):
    # Calculate Page IDs.
    db = get_chroma_instance()
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Add or Update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    else:
        print("✅ No new documents to add")
    return db


def calculate_chunk_ids(chunks):

    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks


def delete_chroma_store():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
