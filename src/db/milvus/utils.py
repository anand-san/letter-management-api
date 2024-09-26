from pymilvus import connections
from langchain.schema.document import Document

from src.rag.indexer import load_embedding_model, EmbeddingModelSource
from src.utils.get_env import get_env_var


def embed_documents(documents: list[Document]):
    embeddings = load_embedding_model(EmbeddingModelSource.OPEN_AI)
    text_content = [doc.page_content for doc in documents]
    return embeddings.embed_documents(text_content)


def embed_query(query: str):
    embeddings = load_embedding_model(EmbeddingModelSource.OPEN_AI)
    return embeddings.embed_query(query)


def open_milvus_connection(alias: str = "default"):
    try:
        MILVUS_HOST = get_env_var("MILVUS_HOST")
        MILVUS_PORT = get_env_var("MILVUS_PORT")
        connections.connect(alias, host=MILVUS_HOST, port=MILVUS_PORT)
    except Exception as e:
        print(str(e))


def close_milvus_connection(alias: str = "default"):
    try:
        connections.disconnect(alias)
    except Exception as e:
        print(str(e))


def create_document_chunk_ids(chunks: list[Document]):
    # This will create IDs like "data/document.pdf:6:2"
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
