"""
資料庫基礎配置
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from ..core.config import settings

# 創建資料庫引擎
engine = create_engine(
    settings.DATABASE_URL,
    # 針對 SQLite 的特殊設定
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# 創建會話工廠
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 創建基礎類
Base = declarative_base()

def get_db():
    """
    獲取資料庫會話的依賴函數
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()