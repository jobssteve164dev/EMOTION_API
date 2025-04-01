from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 基础配置
    PROJECT_NAME: str = "情感分析引擎"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # MongoDB配置
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "emotion_db"
    
    # 情感分析模型配置
    MODEL_NAME: str = "bert-base-chinese"
    MAX_LENGTH: int = 512
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings() 