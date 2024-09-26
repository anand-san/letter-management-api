from src.rag.document_loader import load_file_template
from src.rag.indexer import ChatModelSource, LLM_CHAT_MODEL, OllamaChatModel, OpenAIChatModel
from src.utils.db import get_chroma_instance
from langchain.prompts import PromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain_openai import ChatOpenAI

index = None


async def initialize_index():
    global index
    if index is None:
        return get_chroma_instance()


def find_context_text(query: str, index, k: int):
    """Finds context matching the query from the vector sotre"""
    if index is None:
        return "Failed to initialize"
    docs = index.similarity_search_with_score(query, k=k)
    return "\n\n---\n\n".join([doc.page_content for doc, _score in docs])


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
        print('response meta:', aimessage.response_metadata)
        return str(aimessage.content)
    elif chat_model == ChatModelSource.OLLAMA:
        if not isinstance(model_name, OllamaChatModel):
            raise TypeError("Expected model to be of type OllamaChatModel")

        model = Ollama(model=model_name.value)
        return model.invoke(prompt)
    else:
        raise ValueError(f"Unknown chat model source: {chat_model}")


async def retrieve_documents(query: str, k: int = 8):
    index = await initialize_index()
    context_text = find_context_text(query, index, k)
    llm_prompt = prepare_llm_prompt(context_text, query)
    print(llm_prompt)
    llm_summary = query_llm(ChatModelSource.OPEN_AI,
                            OpenAIChatModel.GPT_4O_MINI, llm_prompt)
    return llm_summary or "I could not find any relevant information"
