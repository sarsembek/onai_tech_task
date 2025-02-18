import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class Settings(BaseSettings):
    app_name: str = "onai"
    openai_api_key: str
    
    model_config = SettingsConfigDict(env_file="../.env", extra="allow")

settings = Settings()
