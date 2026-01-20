from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    aws_region: str = "us-east-1"
    bedrock_embed_model_id: str
    bedrock_chat_model_id: str

    database_url: str
    top_k: int = 5
    chunk_size: int = 800
    chunk_overlap: int = 120
    max_context_chars: int = 6000

settings = Settings()
