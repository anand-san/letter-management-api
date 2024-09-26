from enum import Enum
from typing import Union
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_openai.embeddings import OpenAIEmbeddings


class EmbeddingModelSource(Enum):
    HUGGING_FACE = "huggingface"
    OLLAMA = "ollama"
    OPEN_AI = "openai"


class OllamaEmbedModel(Enum):
    NOMIC_EMBED_TEXT = "nomic-embed-text"
    MXBAI_EMBED_LARGE = "mxbai-embed-large"


class OpenAIEmbedModel(Enum):
    TEXT_EMBED_3_SMALL = "text-embedding-3-small"


class ChatModelSource(Enum):
    OLLAMA = "ollama"
    OPEN_AI = "openai"


class OllamaChatModel(Enum):
    LLAMA3 = "llama3"
    NEMOTRON_MINI = "nemotron-mini"
    MISTRAL_NEMO = "mistral-nemo"
    PHI3_MEDIUM = "phi3:medium"


class OpenAIChatModel(Enum):
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4O_LATEST = "gpt-4o-mini-2024-07-18"


LLM_EMBED_MODEL = Union[OllamaEmbedModel, OpenAIEmbedModel]

LLM_CHAT_MODEL = Union[OllamaChatModel, OpenAIChatModel]


def load_embedding_model(type: EmbeddingModelSource = EmbeddingModelSource.OPEN_AI):
    if (type == EmbeddingModelSource.OPEN_AI):

        model_name = OpenAIEmbedModel.TEXT_EMBED_3_SMALL
        return OpenAIEmbeddings(model=model_name.value)

    elif type == EmbeddingModelSource.OLLAMA:

        model_name = OllamaEmbedModel.NOMIC_EMBED_TEXT.value
        return OllamaEmbeddings(model=model_name)

    elif type == EmbeddingModelSource.HUGGING_FACE:
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
        model_kwargs = {'device': 'cpu'}
        encode_kwargs = {'normalize_embeddings': False}
        cache_folder = '.cache/huggingface'
        return HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs,
            cache_folder=cache_folder
        )
    else:
        raise ValueError(f"Unknown embedding model type: {type}")


# def create_custom_index(documents):
#     embeddings = load_embedding_model()
#     document_text_content = [doc.page_content for doc in documents]
#     return embeddings.embed_documents(document_text_content)
