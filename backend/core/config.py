"""
應用程式配置管理

管理所有環境配置變數
"""
import os
from typing import Optional

class Settings:
    # 基本設定
    PROJECT_NAME: str = "TurnFix API"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # 資料庫設定
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./turnfix.db")
    DATABASE_ENGINE: str = os.getenv("DATABASE_ENGINE", "sqlite")
    
    # AI 模型設定
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "paraphrase-multilingual-MiniLM-L12-v2")
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "huggingface")
    
    # 向量資料庫設定
    VECTOR_DB_TYPE: str = os.getenv("VECTOR_DB_TYPE", "chroma")
    VECTOR_DB_PATH: str = os.getenv("VECTOR_DB_PATH", "./vector_store")
    
    # Supabase 設定
    SUPABASE_URL: Optional[str] = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY: Optional[str] = os.getenv("SUPABASE_ANON_KEY")
    
    # YouTube API 設定
    YOUTUBE_API_KEY: Optional[str] = os.getenv("YOUTUBE_API_KEY")
    
    # 安全設定
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-default-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # 性能設定
    MAX_RESPONSE_TIME_P95: float = 2.5  # 秒
    
    # 應用程式設定
    MAX_TIPS_PER_CARD: int = 3  # 練習卡要點數量上限
    MAX_SELF_CHECK_PER_CARD: int = 3  # 練習卡自我檢查數量上限
    MIN_PRACTICE_CARDS: int = 3  # 最少建議練習卡數量
    MAX_PRACTICE_CARDS: int = 5  # 最多建議練習卡數量

settings = Settings()