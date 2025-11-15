from pydantic_settings import BaseSettings
from typing import List
# Hello from Config file

#BaseSEttings automatically loads environmnet variables
class Settings(BaseSettings):
    PROJECT_NAME:str"Assymetric Seperator API"
    VERSION:str="1.0.0"
    API_V1_PREFIX:str="/api"
    #server settings
    HOST:str="0.0.0.0"
    PORT: int = 8000
    DEBUG: bool= True

    #Database settings
    DATABASE_URL:str="postgresql://separator_user:seperator_pass@localhost:5432/seperator_db"

    #JWT Settings
    SECRET_KEY: str="Ptms2304"
    ALGORITHM: str="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int=30

    #CORS Settings
    ALLOWED_ORIGINS: List[str]=["*"]

    class Config:
        env_file=".env"
        case_sensitive=True
settings= Settings()