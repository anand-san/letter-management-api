from pymilvus import Collection, utility
from langchain.schema.document import Document
from strawberry.types import Info

from src.db.milvus.schema import get_milvus_documents_collection
from src.db.milvus.utils import open_milvus_connection, embed_documents, close_milvus_connection, create_document_chunk_ids


def update_vector_store(chunked_documents: list[Document], user_id: str):
    try:
        open_milvus_connection()

        if (len(chunked_documents) == 0):
            return

        chunks_with_ids = create_document_chunk_ids(chunked_documents)
        collection = get_milvus_documents_collection()
        existing_ids = set()

        if collection.num_entities > 0:
            search_expr = f"document_id == '{chunked_documents[0].metadata["source"]}'"
            existing_items = collection.query(
                expr=search_expr, output_fields=["chunk_id"])
            existing_ids = set(item["chunk_id"] for item in existing_items)

        new_chunks: list[Document] = []
        for chunk in chunks_with_ids:
            if chunk.metadata["id"] not in existing_ids:
                new_chunks.append(chunk)

        if len(new_chunks):
            vectors = embed_documents(new_chunks)

            data = [
                {
                    "user_id": user_id,
                    "document_id": new_chunks[i].metadata["source"],
                    "chunk_id": new_chunks[i].metadata["id"],
                    "embedding": vectors[i],
                    "content": new_chunks[i].page_content,
                    "document_metadata": new_chunks[i].metadata
                }
                for i in range(len(vectors))
            ]

            collection.insert(data=data)
            collection.flush()
    except Exception as e:
        print(str(e))
        raise Exception("Error updating Store")
    finally:
        close_milvus_connection()


def delete_vector_store(user_id: str):
    try:
        open_milvus_connection()
        collection = Collection("documents")
        collection.load()

        collection.delete(expr=f"user_id == '{user_id}'")
        collection.flush()

    except Exception as e:
        print(str(e))
        raise Exception("Error deleting Store")
    finally:
        close_milvus_connection()


def search_user_documents_vector(query_vector, user_id, top_k=8):
    try:

        open_milvus_connection()
        collection = Collection("documents")
        collection.load()

        search_params = {
            "metric_type": "L2",
            "params": {"nprobe": 10},
        }

        results = collection.query(
            data=[query_vector],
            anns_field="embedding",
            param=search_params,
            limit=top_k,
            expr=f"user_id == '{user_id}'",
            output_fields=["content"]
        )

        if (len(results) != 0):
            return "\n\n---\n\n".join([doc["content"] for doc in results])
        else:
            return ""

    except Exception as e:
        raise Exception(f"Error looging up store {str(e)}")
    finally:
        close_milvus_connection()
