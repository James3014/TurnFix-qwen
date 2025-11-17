"""
PracticeCardRepository 單元測試
測試練習卡數據庫操作的所有方法
"""
import pytest
from backend.database.repositories import PracticeCardRepository
from backend.models.practice_card import PracticeCard


class TestPracticeCardRepository:
    """PracticeCardRepository 測試類"""

    def test_create_practice_card(self, test_db, sample_practice_card_data):
        """測試創建練習卡"""
        repo = PracticeCardRepository(test_db)

        new_card = PracticeCard(**sample_practice_card_data)
        created = repo.create(new_card)

        assert created.id is not None
        assert created.name == sample_practice_card_data["name"]
        assert created.goal == sample_practice_card_data["goal"]

    def test_get_by_id(self, test_db, sample_practice_card_data):
        """測試通過 ID 獲取練習卡"""
        repo = PracticeCardRepository(test_db)

        new_card = PracticeCard(**sample_practice_card_data)
        created = repo.create(new_card)

        found = repo.get_by_id(created.id)

        assert found is not None
        assert found.id == created.id
        assert found.name == sample_practice_card_data["name"]

    def test_get_by_id_not_found(self, test_db):
        """測試獲取不存在的練習卡"""
        repo = PracticeCardRepository(test_db)
        found = repo.get_by_id(99999)
        assert found is None

    def test_get_all(self, test_db, sample_practice_card_data):
        """測試獲取所有練習卡"""
        repo = PracticeCardRepository(test_db)

        for i in range(3):
            data = sample_practice_card_data.copy()
            data["name"] = f"練習卡{i}"
            new_card = PracticeCard(**data)
            repo.create(new_card)

        all_cards = repo.get_all()

        assert len(all_cards) == 3

    def test_update_practice_card(self, test_db, sample_practice_card_data):
        """測試更新練習卡"""
        repo = PracticeCardRepository(test_db)

        new_card = PracticeCard(**sample_practice_card_data)
        created = repo.create(new_card)

        updated = repo.update(created.id, goal="更新後的目標")

        assert updated is not None
        assert updated.goal == "更新後的目標"

    def test_delete_practice_card(self, test_db, sample_practice_card_data):
        """測試刪除練習卡"""
        repo = PracticeCardRepository(test_db)

        new_card = PracticeCard(**sample_practice_card_data)
        created = repo.create(new_card)

        result = repo.delete(created.id)

        assert result is True

        found = repo.get_by_id(created.id)
        assert found is None

    def test_delete_nonexistent_card(self, test_db):
        """測試刪除不存在的練習卡"""
        repo = PracticeCardRepository(test_db)
        result = repo.delete(99999)
        assert result is False

    def test_get_by_conditions(self, test_db, sample_practice_card_data):
        """測試根據條件獲取練習卡"""
        repo = PracticeCardRepository(test_db)

        # 創建不同等級的練習卡
        data1 = sample_practice_card_data.copy()
        data1["name"] = "初級卡"
        data1["level"] = ["初級"]
        new_card1 = PracticeCard(**data1)
        repo.create(new_card1)

        data2 = sample_practice_card_data.copy()
        data2["name"] = "中級卡"
        data2["level"] = ["中級"]
        new_card2 = PracticeCard(**data2)
        repo.create(new_card2)

        # 查詢初級
        results = repo.get_by_conditions(level="初級", terrain=None, style=None)

        assert len(results) >= 1
