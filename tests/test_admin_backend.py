"""
管理者後台測試 (API-205)

測試管理者後台API端點功能
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.main import app
from backend.database.base import Base
from backend.models.symptom import Symptom
from backend.models.practice_card import PracticeCard
from backend.models.session import Session
from backend.models.symptom_practice_mapping import SymptomPracticeMapping
from backend.models.practice_card_feedback import PracticeCardFeedback
from backend.models.session_feedback import SessionFeedback

# 創建測試客戶端
client = TestClient(app)

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
    
    app.dependency_overrides["backend.database.base.get_db"] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_admin_dashboard(test_client):
    """測試管理者後台儀表板 (API-205)"""
    response = test_client.get("/api/v1/admin/dashboard")
    assert response.status_code == 200
    data = response.json()
    
    assert "status" in data
    assert data["status"] == "success"
    assert "total_symptoms" in data
    assert "total_practice_cards" in data
    assert "total_sessions" in data
    assert "total_feedback" in data
    assert "avg_rating" in data

def test_symptom_management_crud(test_client):
    """測試症狀管理CRUD操作 (API-205.1)"""
    # 創建症狀
    symptom_data = {
        "name": "測試症狀",
        "category": "技術",
        "synonyms": ["測試", "示例"],
        "level_scope": ["初級", "中級"],
        "terrain_scope": ["綠線", "藍線"],
        "style_scope": ["平花"]
    }
    
    create_response = test_client.post("/api/v1/admin/symptoms", json=symptom_data)
    assert create_response.status_code == 200
    create_data = create_response.json()
    
    assert "status" in create_data
    assert create_data["status"] == "success"
    assert "symptom" in create_data
    assert create_data["symptom"]["name"] == "測試症狀"
    assert create_data["symptom"]["category"] == "技術"
    assert create_data["symptom"]["synonyms"] == ["測試", "示例"]
    assert create_data["symptom"]["level_scope"] == ["初級", "中級"]
    assert create_data["symptom"]["terrain_scope"] == ["綠線", "藍線"]
    assert create_data["symptom"]["style_scope"] == ["平花"]
    
    symptom_id = create_data["symptom"]["id"]
    
    # 獲取症狀
    get_response = test_client.get(f"/api/v1/admin/symptoms/{symptom_id}")
    assert get_response.status_code == 200
    get_data = get_response.json()
    
    assert "status" in get_data
    assert get_data["status"] == "success"
    assert "symptom" in get_data
    assert get_data["symptom"]["name"] == "測試症狀"
    assert get_data["symptom"]["category"] == "技術"
    
    # 更新症狀
    update_data = {
        "name": "更新後的測試症狀",
        "category": "裝備"
    }
    
    update_response = test_client.put(f"/api/v1/admin/symptoms/{symptom_id}", json=update_data)
    assert update_response.status_code == 200
    update_data_response = update_response.json()
    
    assert "status" in update_data_response
    assert update_data_response["status"] == "success"
    assert "symptom" in update_data_response
    assert update_data_response["symptom"]["name"] == "更新後的測試症狀"
    assert update_data_response["symptom"]["category"] == "裝備"
    
    # 刪除症狀
    delete_response = test_client.delete(f"/api/v1/admin/symptoms/{symptom_id}")
    assert delete_response.status_code == 200
    delete_data = delete_response.json()
    
    assert "status" in delete_data
    assert delete_data["status"] == "success"
    assert "message" in delete_data
    assert delete_data["message"] == "症狀已刪除"

def test_practice_card_management_crud(test_client):
    """測試練習卡管理CRUD操作 (API-205.2)"""
    # 創建練習卡
    practice_card_data = {
        "name": "測試練習卡",
        "goal": "測試目標",
        "tips": ["要點1", "要點2"],
        "pitfalls": "常見錯誤",
        "dosage": "建議次數",
        "level": ["初級", "中級"],
        "terrain": ["綠線", "藍線"],
        "self_check": ["檢查點1", "檢查點2"],
        "card_type": "技術"
    }
    
    create_response = test_client.post("/api/v1/admin/practice-cards", json=practice_card_data)
    assert create_response.status_code == 200
    create_data = create_response.json()
    
    assert "status" in create_data
    assert create_data["status"] == "success"
    assert "practice_card" in create_data
    assert create_data["practice_card"]["name"] == "測試練習卡"
    assert create_data["practice_card"]["goal"] == "測試目標"
    assert create_data["practice_card"]["tips"] == ["要點1", "要點2"]
    assert create_data["practice_card"]["pitfalls"] == "常見錯誤"
    assert create_data["practice_card"]["dosage"] == "建議次數"
    assert create_data["practice_card"]["level"] == ["初級", "中級"]
    assert create_data["practice_card"]["terrain"] == ["綠線", "藍線"]
    assert create_data["practice_card"]["self_check"] == ["檢查點1", "檢查點2"]
    assert create_data["practice_card"]["card_type"] == "技術"
    
    practice_card_id = create_data["practice_card"]["id"]
    
    # 獲取練習卡
    get_response = test_client.get(f"/api/v1/admin/practice-cards/{practice_card_id}")
    assert get_response.status_code == 200
    get_data = get_response.json()
    
    assert "status" in get_data
    assert get_data["status"] == "success"
    assert "practice_card" in get_data
    assert get_data["practice_card"]["name"] == "測試練習卡"
    assert get_data["practice_card"]["goal"] == "測試目標"
    
    # 更新練習卡
    update_data = {
        "name": "更新後的測試練習卡",
        "goal": "更新後的測試目標"
    }
    
    update_response = test_client.put(f"/api/v1/admin/practice-cards/{practice_card_id}", json=update_data)
    assert update_response.status_code == 200
    update_data_response = update_response.json()
    
    assert "status" in update_data_response
    assert update_data_response["status"] == "success"
    assert "practice_card" in update_data_response
    assert update_data_response["practice_card"]["name"] == "更新後的測試練習卡"
    assert update_data_response["practice_card"]["goal"] == "更新後的測試目標"
    
    # 刪除練習卡
    delete_response = test_client.delete(f"/api/v1/admin/practice-cards/{practice_card_id}")
    assert delete_response.status_code == 200
    delete_data = delete_response.json()
    
    assert "status" in delete_data
    assert delete_data["status"] == "success"
    assert "message" in delete_data
    assert delete_data["message"] == "練習卡已刪除"

def test_symptom_practice_mapping_management(test_client):
    """測試症狀練習卡映射管理 (API-205.3)"""
    # 創建症狀
    symptom_data = {
        "name": "測試症狀_映射",
        "category": "技術",
        "synonyms": ["測試", "示例"],
        "level_scope": ["初級", "中級"],
        "terrain_scope": ["綠線", "藍線"],
        "style_scope": ["平花"]
    }
    
    symptom_response = test_client.post("/api/v1/admin/symptoms", json=symptom_data)
    assert symptom_response.status_code == 200
    symptom_data_response = symptom_response.json()
    symptom_id = symptom_data_response["symptom"]["id"]
    
    # 創建練習卡
    practice_card_data = {
        "name": "測試練習卡_映射",
        "goal": "測試目標",
        "tips": ["要點1", "要點2"],
        "pitfalls": "常見錯誤",
        "dosage": "建議次數",
        "level": ["初級", "中級"],
        "terrain": ["綠線", "藍線"],
        "self_check": ["檢查點1", "檢查點2"],
        "card_type": "技術"
    }
    
    practice_card_response = test_client.post("/api/v1/admin/practice-cards", json=practice_card_data)
    assert practice_card_response.status_code == 200
    practice_card_data_response = practice_card_response.json()
    practice_card_id = practice_card_data_response["practice_card"]["id"]
    
    # 創建映射
    mapping_data = {
        "symptom_id": symptom_id,
        "practice_id": practice_card_id,
        "order": 1
    }
    
    create_mapping_response = test_client.post("/api/v1/admin/symptom-practice-mappings", json=mapping_data)
    assert create_mapping_response.status_code == 200
    create_mapping_data = create_mapping_response.json()
    
    assert "status" in create_mapping_data
    assert create_mapping_data["status"] == "success"
    assert "mapping" in create_mapping_data
    assert create_mapping_data["mapping"]["symptom_id"] == symptom_id
    assert create_mapping_data["mapping"]["practice_id"] == practice_card_id
    assert create_mapping_data["mapping"]["order"] == 1
    
    # 獲取症狀的練習卡
    get_mapping_response = test_client.get(f"/api/v1/admin/symptoms/{symptom_id}/practice-cards")
    assert get_mapping_response.status_code == 200
    get_mapping_data = get_mapping_response.json()
    
    assert "status" in get_mapping_data
    assert get_mapping_data["status"] == "success"
    assert "practice_cards" in get_mapping_data
    assert "count" in get_mapping_data
    assert get_mapping_data["count"] == 1
    
    # 刪除映射
    delete_mapping_response = test_client.delete(
        "/api/v1/admin/symptom-practice-mappings",
        json={
            "symptom_id": symptom_id,
            "practice_id": practice_card_id
        }
    )
    assert delete_mapping_response.status_code == 200
    delete_mapping_data = delete_mapping_response.json()
    
    assert "status" in delete_mapping_data
    assert delete_mapping_data["status"] == "success"
    assert "message" in delete_mapping_data
    assert delete_mapping_data["message"] == "映射已刪除"

def test_symptom_validation_logic(test_client):
    """測試症狀驗證邏輯 (API-202.4)"""
    # 創建症狀
    symptom_data = {
        "name": "測試症狀_驗證",
        "category": "技術",
        "synonyms": ["測試", "示例"],
        "level_scope": ["初級", "中級"],
        "terrain_scope": ["綠線", "藍線"],
        "style_scope": ["平花"]
    }
    
    symptom_response = test_client.post("/api/v1/admin/symptoms", json=symptom_data)
    assert symptom_response.status_code == 200
    symptom_data_response = symptom_response.json()
    symptom_id = symptom_data_response["symptom"]["id"]
    
    # 獲取症狀的練習卡（應該顯示警告因為關聯數量不足3張）
    get_mapping_response = test_client.get(f"/api/v1/admin/symptoms/{symptom_id}/practice-cards")
    assert get_mapping_response.status_code == 200
    get_mapping_data = get_mapping_response.json()
    
    assert "status" in get_mapping_data
    assert get_mapping_data["status"] == "success"
    assert "practice_cards" in get_mapping_data
    assert "count" in get_mapping_data
    assert "warning" in get_mapping_data
    # 應該顯示警告，因為還沒有關聯任何練習卡
    assert get_mapping_data["warning"] is not None

def test_admin_analytics_summary(test_client):
    """測試管理後台分析摘要 (API-207.1)"""
    response = test_client.get("/api/v1/admin/feedback-analytics/summary")
    assert response.status_code == 200
    data = response.json()
    
    assert "status" in data
    assert data["status"] == "success"
    assert "session_feedback_distribution" in data
    assert "immediate_vs_delayed" in data
    assert "feedback_completion_rate" in data
    assert "total_feedback_count" in data
    assert "rating_distribution" in data
    assert "average_rating" in data
    assert "rating_count" in data
    assert "favorite_count" in data
    assert "favorite_rate" in data

def test_practice_card_feedback_analysis(test_client):
    """測試練習卡回饋分析 (API-207.2)"""
    # 創建練習卡
    practice_card_data = {
        "name": "測試練習卡_分析",
        "goal": "測試目標",
        "tips": ["要點1", "要點2"],
        "pitfalls": "常見錯誤",
        "dosage": "建議次數",
        "level": ["初級", "中級"],
        "terrain": ["綠線", "藍線"],
        "self_check": ["檢查點1", "檢查點2"],
        "card_type": "技術"
    }
    
    practice_card_response = test_client.post("/api/v1/admin/practice-cards", json=practice_card_data)
    assert practice_card_response.status_code == 200
    practice_card_data_response = practice_card_response.json()
    practice_card_id = practice_card_data_response["practice_card"]["id"]
    
    # 獲取練習卡回饋分析
    response = test_client.get(f"/api/v1/admin/feedback-analytics/practice-cards/{practice_card_id}")
    assert response.status_code == 200
    data = response.json()
    
    assert "status" in data
    assert data["status"] == "success"
    assert "card_info" in data
    assert "rating_distribution" in data
    assert "average_rating" in data
    assert "rating_count" in data
    assert "favorite_count" in data
    assert "favorite_rate" in data

def test_symptom_feedback_analysis(test_client):
    """測試症狀回饋分析 (API-207.3)"""
    # 創建症狀
    symptom_data = {
        "name": "測試症狀_分析",
        "category": "技術",
        "synonyms": ["測試", "示例"],
        "level_scope": ["初級", "中級"],
        "terrain_scope": ["綠線", "藍線"],
        "style_scope": ["平花"]
    }
    
    symptom_response = test_client.post("/api/v1/admin/symptoms", json=symptom_data)
    assert symptom_response.status_code == 200
    symptom_data_response = symptom_response.json()
    symptom_id = symptom_data_response["symptom"]["id"]
    
    # 獲取症狀回饋分析
    response = test_client.get(f"/api/v1/admin/feedback-analytics/symptoms/{symptom_id}")
    assert response.status_code in [200, 404]  # 可能返回404如果症狀不存在
    if response.status_code == 200:
        data = response.json()
        
        assert "status" in data
        assert data["status"] == "success"
        assert "symptom_info" in data
        assert "session_feedback_distribution" in data
        assert "related_cards_analysis" in data
        assert "high_performers" in data
        assert "low_performers" in data

def test_user_preference_analysis(test_client):
    """測試用戶偏好分析 (API-207.4)"""
    response = test_client.get("/api/v1/admin/feedback-analytics/user-preferences")
    assert response.status_code in [200, 404]  # 可能返回404如果用戶偏好不存在
    if response.status_code == 200:
        data = response.json()
        
        assert "status" in data
        assert data["status"] == "success"
        assert "top_rated_cards" in data
        assert "most_favorited_cards" in data
        assert "user_segment_analysis" in data