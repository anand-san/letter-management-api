import strawberry
from strawberry.types import Info
from enum import Enum

from src.db.milvus.operations import update_vector_store, delete_vector_store
from src.rag.document_loader import recursive_chunk_documents, load_docs_from_directory, semantic_chunk_documents
from src.rag.retriever import retrieve_documents
from src.utils.get_env import get_env_var


@strawberry.type
class RAGResult:
    result: str


@strawberry.enum
class ChunkStrategy(Enum):
    SEMANTIC = "semantic"
    RECURSIVE = "recursive"


class RagException(Exception):
    def __init__(self, message):
        super().__init__(message)


@strawberry.type
class Query:
    @strawberry.field
    async def get_response(self, query: str, info: Info) -> RAGResult:
        try:
            user_id = info.context['user']['id']
            result = await retrieve_documents(query, user_id)
            return RAGResult(result=result)
        except Exception as e:
            raise RagException(str(e))

    @strawberry.field
    async def get_me(self, info: Info) -> RAGResult:
        try:
            user = info.context["user"]
            return RAGResult(result=f"{user}")
        except Exception as e:
            raise RagException(str(e))


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def update_store(self, chunk_strategy: ChunkStrategy, info: Info) -> RAGResult:
        try:
            user_id = info.context['user']['id']

            DOCUMENTS_DIR = get_env_var("DOCUMENTS_DIR")
            documents = load_docs_from_directory(DOCUMENTS_DIR)
            chunked_documents = []
            if chunk_strategy == ChunkStrategy.SEMANTIC:
                chunked_documents = semantic_chunk_documents(documents)
            elif chunk_strategy == ChunkStrategy.RECURSIVE:
                chunked_documents = recursive_chunk_documents(documents)
            else:
                raise ValueError("Unknown chunk strategy")

            update_vector_store(chunked_documents, user_id)
            return RAGResult(result="Store updated")
        except ValueError as e:
            raise Exception(e)
        except Exception as e:
            raise RagException(e)

    @strawberry.mutation
    async def delete_store(self, info: Info) -> RAGResult:
        try:
            user_id = info.context['user']['id']

            delete_vector_store(user_id=user_id)
            return RAGResult(result="Store deleted")
        except Exception as e:
            raise RagException(str(e))
