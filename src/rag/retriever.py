from langchain.prompts import PromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain_openai import ChatOpenAI

from src.db.milvus.utils import embed_query
from src.rag.document_loader import load_file_template
from src.rag.indexer import ChatModelSource, LLM_CHAT_MODEL, OllamaChatModel, OpenAIChatModel
from src.db.milvus.operations import search_user_documents_vector
from src.db.postgres.utils import save_user_token_usage


def find_context_text(query: str, user_id: str):
    query_vector = embed_query(query)
    return search_user_documents_vector(query_vector=query_vector, user_id=user_id, top_k=2)


def prepare_llm_prompt(context_text: str, query: str):
    prompt_text = load_file_template("llm_prompt.txt")
    return PromptTemplate.from_template(prompt_text).format(context=context_text, question=query)


def query_llm(chat_model: ChatModelSource, model_name: LLM_CHAT_MODEL, prompt):
    if chat_model == ChatModelSource.OPEN_AI:
        if not isinstance(model_name, OpenAIChatModel):
            raise TypeError("Expected model to be of type OpenAIChatModel")
        llm = ChatOpenAI(
            model=model_name.value,
            max_retries=2,
            # temperature=0,
            max_tokens=4000,
            timeout=10,
        )
        aimessage = llm.invoke(prompt)
        save_user_token_usage(metadata=aimessage.response_metadata)
        return str(aimessage.content)
    elif chat_model == ChatModelSource.OLLAMA:
        if not isinstance(model_name, OllamaChatModel):
            raise TypeError("Expected model to be of type OllamaChatModel")

        model = Ollama(model=model_name.value)
        return model.invoke(prompt)
    else:
        raise ValueError(f"Unknown chat model source: {chat_model}")


async def retrieve_documents(query: str, user_id: str):
    context_text = find_context_text(query, user_id)
    llm_prompt = prepare_llm_prompt(context_text, query)
    llm_summary = query_llm(ChatModelSource.OPEN_AI,
                            OpenAIChatModel.GPT_4O_MINI, llm_prompt)
    return llm_summary or "I could not find any relevant information"
