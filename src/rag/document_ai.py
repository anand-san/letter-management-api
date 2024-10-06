
from google.api_core.client_options import ClientOptions
from google.cloud import documentai
from src.utils.get_env import get_env_var


def ocr_single_file(
    file_content: bytes,
    file_mime_type: str
) -> str | None:
    try:
        GOOGLE_CLOUD_PROJECT_ID = get_env_var("GOOGLE_CLOUD_PROJECT_ID")
        GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_ID = get_env_var(
            "GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_ID")
        GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_REGION = get_env_var(
            "GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_REGION")

        opts = ClientOptions(
            api_endpoint=f"{GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_REGION}-documentai.googleapis.com")

        client = documentai.DocumentProcessorServiceClient(client_options=opts)

        raw_document = documentai.RawDocument(
            content=file_content,
            mime_type=file_mime_type,
        )

        processor_name = f"projects/{GOOGLE_CLOUD_PROJECT_ID}/locations/{
            GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_REGION}/processors/{GOOGLE_CLOUD_DOCUMENT_AI_PROCESSOR_ID}"

        request = documentai.ProcessRequest(
            name=processor_name, raw_document=raw_document)

        result = client.process_document(request=request)

        return result.document.text if result.document else None
    except Exception:
        raise
