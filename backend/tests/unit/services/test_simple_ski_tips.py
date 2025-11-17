"""
簡化版滑雪技巧服務單元測試
測試 simple_ski_tips.py 的所有核心函數
"""
import pytest
from backend.services.simple_ski_tips import (
    get_ski_tips,
    identify_symptom,
    filter_cards_by_conditions,
    rank_cards,
    get_default_tips,
    card_to_dict,
    process_ski_tips_request
)
from backend.database.repositories import (
    SymptomRepository,
    PracticeCardRepository,
    SymptomPracticeMappingRepository
)
from backend.models.symptom import Symptom
from backend.models.practice_card import PracticeCard
from backend.models.symptom_practice_mapping import SymptomPracticeMapping


class TestSimpleSkiTips:
    """簡化版滑雪技巧服務測試類"""

    def test_identify_symptom_by_synonym(self, test_db):
        """測試通過同義詞識別症狀"""
        symptom_repo = SymptomRepository(test_db)

        # 創建測試症狀
        symptom = Symptom(
            name="重心太後",
            category="技術",
            synonyms=["後坐", "重心後移"]
        )
        symptom_repo.create(symptom)

        # 測試識別
        result = identify_symptom(symptom_repo, "我滑雪時容易後坐")

        assert result is not None
        assert result.name == "重心太後"

    def test_identify_symptom_by_keyword(self, test_db):
        """測試通過關鍵詞識別症狀"""
        symptom_repo = SymptomRepository(test_db)

        symptom = Symptom(
            name="換刃不順",
            category="技術"
        )
        symptom_repo.create(symptom)

        result = identify_symptom(symptom_repo, "我換刃時有問題")

        assert result is not None
        assert "換刃" in result.name

    def test_identify_symptom_default(self, test_db):
        """測試無法識別時返回默認症狀"""
        symptom_repo = SymptomRepository(test_db)

        result = identify_symptom(symptom_repo, "完全無關的文字 xyz123")

        assert result is not None
        assert result.name == "一般技術問題"

    def test_filter_cards_by_level(self, test_db):
        """測試按等級篩選練習卡"""
        # 創建測試卡片
        card1 = PracticeCard(
            name="初級練習",
            goal="測試",
            level=["初級"],
            terrain=["綠線"]
        )
        card2 = PracticeCard(
            name="中級練習",
            goal="測試",
            level=["中級"],
            terrain=["藍線"]
        )

        cards = [card1, card2]

        # 篩選初級
        filtered = filter_cards_by_conditions(test_db, cards, level="初級", terrain=None, style=None)

        assert len(filtered) == 1
        assert filtered[0].name == "初級練習"

    def test_filter_cards_by_terrain(self, test_db):
        """測試按地形篩選練習卡"""
        card1 = PracticeCard(
            name="綠線練習",
            goal="測試",
            terrain=["綠線"]
        )
        card2 = PracticeCard(
            name="黑線練習",
            goal="測試",
            terrain=["黑線"]
        )

        cards = [card1, card2]

        filtered = filter_cards_by_conditions(test_db, cards, level=None, terrain="綠線", style=None)

        assert len(filtered) == 1
        assert filtered[0].name == "綠線練習"

    def test_filter_cards_fallback_when_empty(self, test_db):
        """測試篩選結果為空時返回原列表"""
        card1 = PracticeCard(
            name="專業練習",
            goal="測試",
            level=["高級"]
        )

        cards = [card1]

        # 篩選初級（不匹配）
        filtered = filter_cards_by_conditions(test_db, cards, level="初級", terrain=None, style=None)

        # 應返回原列表（降級策略）
        assert len(filtered) == 1

    def test_rank_cards_by_level_match(self, test_db):
        """測試根據等級匹配排序"""
        card1 = PracticeCard(
            id=1,
            name="不匹配卡片",
            goal="測試",
            level=["高級"]
        )
        card2 = PracticeCard(
            id=2,
            name="匹配卡片",
            goal="測試",
            level=["初級"]
        )

        cards = [card1, card2]

        ranked = rank_cards(cards, level="初級", terrain=None)

        # 匹配的卡片應該排在前面
        assert ranked[0].name == "匹配卡片"

    def test_rank_cards_by_terrain_match(self, test_db):
        """測試根據地形匹配排序"""
        card1 = PracticeCard(
            id=1,
            name="藍線卡片",
            goal="測試",
            terrain=["藍線"]
        )
        card2 = PracticeCard(
            id=2,
            name="綠線卡片",
            goal="測試",
            terrain=["綠線"]
        )

        cards = [card1, card2]

        ranked = rank_cards(cards, level=None, terrain="綠線")

        assert ranked[0].name == "綠線卡片"

    def test_card_to_dict(self, test_db):
        """測試將練習卡轉換為字典"""
        card = PracticeCard(
            id=123,
            name="測試練習卡",
            goal="提升技巧",
            tips=["提示1", "提示2"],
            pitfalls="避免錯誤",
            dosage="10次",
            level=["初級"],
            terrain=["綠線"],
            self_check=["檢查1"],
            card_type="技術"
        )

        result = card_to_dict(card)

        assert result["id"] == 123
        assert result["name"] == "測試練習卡"
        assert result["goal"] == "提升技巧"
        assert len(result["tips"]) == 2
        assert result["level"] == ["初級"]

    def test_card_to_dict_with_none_fields(self, test_db):
        """測試處理包含 None 字段的練習卡"""
        card = PracticeCard(
            id=456,
            name="簡單卡片",
            goal="測試"
        )

        result = card_to_dict(card)

        assert result["id"] == 456
        assert result["tips"] == []
        assert result["pitfalls"] == ""
        assert result["dosage"] == ""

    def test_get_default_tips(self, test_db):
        """測試獲取默認建議"""
        practice_repo = PracticeCardRepository(test_db)

        # 創建一些練習卡
        card = PracticeCard(
            id=201,
            name="基礎滑行",
            goal="基礎練習"
        )
        practice_repo.create(card)

        result = get_default_tips(test_db)

        assert len(result) > 0
        assert result[0].id == 201

    def test_get_default_tips_fallback(self, test_db):
        """測試默認建議降級策略"""
        practice_repo = PracticeCardRepository(test_db)

        # 創建一個非 201 的卡片
        card = PracticeCard(
            id=999,
            name="其他練習",
            goal="測試"
        )
        practice_repo.create(card)

        result = get_default_tips(test_db)

        # 應該返回第一個可用的卡片
        assert len(result) > 0

    def test_get_ski_tips_success(self, test_db):
        """測試完整的獲取滑雪建議流程"""
        symptom_repo = SymptomRepository(test_db)
        practice_repo = PracticeCardRepository(test_db)
        mapping_repo = SymptomPracticeMappingRepository(test_db)

        # 創建症狀
        symptom = Symptom(
            name="重心太後",
            category="技術",
            synonyms=["後坐"]
        )
        created_symptom = symptom_repo.create(symptom)

        # 創建練習卡
        card = PracticeCard(
            name="J型轉彎",
            goal="改善重心",
            level=["初級"],
            terrain=["綠線"]
        )
        created_card = practice_repo.create(card)

        # 創建映射
        mapping = SymptomPracticeMapping(
            symptom_id=created_symptom.id,
            practice_id=created_card.id,
            order=1
        )
        mapping_repo.create(mapping)

        # 測試
        result = get_ski_tips(test_db, "我滑雪時容易後坐", level="初級", terrain="綠線")

        assert len(result) > 0
        assert result[0]["name"] == "J型轉彎"

    def test_get_ski_tips_error_fallback(self, test_db):
        """測試錯誤時返回默認建議"""
        practice_repo = PracticeCardRepository(test_db)

        # 創建默認卡片
        card = PracticeCard(
            id=201,
            name="默認練習",
            goal="基礎"
        )
        practice_repo.create(card)

        # 傳入無效參數觸發異常（空數據庫，找不到症狀會報錯）
        result = get_ski_tips(test_db, "xyz無法識別", level="初級")

        # 應該返回默認建議而不是崩潰
        assert isinstance(result, list)

    def test_process_ski_tips_request(self, test_db):
        """測試兼容性接口"""
        practice_repo = PracticeCardRepository(test_db)
        symptom_repo = SymptomRepository(test_db)
        mapping_repo = SymptomPracticeMappingRepository(test_db)

        # 準備測試數據
        symptom = Symptom(name="測試症狀", category="技術", synonyms=["測試"])
        created_symptom = symptom_repo.create(symptom)

        card = PracticeCard(name="測試卡片", goal="測試")
        created_card = practice_repo.create(card)

        mapping = SymptomPracticeMapping(
            symptom_id=created_symptom.id,
            practice_id=created_card.id,
            order=1
        )
        mapping_repo.create(mapping)

        # 測試
        result = process_ski_tips_request(
            test_db,
            "測試問題",
            level="初級",
            terrain="綠線",
            style="平花"
        )

        assert result["status"] == "success"
        assert "recommended_cards" in result
        assert "count" in result
        assert isinstance(result["recommended_cards"], list)
