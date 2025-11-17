"""
SymptomRepository 單元測試
測試症狀數據庫操作的所有方法
"""
import pytest
from backend.database.repositories import SymptomRepository
from backend.models.symptom import Symptom


class TestSymptomRepository:
    """SymptomRepository 測試類"""

    def test_create_symptom(self, test_db, sample_symptom_data):
        """測試創建症狀"""
        repo = SymptomRepository(test_db)

        # 創建新症狀
        new_symptom = Symptom(**sample_symptom_data)
        created_symptom = repo.create(new_symptom)

        assert created_symptom.id is not None
        assert created_symptom.name == sample_symptom_data["name"]
        assert created_symptom.category == sample_symptom_data["category"]

    def test_get_by_id(self, test_db, sample_symptom_data):
        """測試通過 ID 獲取症狀"""
        repo = SymptomRepository(test_db)

        # 先創建一個症狀
        new_symptom = Symptom(**sample_symptom_data)
        created = repo.create(new_symptom)

        # 通過 ID 獲取
        found_symptom = repo.get_by_id(created.id)

        assert found_symptom is not None
        assert found_symptom.id == created.id
        assert found_symptom.name == sample_symptom_data["name"]

    def test_get_by_id_not_found(self, test_db):
        """測試獲取不存在的症狀"""
        repo = SymptomRepository(test_db)
        found_symptom = repo.get_by_id(99999)
        assert found_symptom is None

    def test_get_by_name(self, test_db, sample_symptom_data):
        """測試通過名稱獲取症狀"""
        repo = SymptomRepository(test_db)

        # 先創建
        new_symptom = Symptom(**sample_symptom_data)
        repo.create(new_symptom)

        # 通過名稱獲取
        found = repo.get_by_name(sample_symptom_data["name"])

        assert found is not None
        assert found.name == sample_symptom_data["name"]

    def test_get_all(self, test_db, sample_symptom_data):
        """測試獲取所有症狀"""
        repo = SymptomRepository(test_db)

        # 創建多個症狀
        for i in range(3):
            data = sample_symptom_data.copy()
            data["name"] = f"症狀{i}"
            new_symptom = Symptom(**data)
            repo.create(new_symptom)

        # 獲取所有
        all_symptoms = repo.get_all()

        assert len(all_symptoms) == 3

    def test_update_symptom(self, test_db, sample_symptom_data):
        """測試更新症狀"""
        repo = SymptomRepository(test_db)

        # 創建症狀
        new_symptom = Symptom(**sample_symptom_data)
        created = repo.create(new_symptom)

        # 更新
        updated = repo.update(created.id, name="更新後的名稱")

        assert updated is not None
        assert updated.name == "更新後的名稱"

    def test_delete_symptom(self, test_db, sample_symptom_data):
        """測試刪除症狀"""
        repo = SymptomRepository(test_db)

        # 創建症狀
        new_symptom = Symptom(**sample_symptom_data)
        created = repo.create(new_symptom)

        # 刪除
        result = repo.delete(created.id)

        assert result is True

        # 驗證已刪除
        found = repo.get_by_id(created.id)
        assert found is None

    def test_delete_nonexistent_symptom(self, test_db):
        """測試刪除不存在的症狀"""
        repo = SymptomRepository(test_db)
        result = repo.delete(99999)
        assert result is False

    def test_find_by_synonym(self, test_db, sample_symptom_data):
        """測試通過同義詞查找症狀"""
        repo = SymptomRepository(test_db)

        # 創建症狀
        new_symptom = Symptom(**sample_symptom_data)
        repo.create(new_symptom)

        # 通過同義詞查找
        found = repo.find_by_synonym("後坐")

        assert found is not None
        assert found.name == sample_symptom_data["name"]
