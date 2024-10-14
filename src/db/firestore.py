import json
from typing import Dict, Any
from firebase_admin import storage
from google.cloud import datastore
from google.cloud.datastore import Entity, Key
from datetime import datetime, timezone

from src.utils.get_env import get_env_var


class FirestoreManager:
    def __init__(self, user_id: str):
        self.datastore_client = datastore.Client()
        self.storage_bucket = self._get_storage_bucket()
        self.user_id = user_id

    def _get_storage_bucket(self):
        bucket_name = get_env_var('GOOGLE_CLOUD_STORAGE_BUCKET')
        return storage.bucket(bucket_name)

    def upload_document_to_bucket(self, file_id: str, file: Any, file_type: str) -> str:
        try:
            blob = self.storage_bucket.blob(f"documents/{self.user_id}/{file_id}")
            blob.upload_from_string(file, content_type=file_type)
            return blob.public_url
        except Exception as e:
            raise Exception(f"Failed to save document: {str(e)}")

    def save_document_metadata(self, file_id: str, file_name: str, file_type: str, file_url: str) -> Key:
        try:
            key = self.datastore_client.key('User', self.user_id, 'Document')
            entity = Entity(key)
            entity.update({
                'stored_file_name': file_id,
                'file_type': file_type,
                'original_file_name': file_name,
                'file_url': file_url,
                'extracted_text': '',
                'upload_date': datetime.now(timezone.utc)
            })
            self.datastore_client.put(entity)
            return entity.key  # type: ignore
        except Exception as e:
            raise Exception(f"Failed to save document metadata: {str(e)}")

    def update_extracted_text(self, document_key: Key, extracted_text: str) -> Key:
        try:
            print(extracted_text)
            key = self.datastore_client.key(
                'User', self.user_id, 'Document', document_key.id)
            entity = self.datastore_client.get(key)
            if not entity:
                raise ValueError(f"No document found for user {
                                 self.user_id} with key {document_key.id}")
            truncated_text = extracted_text.encode(
                'utf-8')[:1500].decode('utf-8', 'ignore')

            entity['extracted_text'] = truncated_text
            self.datastore_client.put(entity)
            return entity.key  # type: ignore
        except Exception as e:
            raise Exception(f"Failed to update extracted text from document: {str(e)}")

    def save_user_token_usage(self, metadata: Dict[str, Any]) -> None:
        try:
            return
            user_key = self.datastore_client.key('User', self.user_id)
            user_entity = self.datastore_client.get(user_key)
            if not user_entity:
                raise ValueError(f"No user found with id {self.user_id}")
            new_token_usage = {
                'completion_tokens': metadata['token_usage']['completion_tokens'],
                'prompt_tokens': metadata['token_usage']['prompt_tokens'],
                'total_tokens': metadata['token_usage']['total_tokens'],
                'cached_tokens': metadata['token_usage']['prompt_tokens_details']['cached_tokens']
            }

            if 'token_usage' in user_entity:
                current_usage = user_entity['token_usage']
                for key, value in new_token_usage.items():
                    current_usage[key] = current_usage.get(key, 0) + value
            else:
                user_entity['token_usage'] = new_token_usage

            self.datastore_client.put(user_entity)
        except Exception as e:
            raise Exception(f"Failed to save user token usage: {str(e)}")

    def save_document_insights(self, document_key: Key, insights: Dict[str, Any]) -> Key:
        try:
            key = self.datastore_client.key(
                'User', self.user_id, 'Document', document_key.id)
            entity = self.datastore_client.get(key)
            if not entity:
                raise ValueError(f"No document found for user {
                                 self.user_id} with key {document_key.id}")

            entity['insights'] = json.dumps(insights)
            print('saving insight')
            self.datastore_client.put(entity)
            return entity.key  # type: ignore
        except Exception as e:
            raise Exception(f"Failed to save document insights: {str(e)}")

# ... existing code ...
