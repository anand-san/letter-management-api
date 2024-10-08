from firebase_admin import storage
from google.cloud import datastore
from google.cloud.datastore import Entity, Key
from datetime import datetime, timezone

from src.utils.get_env import get_env_var


def upload_document_to_bucket(file_id: str, file, file_type: str, user_id: str):
    try:
        GOOGLE_CLOUD_STORAGE_BUCKET = get_env_var('GOOGLE_CLOUD_STORAGE_BUCKET')
        bucket = storage.bucket(GOOGLE_CLOUD_STORAGE_BUCKET)

        blob = bucket.blob(f"documents/{user_id}/{file_id}")

        blob.upload_from_string(
            file,
            content_type=file_type
        )

        return blob.public_url
    except Exception:
        raise Exception("Failed to save document")


def save_document_metadata(file_id: str, file_name: str, file_type: str, file_url: str, user_id: str) -> Key:
    try:
        client = datastore.Client()

        # Create a new entity
        key = client.key('User', user_id, 'Document')
        entity = Entity(key)

        # Set the entity properties
        entity.update({
            'stored_file_name': file_id,
            'file_type': file_type,
            'original_file_name': file_name,
            'file_url': file_url,
            'extracted_text': '',
            'upload_date': datetime.now(timezone.utc)
        })

        client.put(entity)

        return entity.key  # type: ignore
    except Exception:
        raise Exception("Failed to save document metadata")


def update_extracted_text(user_id: str, document_key: Key, extracted_text: str) -> Key:
    try:
        client = datastore.Client()

        key = client.key('User', user_id, 'Document', document_key.id)
        entity = client.get(key)

        if not entity:
            raise ValueError(f"No document found for user {
                             user_id} with key {document_key.id}")

        entity['extracted_text'] = extracted_text
        client.put(entity)
        return entity.key  # type: ignore
    except Exception as e:
        print(str(e))
        raise Exception("Failed to update extracted text from document")
