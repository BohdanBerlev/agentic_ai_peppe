from typing import Any

from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from src.app.settings import Settings, get_settings


def get_chat_model(settings: Settings | None = None) -> Any:
    """Return the configured LangChain chat-model abstraction.

    Team agents should depend on this factory (or an evolved equivalent), not
    directly on Ollama or ICC-specific code.
    """
    settings = settings or get_settings()

    if settings.llm_provider == "ollama":
        return ChatOllama(
            model=settings.llm_model,
            base_url=settings.llm_base_url,
            temperature=settings.llm_temperature,
            client_kwargs={"timeout": settings.llm_timeout_seconds},
            num_predict=settings.llm_max_output_tokens,
        )

    if settings.llm_provider == "openai_compatible":
        # Many self-hosted OpenAI-compatible services support Chat Completions
        # but not the OpenAI Responses API. Keep the starter on the common path.
        return ChatOpenAI(
            model=settings.llm_model,
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key or "not-required",
            temperature=settings.llm_temperature,
            timeout=settings.llm_timeout_seconds,
            max_tokens=settings.llm_max_output_tokens,
            max_retries=0,
            stream_usage=False,
            use_responses_api=False,
        )

    raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")


def get_embeddings(settings: Settings | None = None) -> Any:
    """Return the configured embedding-model abstraction for later RAG work."""
    settings = settings or get_settings()

    if settings.embedding_provider == "ollama":
        return OllamaEmbeddings(
            model=settings.embedding_model,
            base_url=settings.embedding_base_url,
        )

    if settings.embedding_provider == "openai_compatible":
        return OpenAIEmbeddings(
            model=settings.embedding_model,
            base_url=settings.embedding_base_url,
            api_key=settings.embedding_api_key or "not-required",
        )

    raise ValueError(
        f"Unsupported embedding provider: {settings.embedding_provider}"
    )
