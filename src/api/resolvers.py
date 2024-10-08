import strawberry
from enum import Enum
import uuid

from strawberry.file_uploads import Upload as UploadFile
from strawberry.types import Info

from src.db.milvus.operations import update_vector_store, delete_vector_store
from src.rag.document_loader import recursive_chunk_documents, semantic_chunk_documents, recursive_chunk_text
from src.rag.retriever import retrieve_documents
from src.rag.document_ai import ocr_single_file
from src.db.firestore import save_document_metadata, upload_document_to_bucket


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
            user_id = info.context['user']['user_id']

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
    async def process_document(self, file: UploadFile, info: Info) -> str:
        try:
            user_id = info.context['user']['user_id']

            file_headers = file.headers  # type: ignore
            file_name = file.filename  # type: ignore
            file_type = file_headers['content-type']  # type: ignore

            file_id = str(uuid.uuid4())
            file_content = await file.read()  # type: ignore

            uploaded_file_url = upload_document_to_bucket(
                file_id=file_id, file=file_content, file_type=file_type, user_id=user_id)

            save_document_metadata(file_id=file_id, file_name=file_name,
                                   file_type=file_type, file_url=uploaded_file_url, user_id=user_id)

            file_text = ocr_single_file(file_content=file_content,
                                        file_type=file_type)

            file_metadata = (
                [{"name": file_name, "mime_type": file_type}])

            chunks = recursive_chunk_text([file_text], metadata=file_metadata)

            update_vector_store(chunks, user_id)

            return "Documents processed"

        except Exception as e:
            print(str(e))
            raise RagException(message="Failed to process provided files")

    @ strawberry.mutation
    async def update_store(self, chunk_strategy: ChunkStrategy, info: Info) -> RAGResult:
        try:
            user_id = info.context['user']['user_id']
            # TODO: Allow users to reset store?
            documents = []
            chunked_documents = []
            if chunk_strategy == ChunkStrategy.SEMANTIC:
                chunked_documents = semantic_chunk_documents(documents)
            elif chunk_strategy == ChunkStrategy.RECURSIVE:
                chunked_documents = recursive_chunk_documents(documents)
            else:
                raise ValueError("Unknown chunk strategy")
            update_vector_store(chunked_documents, user_id)
            return RAGResult(result="Store updated")
        except Exception as e:
            print(str(e))

            raise RagException(message="Could not update store")

    @ strawberry.mutation
    async def delete_store(self, info: Info) -> RAGResult:
        try:
            user_id = info.context['user']['user_id']

            delete_vector_store(user_id=user_id)
            return RAGResult(result="Store deleted")
        except Exception as e:
            raise RagException(str(e))
