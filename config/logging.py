from pydantic_settings import BaseSettings, SettingsConfigDict

class LogSettings(BaseSettings):
    '''日志设置'''
    LOG_DIR: str = "logs"
    LOG_DEFAULT_CHANNEL: str = "main"
    LOG_MAX_BYTES: int = 20 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT: int = 7

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")