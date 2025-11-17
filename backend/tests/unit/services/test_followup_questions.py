"""
自適應追問服務單元測試
測試 followup_questions.py 的所有核心函數
"""
import pytest
from backend.services.followup_questions import (
    assess_confidence,
    generate_followup_questions,
    get_followup_needs,
    identify_simple_symptom
)
from backend.database.repositories import SymptomRepository
from backend.models.symptom import Symptom


class TestFollowupQuestions:
    """自適應追問服務測試類"""

    def test_assess_confidence_high(self, test_db):
        """測試高置信度情況（完整資訊）"""
        symptom = Symptom(
            name="重心太後",
            category="技術",
            synonyms=["後坐"]
        )

        confidence, missing_slots = assess_confidence(
            user_input="我滑雪時總是感覺重心偏後，容易後坐",
            recognized_symptom=symptom,
            level="初級",
            terrain="綠線",
            style="平花"
        )

        # 完整資訊 + 描述充分，置信度應該很高
        assert confidence >= 0.7
        assert len(missing_slots) == 0

    def test_assess_confidence_missing_level(self, test_db):
        """測試缺少等級資訊時的置信度"""
        symptom = Symptom(
            name="換刃問題",
            category="技術"
        )

        confidence, missing_slots = assess_confidence(
            user_input="我換刃的時候不太穩定",
            recognized_symptom=symptom,
            level=None,
            terrain="綠線",
            style="平花"
        )

        assert "level" in missing_slots
        assert confidence < 1.0

    def test_assess_confidence_missing_terrain(self, test_db):
        """測試缺少地形資訊時的置信度"""
        symptom = Symptom(name="測試症狀", category="技術")

        confidence, missing_slots = assess_confidence(
            user_input="我有滑雪問題需要幫助",
            recognized_symptom=symptom,
            level="初級",
            terrain=None,
            style="平花"
        )

        assert "terrain" in missing_slots
        assert confidence < 1.0

    def test_assess_confidence_missing_style(self, test_db):
        """測試缺少風格資訊時的置信度"""
        symptom = Symptom(name="測試症狀", category="技術")

        confidence, missing_slots = assess_confidence(
            user_input="我有滑雪問題需要幫助",
            recognized_symptom=symptom,
            level="初級",
            terrain="綠線",
            style=None
        )

        assert "style" in missing_slots
        assert confidence < 1.0

    def test_assess_confidence_short_input(self, test_db):
        """測試輸入過短時的置信度"""
        symptom = Symptom(name="測試", category="技術")

        confidence, missing_slots = assess_confidence(
            user_input="後坐",  # 很短的輸入
            recognized_symptom=symptom,
            level="初級",
            terrain="綠線",
            style="平花"
        )

        # 輸入太短應降低置信度
        assert confidence < 0.8

    def test_assess_confidence_many_synonyms(self, test_db):
        """測試症狀有多個同義詞時的置信度"""
        symptom = Symptom(
            name="測試症狀",
            category="技術",
            synonyms=["同義詞1", "同義詞2", "同義詞3", "同義詞4"]
        )

        confidence, missing_slots = assess_confidence(
            user_input="我有滑雪問題",
            recognized_symptom=symptom,
            level="初級",
            terrain="綠線",
            style="平花"
        )

        # 多個同義詞表示競爭激烈，應降低置信度
        assert confidence < 1.0

    def test_assess_confidence_minimum_zero(self, test_db):
        """測試置信度不會低於 0"""
        symptom = Symptom(
            name="測試",
            category="技術",
            synonyms=["s1", "s2", "s3", "s4"]
        )

        confidence, missing_slots = assess_confidence(
            user_input="短",  # 極短輸入
            recognized_symptom=symptom,
            level=None,
            terrain=None,
            style=None
        )

        assert confidence >= 0.0
        assert confidence <= 1.0

    def test_generate_followup_questions_low_confidence(self, test_db):
        """測試低置信度時生成追問問題"""
        confidence = 0.5
        missing_slots = ["level", "terrain"]

        questions = generate_followup_questions(
            confidence=confidence,
            missing_slots=missing_slots,
            user_input="我有問題"
        )

        # 低置信度應該生成問題
        assert len(questions) > 0
        # 檢查是否包含等級相關問題
        assert any("等級" in q["question"] for q in questions)

    def test_generate_followup_questions_high_confidence(self, test_db):
        """測試高置信度時不生成追問問題"""
        confidence = 0.9
        missing_slots = []

        questions = generate_followup_questions(
            confidence=confidence,
            missing_slots=missing_slots,
            user_input="我滑雪時總是感覺重心偏後"
        )

        # 高置信度不需要追問
        assert len(questions) == 0

    def test_generate_followup_questions_max_two(self, test_db):
        """測試最多生成 2 個問題"""
        confidence = 0.3
        missing_slots = ["level", "terrain", "style"]

        questions = generate_followup_questions(
            confidence=confidence,
            missing_slots=missing_slots,
            user_input="幫我"  # 很短
        )

        # 應該限制在 2 個問題
        assert len(questions) <= 2

    def test_generate_followup_questions_clarification(self, test_db):
        """測試生成澄清問題"""
        confidence = 0.5
        missing_slots = []

        questions = generate_followup_questions(
            confidence=confidence,
            missing_slots=missing_slots,
            user_input="問題"  # 很短
        )

        # 輸入太短應該要求澄清
        assert len(questions) > 0
        assert any("詳細描述" in q["question"] for q in questions)

    def test_identify_simple_symptom_by_synonym(self, test_db):
        """測試通過同義詞識別症狀"""
        symptom_repo = SymptomRepository(test_db)

        symptom = Symptom(
            name="重心太後",
            category="技術",
            synonyms=["後坐", "重心後移"]
        )
        symptom_repo.create(symptom)

        result = identify_simple_symptom(symptom_repo, "後坐")

        assert result is not None
        assert result.name == "重心太後"

    def test_identify_simple_symptom_by_keyword(self, test_db):
        """測試通過關鍵詞識別症狀"""
        symptom_repo = SymptomRepository(test_db)

        symptom = Symptom(
            name="換刃不順",
            category="技術"
        )
        symptom_repo.create(symptom)

        result = identify_simple_symptom(symptom_repo, "我換刃時有問題")

        assert result is not None
        assert "換刃" in result.name

    def test_identify_simple_symptom_default(self, test_db):
        """測試無法識別時返回默認症狀"""
        symptom_repo = SymptomRepository(test_db)

        result = identify_simple_symptom(symptom_repo, "完全無關的內容")

        assert result is not None
        assert result.name == "一般技術問題"

    def test_get_followup_needs_high_confidence(self, test_db):
        """測試高置信度情況不需要追問"""
        symptom_repo = SymptomRepository(test_db)

        # 創建測試症狀
        symptom = Symptom(
            name="重心太後",
            category="技術",
            synonyms=["後坐"]
        )
        symptom_repo.create(symptom)

        result = get_followup_needs(
            db=test_db,
            user_input="我滑雪時總是感覺重心偏後，容易後坐的情況",
            level="初級",
            terrain="綠線",
            style="平花"
        )

        assert "need_followup" in result
        assert "confidence" in result
        assert "missing_slots" in result
        assert "questions" in result
        # 高置信度不需要追問
        assert result["need_followup"] is False

    def test_get_followup_needs_low_confidence(self, test_db):
        """測試低置信度情況需要追問"""
        symptom_repo = SymptomRepository(test_db)

        symptom = Symptom(
            name="測試症狀",
            category="技術"
        )
        symptom_repo.create(symptom)

        result = get_followup_needs(
            db=test_db,
            user_input="有問題",  # 很短
            level=None,
            terrain=None,
            style=None
        )

        assert result["need_followup"] is True
        assert result["confidence"] < 0.7
        assert len(result["questions"]) > 0

    def test_get_followup_needs_missing_info(self, test_db):
        """測試缺少資訊時需要追問"""
        symptom_repo = SymptomRepository(test_db)

        symptom = Symptom(
            name="換刃問題",
            category="技術",
            synonyms=["換刃"]
        )
        symptom_repo.create(symptom)

        result = get_followup_needs(
            db=test_db,
            user_input="我換刃時不太穩",
            level=None,  # 缺少等級
            terrain=None,  # 缺少地形
            style="平花"
        )

        assert "level" in result["missing_slots"] or "terrain" in result["missing_slots"]

    def test_get_followup_needs_error_handling(self, test_db):
        """測試錯誤處理的降級策略"""
        # 傳入 None 作為 db 會觸發異常
        result = get_followup_needs(
            db=None,
            user_input="測試",
            level="初級",
            terrain="綠線",
            style="平花"
        )

        # 降級策略：不追問
        assert result["need_followup"] is False
        assert result["confidence"] == 1.0
        assert len(result["questions"]) == 0
