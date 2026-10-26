import os
from functools import lru_cache
from typing import Literal

from pydantic import AliasChoices, Field, model_validator
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
    llm_api_key: str = Field(
        default="",
        validation_alias=AliasChoices(
            "llm_api_key",
            "LLM_API_KEY",
            "GEMINI_API_KEY",
            "gemini_api_key",
            "GOOGLE_API_KEY",
            "google_api_key",
            "AI_STUDIO_API_KEY",
            "ai_studio_api_key",
        ),
    )
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

    @model_validator(mode="after")
    def resolve_api_keys(self) -> "Settings":
        if not self.llm_api_key:
            env_key = (
                os.getenv("LLM_API_KEY")
                or os.getenv("GEMINI_API_KEY")
                or os.getenv("GOOGLE_API_KEY")
                or os.getenv("AI_STUDIO_API_KEY")
                or ""
            )
            if env_key:
                self.llm_api_key = env_key
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
