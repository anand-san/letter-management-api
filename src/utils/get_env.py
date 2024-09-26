import os


def get_env_var(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        match key:
            case "DOCUMENTS_DIR":
                value = "documents"
            case "CHROMA_PATH":
                value = ".cache/chroma"
            case "CHROMA_PATH":
                value = ".cache/chroma"
            case "OLLAMA_LLM_MODEL":
                value = "nemotron-mini"
            case _:
                value = None
        raise ValueError(f"Missing required environment variable: {key}")
    return value
