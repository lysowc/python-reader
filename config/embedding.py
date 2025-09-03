from pydantic_settings import BaseSettings, SettingsConfigDict


class EmbeddingSettings(BaseSettings):
    """嵌入模型设置"""

    EMBEDDING_MODEL_PATH: str = (
        "/mnt/39c11858-dd64-43db-b572-f6d164e03458/embedding/bge-m3"
    )

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
