from pydantic import computed_field, field_validator
import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config: SettingsConfigDict = SettingsConfigDict(  # type: ignore
        env_file=".env", enable_decoding=False, extra="allow"
    )

    ZOTERO_ID: str
    ZOTERO_KEY: str
    ARXIV_QUERY: str
    SMTP_SERVER: str
    SMTP_PORT: int
    SENDER: str
    RECEIVERS: list[str]

    @field_validator("RECEIVERS", mode="before")
    def validate_receivers(cls, value: str) -> list[str]:
        if not value:
            raise ValueError("RECEIVERS cannot be empty")
        return [x.strip() for x in value.split(",") if x.strip() != ""]

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
