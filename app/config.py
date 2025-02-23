import os
from typing import Annotated, TypeVar
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

T = TypeVar("T")
ExcludedField = Annotated[T, Field(exclude=True)]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env")
    app_name: str = "onai"
    OPENAI_API_KEY: ExcludedField[str]

settings = Settings()