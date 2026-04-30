from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openai_api_key: str = ""
    anthropic_api_key: str = ""
    embedding_model: str = "all-MiniLM-L6-v2"
    vector_db_path: str = "storage/vector_index"
    log_level: str = "INFO"
    env: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
