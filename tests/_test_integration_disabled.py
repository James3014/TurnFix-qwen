"""
集成測試
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.main import app
from backend.database.base import Base, get_db
from backend.models.symptom import Symptom
from backend.models.practice_card import PracticeCard
from backend.database.models import SymptomPracticeMapping
from backend.database.repositories import SymptomRepository, PracticeCardRepository, SymptomPracticeMappingRepository


# 創建測試數據庫
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 重寫依賴項以使用測試數據庫
def override_get_db():
    try:
        db = TestingSessionLocal()
        # 創建所有表
        Base.metadata.create_all(bind=engine)
        
        # 創建測試數據
        create_test_data(db)
        
        yield db
    finally:
        db.close()


def create_test_data(db):
    """創建測試數據"""
    symptom_repo = SymptomRepository(db)
    practice_repo = PracticeCardRepository(db)
    mapping_repo = SymptomPracticeMappingRepository(db)
    
    # 創建測試症狀
    symptom = Symptom(
        name="重心太後",
        category="技術",
        synonyms=["後坐", "重心不穩", "轉彎後坐"],
        level_scope=["初級", "中級"],
        terrain_scope=["綠線", "藍線"],
        style_scope=["平花", "回轉"]
    )
    created_symptom = symptom_repo.create(symptom)
    
    # 創建測試練習卡
    practice_card1 = PracticeCard(
        name="J型轉彎練習",
        goal="完成外腳承重再過中立",
        tips=["視線外緣", "外腳 70–80%", "中立後換刃"],
        pitfalls="避免提前壓內腳",
        dosage="藍線 6 次/趟 ×3 趟",
        level=["初級", "中級"],
        terrain=["綠線", "藍線"],
        self_check=["是否在換刃前感到外腳壓力峰值？"],
        card_type="技術"
    )
    
    practice_card2 = PracticeCard(
        name="重心轉移練習",
        goal="改善重心控制",
        tips=["身體前傾", "膝蓋彎曲", "重心保持在腳掌中心"],
        pitfalls="避免重心過後或過前",
        dosage="平地 10 次 ×3 組",
        level=["初級", "中級"],
        terrain=["綠線"],
        self_check=["重心是否能穩定在腳掌中心？"],
        card_type="基礎"
    )
    
    created_card1 = practice_repo.create(practice_card1)
    created_card2 = practice_repo.create(practice_card2)
    
    # 創建症狀和練習卡的映射關係
    mapping_repo.create_mapping(created_symptom.id, created_card1.id, 0)
    mapping_repo.create_mapping(created_symptom.id, created_card2.id, 1)


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_root_endpoint():
    """測試根端點"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to TurnFix API"}


def test_health_check():
    """測試健康檢查端點"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_ski_tips_endpoint():
    """測試滑雪技巧建議端點"""
    # 測試正常請求
    response = client.post(
        "/api/v1/ski-tips",
        params={
            "input_text": "轉彎會後坐",
            "level": "初級",
            "terrain": "綠線"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # 驗證響應格式
    assert "status" in data
    assert "recommended_cards" in data
    assert "count" in data
    
    # 驗證狀態
    assert data["status"] == "success"
    
    # 驗證推薦卡片
    assert isinstance(data["recommended_cards"], list)
    assert data["count"] == len(data["recommended_cards"])
    
    # 驗證至少有一張推薦卡片
    assert len(data["recommended_cards"]) >= 1
    
    # 驗證卡片結構
    for card in data["recommended_cards"]:
        assert "id" in card
        assert "name" in card
        assert "goal" in card
        assert "tips" in card
        assert "pitfalls" in card
        assert "dosage" in card
        assert "level" in card
        assert "terrain" in card
        assert "self_check" in card
        assert "card_type" in card


def test_ski_tips_endpoint_without_optional_params():
    """測試不帶可選參數的滑雪技巧建議端點"""
    response = client.post(
        "/api/v1/ski-tips",
        params={
            "input_text": "重心不穩"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # 驗證響應格式
    assert "status" in data
    assert "recommended_cards" in data
    assert "count" in data
    
    # 驗證狀態
    assert data["status"] == "success"


def test_ski_tips_endpoint_with_invalid_input():
    """測試帶無效輸入的滑雪技巧建議端點"""
    response = client.post(
        "/api/v1/ski-tips",
        params={
            "input_text": ""  # 空輸入，應該觸發默認行為
        }
    )
    
    # 測試應該成功，返回默認建議
    assert response.status_code == 200
    data = response.json()
    
    assert "status" in data
    assert data["status"] == "success"
    assert "recommended_cards" in data