from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "CopMap PoC"
    ENV: str = "dev"
    CORS_ORIGINS: str = "http://localhost:3000"

    DATA_DIR: str = "./data"
    SQLITE_PATH: str = "./data/copmap.db"

    CHROMA_DIR: str = "./data/chroma"
    CHROMA_COLLECTION: str = "copmap_docs"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    LLM_MODE: str = "off"  # off|groq
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.1-8b-instant"

    def cors_list(self) -> List[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


settings = Settings()
