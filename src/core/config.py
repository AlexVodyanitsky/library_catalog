from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    STORAGE_TYPE: str = ""  # file, db, jsonbin
    JSONBIN_API_KEY: str = ""
    JSONBIN_BIN_ID: str = ""
    DATABASE_URL: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
