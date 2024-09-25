import os
from functools import lru_cache

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    LLM: str = "gpt-4o-mini"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    EMBEDDING_LENGTH: int = 1536

    OUTPUT_DEBUG: bool = True
    OUTPUT_DIR: str = "output"

    OPTIONS: dict = {
        "page-size": "A4",
        "margin-top": "0.75in",
        "margin-right": "0.75in",
        "margin-bottom": "0.75in",
        "margin-left": "0.75in",
        "encoding": "UTF-8",
        "no-outline": None,
        "enable-local-file-access": None,
    }

    model_config = ConfigDict(
        env_file=".env" if os.getenv("ENVIRONMENT") != "production" else None
    )


@lru_cache()
def get_settings():
    return Settings()
