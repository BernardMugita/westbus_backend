from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    PROJECT_NAME: str = "WestBus Server"
    DATABASE_URL: str
    SECRET_KEY: str

settings = Settings()