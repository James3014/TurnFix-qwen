"""
API 端點測試

測試 API 端點的功能
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.main import app
from backend.database.base import Base
from backend.models.symptom import Symptom
from backend.models.practice_card import PracticeCard

@pytest.fixture(scope="module")
def test_client():
    """創建測試客戶端"""
    # 使用內存數據庫進行測試
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    def override_get_db():
        try:
            db = SessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_get_ski_tips_endpoint(test_client):
    """測試獲取滑雪技巧建議端點"""
    response = test_client.post(
        "/api/v1/ski-tips",
        json={
            "input_text": "轉彎會後坐",
            "level": "初級",
            "terrain": "綠線",
            "style": "平花"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "status" in data
    assert "recommended_cards" in data
    assert "count" in data

def test_identify_symptom_endpoint(test_client):
    """測試症狀辨識端點"""
    response = test_client.post(
        "/api/v1/symptoms/identify",
        json={
            "input_text": "轉彎會後坐"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "status" in data
    assert "symptom" in data
    assert data["status"] == "success"

def test_get_followup_needs_endpoint(test_client):
    """測試獲取追問需求端點"""
    response = test_client.post(
        "/api/v1/followup-needs",
        json={
            "input_text": "轉彎會後坐",
            "level": "初級",
            "terrain": "綠線",
            "style": "平花"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "status" in data
    assert "followup_needs" in data
    assert data["status"] == "success"

def test_crud_operations(test_client):
    """測試基本 CRUD 操作"""
    # 創建症狀
    response = test_client.post(
        "/api/v1/symptoms",
        json={
            "name": "測試症狀",
            "category": "技術",
            "synonyms": ["測試", "示例"],
            "level_scope": ["初級", "中級"],
            "terrain_scope": ["綠線", "藍線"],
            "style_scope": ["平花"]
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    symptom_id = data["symptom"]["id"]
    
    # 獲取症狀
    response = test_client.get(f"/api/v1/symptoms/{symptom_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    
    # 創建練習卡
    response = test_client.post(
        "/api/v1/practice-cards",
        json={
            "name": "測試練習卡",
            "goal": "測試目標",
            "tips": ["要點1", "要點2"],
            "pitfalls": "常見錯誤",
            "dosage": "建議次數",
            "level": ["初級", "中級"],
            "terrain": ["綠線", "藍線"],
            "self_check": ["自我檢查點1"],
            "card_type": "技術"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    practice_card_id = data["practice_card"]["id"]
    
    # 獲取練習卡
    response = test_client.get(f"/api/v1/practice-cards/{practice_card_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    
    # 創建症狀練習卡映射
    response = test_client.post(
        "/api/v1/symptom-practice-mappings",
        json={
            "symptom_id": symptom_id,
            "practice_id": practice_card_id,
            "order": 0
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    
    # 獲取症狀練習卡
    response = test_client.get(f"/api/v1/symptoms/{symptom_id}/practice-cards")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    
    # 測試回饋端點
    # 創建會話回饋
    response = test_client.post(
        "/api/v1//session-feedback",
        json={
            "session_id": 1,
            "rating": "applicable",
            "feedback_text": "測試回饋",
            "feedback_type": "immediate"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    
    # 創建練習卡回饋
    response = test_client.post(
        "/api/v1//practice-card-feedback",
        json={
            "session_id": 1,
            "practice_id": practice_card_id,
            "rating": 5,
            "feedback_text": "測試練習卡回饋",
            "is_favorite": True
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    feedback_id = data["feedback"]["id"]
    
    # 切換最愛狀態
    response = test_client.put(
        f"/api/v1//practice-card-feedback/{feedback_id}/favorite",
        json={"is_favorite": False}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    
    # 獲取最愛練習卡
    response = test_client.get("/api/v1//user/favorite-cards")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    
    # 測試分析端點
    response = test_client.get("/api/v1//admin/feedback-analytics/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    
    response = test_client.get(f"/api/v1//admin/feedback-analytics/practice-cards/{practice_card_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    
    # 測試最愛清單端點
    response = test_client.post(
        f"/api/v1//user/favorite-cards/{practice_card_id}",
        json={
            "is_favorite": True,
            "session_id": 1
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    
    response = test_client.delete(
        f"/api/v1//user/favorite-cards/{practice_card_id}",
        json={"session_id": 1}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"

def test_health_check_endpoint(test_client):
    """測試健康檢查端點"""
    response = test_client.get("/api/v1//health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"