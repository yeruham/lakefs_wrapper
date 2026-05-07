from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Server
    port: int = 8000

    # JWT
    jwt_secret: str = "change_me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # MongoDB
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db_name: str = "datasets_db"

    # lakeFS
    lakefs_endpoint: str = "http://localhost:8001"
    lakefs_access_key: str = "AKIAJPCO7MT4PTCZNY5Q"


@lru_cache
def get_settings() -> Settings:
    return Settings()