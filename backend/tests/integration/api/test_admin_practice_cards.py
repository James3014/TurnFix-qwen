"""
Admin Practice Cards API 集成測試
測試練習卡管理 API 端點
"""
import pytest


class TestAdminPracticeCardsAPI:
    """練習卡管理 API 測試類"""

    def test_create_practice_card_success(self, client, sample_practice_card_data):
        """測試成功創建練習卡"""
        response = client.post(
            "/api/v1/admin/practice-cards",
            json=sample_practice_card_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "practice_card" in data
        assert data["practice_card"]["name"] == sample_practice_card_data["name"]

    def test_get_all_practice_cards(self, client, sample_practice_card_data):
        """測試獲取所有練習卡"""
        # 先創建一些練習卡
        for i in range(3):
            data = sample_practice_card_data.copy()
            data["name"] = f"練習卡{i}"
            client.post("/api/v1/admin/practice-cards", json=data)

        # 獲取所有練習卡
        response = client.get("/api/v1/admin/practice-cards")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "practice_cards" in data
        assert len(data["practice_cards"]) >= 3

    def test_get_practice_card_by_id(self, client, sample_practice_card_data):
        """測試通過 ID 獲取練習卡"""
        # 先創建練習卡
        create_response = client.post(
            "/api/v1/admin/practice-cards",
            json=sample_practice_card_data
        )
        card_id = create_response.json()["practice_card"]["id"]

        # 獲取練習卡
        response = client.get(f"/api/v1/admin/practice-cards/{card_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["practice_card"]["id"] == card_id

    def test_update_practice_card(self, client, sample_practice_card_data):
        """測試更新練習卡"""
        # 先創建練習卡
        create_response = client.post(
            "/api/v1/admin/practice-cards",
            json=sample_practice_card_data
        )
        card_id = create_response.json()["practice_card"]["id"]

        # 更新練習卡
        update_data = {"goal": "更新後的目標"}
        response = client.put(
            f"/api/v1/admin/practice-cards/{card_id}",
            json=update_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["practice_card"]["goal"] == "更新後的目標"

    def test_delete_practice_card(self, client, sample_practice_card_data):
        """測試刪除練習卡"""
        # 先創建練習卡
        create_response = client.post(
            "/api/v1/admin/practice-cards",
            json=sample_practice_card_data
        )
        card_id = create_response.json()["practice_card"]["id"]

        # 刪除練習卡
        response = client.delete(f"/api/v1/admin/practice-cards/{card_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

        # 驗證已刪除
        get_response = client.get(f"/api/v1/admin/practice-cards/{card_id}")
        assert get_response.status_code == 404
