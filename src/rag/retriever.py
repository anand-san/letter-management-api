import json
from langchain.prompts import PromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from src.db.milvus.utils import embed_query
from src.rag.document_loader import load_file_template
from src.rag.indexer import ChatModelSource, LLM_CHAT_MODEL, OllamaChatModel, OpenAIChatModel
from src.db.milvus.operations import search_user_documents_vector
from src.db.firestore import FirestoreManager


class LLMAssistant:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.firestore_manager = FirestoreManager(self.user_id)

    def _find_context_text(self, query: str):
        query_vector = embed_query(query)
        return search_user_documents_vector(query_vector=query_vector, user_id=self.user_id, top_k=2)

    def _prepare_llm_prompt(self, context_text: str, query: str):
        prompt_text = load_file_template("llm_prompt.txt")
        return PromptTemplate.from_template(prompt_text).format(context=context_text, question=query)

    def _summarize_with_llm(self, chat_model: ChatModelSource, model_name: LLM_CHAT_MODEL, prompt):
        if chat_model == ChatModelSource.OPEN_AI:
            if not isinstance(model_name, OpenAIChatModel):
                raise TypeError("Expected model to be of type OpenAIChatModel")
            llm = ChatOpenAI(
                model=model_name.value,
                max_retries=2,
                max_tokens=4000,
                timeout=10,
            )
            aimessage = llm.invoke(prompt)
            self.firestore_manager.save_user_token_usage(
                metadata=aimessage.response_metadata)
            return str(aimessage.content)
        elif chat_model == ChatModelSource.OLLAMA:
            if not isinstance(model_name, OllamaChatModel):
                raise TypeError("Expected model to be of type OllamaChatModel")
            model = Ollama(model=model_name.value)
            return model.invoke(prompt)
        else:
            raise ValueError(f"Unknown chat model source: {chat_model}")

    def _gather_insights_from_llm(self, chat_model: ChatModelSource, model_name: LLM_CHAT_MODEL, prompt):
        if chat_model == ChatModelSource.OPEN_AI:
            if not isinstance(model_name, OpenAIChatModel):
                raise TypeError("Expected model to be of type OpenAIChatModel")
            llm = ChatOpenAI(
                model=model_name.value,
                max_retries=2,
                max_tokens=8000,
                timeout=60,
                temperature=0.5,
                top_p=1,
            )
            json_llm = llm.bind(response_format={"type": "json_object"})
            aimessage = json_llm.invoke(prompt)
            self.firestore_manager.save_user_token_usage(
                metadata=aimessage.response_metadata)
            return str(aimessage.content)
        elif chat_model == ChatModelSource.OLLAMA:
            if not isinstance(model_name, OllamaChatModel):
                raise TypeError("Expected model to be of type OllamaChatModel")
            model = Ollama(model=model_name.value)
            json_llm = model.bind(response_format={"type": "json_object"})
            return json_llm.invoke(prompt)
        else:
            raise ValueError(f"Unknown chat model source: {chat_model}")

    async def retrieve_documents(self, query: str):
        context_text = self._find_context_text(query)
        llm_prompt = self._prepare_llm_prompt(context_text, query)
        llm_summary = self._summarize_with_llm(ChatModelSource.OPEN_AI,
                                               OpenAIChatModel.GPT_4O_MINI, llm_prompt)
        return llm_summary or "I could not find any relevant information"

    async def retrieve_insights_from_assistant(self, document_text: str):
        prompt_text = load_file_template("insights_prompt.txt")
        llm_prompt = [
            SystemMessage(content=prompt_text),
            HumanMessage(content=document_text),
        ]
        insights_json = self._gather_insights_from_llm(ChatModelSource.OPEN_AI,
                                                       OpenAIChatModel.GPT_4O_MINI, llm_prompt)
        try:
            # Parse the JSON response
            insights = json.loads(insights_json)
        except json.JSONDecodeError as e:
            # Handle JSON parsing error
            print(f"JSON parsing error: {e}")
            insights = {}

        return insights or {}
