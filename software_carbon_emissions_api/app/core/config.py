from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Software Carbon Emissions API"
    VERSION: str = "1.0.0"
    GITHUB_TOKEN: str = ""

    # This tells Pydantic to look for a .env file at the root level
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
