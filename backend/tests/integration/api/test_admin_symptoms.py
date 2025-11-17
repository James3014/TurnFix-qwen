"""
Admin Symptoms API 集成測試
測試症狀管理 API 端點
"""
import pytest


class TestAdminSymptomsAPI:
    """症狀管理 API 測試類"""

    def test_create_symptom_success(self, client, sample_symptom_data):
        """測試成功創建症狀"""
        response = client.post(
            "/api/v1/admin/symptoms",
            json=sample_symptom_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "symptom" in data
        assert data["symptom"]["name"] == sample_symptom_data["name"]

    def test_create_symptom_missing_name(self, client):
        """測試創建症狀時缺少必要字段"""
        response = client.post(
            "/api/v1/admin/symptoms",
            json={"category": "技術"}
        )

        assert response.status_code == 422  # Validation error

    def test_get_all_symptoms(self, client, sample_symptom_data):
        """測試獲取所有症狀"""
        # 先創建一些症狀
        for i in range(3):
            data = sample_symptom_data.copy()
            data["name"] = f"症狀{i}"
            client.post("/api/v1/admin/symptoms", json=data)

        # 獲取所有症狀
        response = client.get("/api/v1/admin/symptoms")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "symptoms" in data
        assert len(data["symptoms"]) >= 3

    def test_get_symptom_by_id(self, client, sample_symptom_data):
        """測試通過 ID 獲取症狀"""
        # 先創建症狀
        create_response = client.post(
            "/api/v1/admin/symptoms",
            json=sample_symptom_data
        )
        symptom_id = create_response.json()["symptom"]["id"]

        # 獲取症狀
        response = client.get(f"/api/v1/admin/symptoms/{symptom_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["symptom"]["id"] == symptom_id

    def test_get_symptom_not_found(self, client):
        """測試獲取不存在的症狀"""
        response = client.get("/api/v1/admin/symptoms/99999")

        assert response.status_code == 404

    def test_update_symptom(self, client, sample_symptom_data):
        """測試更新症狀"""
        # 先創建症狀
        create_response = client.post(
            "/api/v1/admin/symptoms",
            json=sample_symptom_data
        )
        symptom_id = create_response.json()["symptom"]["id"]

        # 更新症狀
        update_data = {"name": "更新後的症狀名稱"}
        response = client.put(
            f"/api/v1/admin/symptoms/{symptom_id}",
            json=update_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["symptom"]["name"] == "更新後的症狀名稱"

    def test_delete_symptom(self, client, sample_symptom_data):
        """測試刪除症狀"""
        # 先創建症狀
        create_response = client.post(
            "/api/v1/admin/symptoms",
            json=sample_symptom_data
        )
        symptom_id = create_response.json()["symptom"]["id"]

        # 刪除症狀
        response = client.delete(f"/api/v1/admin/symptoms/{symptom_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

        # 驗證已刪除
        get_response = client.get(f"/api/v1/admin/symptoms/{symptom_id}")
        assert get_response.status_code == 404

    def test_get_symptom_practice_cards(self, client, sample_symptom_data, sample_practice_card_data):
        """測試獲取症狀的練習卡"""
        # 創建症狀
        symptom_response = client.post(
            "/api/v1/admin/symptoms",
            json=sample_symptom_data
        )
        symptom_id = symptom_response.json()["symptom"]["id"]

        # 獲取練習卡
        response = client.get(f"/api/v1/admin/symptoms/{symptom_id}/practice-cards")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "practice_cards" in data
