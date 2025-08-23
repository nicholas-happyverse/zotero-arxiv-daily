from pydantic import computed_field
import os
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    ZOTERO_ID: str
    ZOTERO_KEY: str
    ARXIV_QUERY: str
    SMTP_SERVER: str
    SMTP_PORT: int
    SENDER: str
    RECEIVER: str
    SMTP_PASSWORD: str
    SMTP_USERNAME: str | None = None
    OPENAI_API_KEY: str = ""
    ZOTERO_IGNORE: str = ""
    SEND_EMPTY: bool = True
    MAX_PAPER_NUM: int = 100
    USE_LLM_API: bool = False
    OPENAI_API_BASE: str = "https://api.openai.com/v1"
    MODEL_NAME: str = "gpt-5-nano"
    LANGUAGE: str = "English"
    DEBUG: bool = False


settings = Config()  # type: ignore
