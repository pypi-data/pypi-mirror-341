from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "DEBUG"
    GRPC_SERVER: str = "localhost:50051"

    class Config:
        env_file = ".env"
        case_sensitive = True

# Instancia global
settings = Settings()