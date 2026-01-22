from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    #БД
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/advertisements"

    API_V1_PREFIX: str = ""
    PROJECT_NAME: str = "Advertisement Service"
    VERSION: str = "1.0.0"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()