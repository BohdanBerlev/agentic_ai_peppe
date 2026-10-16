from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Agentic AI Software Company"

    llm_provider: Literal["ollama", "openai_compatible", "google"] = "ollama"
    llm_model: str = "qwen3:4b"
    llm_base_url: str = "http://localhost:11434"
    llm_api_key: str = ""
    llm_temperature: float = 0.0
    llm_timeout_seconds: float = Field(default=120.0, gt=0)
    llm_max_output_tokens: int = Field(default=768, gt=0)

    embedding_provider: Literal["ollama", "openai_compatible"] = "ollama"
    embedding_model: str = "nomic-embed-text"
    embedding_base_url: str = "http://localhost:11434"
    embedding_api_key: str = ""

    database_url: str = (
        "postgresql://agentic:agentic_dev_only@localhost:5432/agentic_company"
    )
    langchain_postgres_url: str = (
        "postgresql+psycopg://agentic:agentic_dev_only@localhost:5432/agentic_company"
    )

    trace_file: str = "logs/RUN_ID.jsonl"
    cost_call_base_credits: float = 1.0
    cost_runtime_credits_per_second: float = 0.01
    cost_input_credits_per_1k_tokens: float = 0.02
    cost_output_credits_per_1k_tokens: float = 0.04


@lru_cache
def get_settings() -> Settings:
    return Settings()
