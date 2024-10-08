from firebase_admin import storage
from google.cloud import datastore
from google.cloud.datastore import Entity
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


def save_document_metadata(file_id: str, file_name: str, file_type: str, file_url: str, user_id: str, ):
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
            'extracted_text': 'Not-Processed',
            'upload_date': datetime.now(timezone.utc)
        })

        client.put(entity)

        return entity.key
    except Exception:
        raise Exception("Failed to save document metadata")
