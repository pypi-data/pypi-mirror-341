from pydantic import Field, PositiveInt
from pydantic_settings import BaseSettings


class DownloadConfig(BaseSettings):
    max_concurrency: PositiveInt = Field(default=10, env="DOWNLOAD_MAX_CONCURRENCY")
    base_timeout: PositiveInt = Field(default=30, env="DOWNLOAD_BASE_TIMEOUT")
    retry_attempts: PositiveInt = Field(default=3, env="DOWNLOAD_RETRY_ATTEMPTS")
    chunk_size: PositiveInt = Field(default=1048576, env="DOWNLOAD_CHUNK_SIZE")  # 1MB

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
