"""
測試配置文件
提供測試所需的 fixtures
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from backend.database.base import Base
from backend.main import app

# 導入所有模型以確保 Base.metadata 包含它們
from backend.models.symptom import Symptom
from backend.models.practice_card import PracticeCard
from backend.models.session import Session as SessionModel
from backend.models.symptom_practice_mapping import SymptomPracticeMapping
from backend.models.practice_card_feedback import PracticeCardFeedback
from backend.models.session_feedback import SessionFeedback
from backend.models.user import User


@pytest.fixture(scope="function")
def test_db():
    """
    創建測試資料庫 fixture
    每個測試函數使用獨立的內存資料庫
    """
    # 使用 SQLite in-memory 資料庫，StaticPool 確保所有連接共享同一個數據庫
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    # 創建所有表格
    Base.metadata.create_all(bind=engine)

    # 創建 session
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    """
    創建測試客戶端 fixture
    自動使用測試資料庫
    """
    from backend.database.base import get_db

    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_symptom_data():
    """症狀測試數據"""
    return {
        "name": "重心太後",
        "category": "技術",
        "synonyms": ["後坐", "重心後移"],
        "level_scope": ["初級", "中級"],
        "terrain_scope": ["綠線", "藍線"],
        "style_scope": ["平花"]
    }


@pytest.fixture
def sample_practice_card_data():
    """練習卡測試數據"""
    return {
        "name": "J型轉彎練習",
        "goal": "完成外腳承重再過中立",
        "tips": ["視線外緣", "外腳 70-80%", "中立後換刃"],
        "pitfalls": "避免提前壓內腳",
        "dosage": "藍線 6 次/趟 ×3 趟",
        "level": ["初級", "中級"],
        "terrain": ["綠線", "藍線"],
        "self_check": ["是否在換刃前感到外腳壓力峰值?"],
        "card_type": "技術"
    }
