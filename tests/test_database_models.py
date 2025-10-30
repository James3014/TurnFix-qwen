"""
數據庫模型測試
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.base import Base
from backend.models.symptom import Symptom
from backend.models.practice_card import PracticeCard
from backend.models.session import Session
from backend.models.symptom_practice_mapping import SymptomPracticeMapping
from backend.models.practice_card_feedback import PracticeCardFeedback
from backend.models.session_feedback import SessionFeedback


@pytest.fixture
def db_session():
    """創建測試用的數據庫會話"""
    # 使用內存數據庫進行測試
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    yield session
    
    session.close()


def test_symptom_model(db_session):
    """測試症狀模型"""
    from backend.database.repositories import SymptomRepository
    import json
    
    # 創建一個症狀對象 using hybrid properties, we can pass lists directly
    symptom = Symptom(
        name="重心太後",
        category="技術",
        synonyms=["後坐", "重心後移"],
        level_scope=["初級", "中級"],
        terrain_scope=["綠線", "藍線"],
        style_scope=["平花"]
    )
    
    db_session.add(symptom)
    db_session.commit()
    
    # 驗證對象已正確保存
    saved_symptom = db_session.query(Symptom).filter(Symptom.name == "重心太後").first()
    assert saved_symptom is not None
    assert saved_symptom.name == "重心太後"
    assert saved_symptom.category == "技術"
    assert saved_symptom.synonyms == ["後坐", "重心後移"]
    assert saved_symptom.level_scope == ["初級", "中級"]
    assert saved_symptom.terrain_scope == ["綠線", "藍線"]
    assert saved_symptom.style_scope == ["平花"]


def test_practice_card_model(db_session):
    """測試練習卡模型"""
    
    # 創建一個練習卡對象，使用hybrid properties可以直接傳遞列表
    practice_card = PracticeCard(
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
    
    db_session.add(practice_card)
    db_session.commit()
    
    # 驗證對象已正確保存
    saved_card = db_session.query(PracticeCard).filter(PracticeCard.name == "J型轉彎練習").first()
    assert saved_card is not None
    assert saved_card.name == "J型轉彎練習"
    assert saved_card.goal == "完成外腳承重再過中立"
    assert saved_card.tips == ["視線外緣", "外腳 70–80%", "中立後換刃"]
    assert saved_card.pitfalls == "避免提前壓內腳"
    assert saved_card.dosage == "藍線 6 次/趟 ×3 趟"
    assert saved_card.level == ["初級", "中級"]
    assert saved_card.terrain == ["綠線", "藍線"]
    assert saved_card.self_check == ["是否在換刃前感到外腳壓力峰值？"]
    assert saved_card.card_type == "技術"


def test_session_model(db_session):
    """測試會話模型"""
    # 創建一個會話對象
    session = Session(
        user_type="學員",
        input_text="轉彎會後坐",
        level_slot="初級",
        terrain_slot="綠線",
        style_slot="平花",
        chosen_symptom_id=1,
        feedback_rating="applicable",
        feedback_text="練習卡很有用"
    )
    
    db_session.add(session)
    db_session.commit()
    
    # 驗證對象已正確保存
    saved_session = db_session.query(Session).filter(Session.input_text == "轉彎會後坐").first()
    assert saved_session is not None
    assert saved_session.user_type == "學員"
    assert saved_session.input_text == "轉彎會後坐"
    assert saved_session.level_slot == "初級"
    assert saved_session.terrain_slot == "綠線"
    assert saved_session.style_slot == "平花"
    assert saved_session.chosen_symptom_id == 1
    assert saved_session.feedback_rating == "applicable"
    assert saved_session.feedback_text == "練習卡很有用"


def test_symptom_practice_mapping_model(db_session):
    """測試症狀練習卡映射模型"""
    # 創建一個映射對象
    mapping = SymptomPracticeMapping(
        symptom_id=1,
        practice_id=1,
        order=0
    )
    
    db_session.add(mapping)
    db_session.commit()
    
    # 驗證對象已正確保存
    saved_mapping = db_session.query(SymptomPracticeMapping).filter(
        SymptomPracticeMapping.symptom_id == 1,
        SymptomPracticeMapping.practice_id == 1
    ).first()
    
    assert saved_mapping is not None
    assert saved_mapping.symptom_id == 1
    assert saved_mapping.practice_id == 1
    assert saved_mapping.order == 0


def test_practice_card_feedback_model(db_session):
    """測試練習卡回饋模型"""
    # 創建一個回饋對象
    feedback = PracticeCardFeedback(
        session_id=1,
        practice_id=1,
        rating=5,
        feedback_text="這張練習卡非常有幫助",
        is_favorite=True
    )
    
    db_session.add(feedback)
    db_session.commit()
    
    # 驗證對象已正確保存
    saved_feedback = db_session.query(PracticeCardFeedback).filter(
        PracticeCardFeedback.session_id == 1,
        PracticeCardFeedback.practice_id == 1
    ).first()
    
    assert saved_feedback is not None
    assert saved_feedback.session_id == 1
    assert saved_feedback.practice_id == 1
    assert saved_feedback.rating == 5
    assert saved_feedback.feedback_text == "這張練習卡非常有幫助"
    assert saved_feedback.is_favorite is True


def test_session_feedback_model(db_session):
    """測試會話回饋模型"""
    # 創建一個會話回饋對象
    session_feedback = SessionFeedback(
        session_id=1,
        rating="applicable",
        feedback_text="整體建議很有用",
        feedback_type="immediate"
    )
    
    db_session.add(session_feedback)
    db_session.commit()
    
    # 驗證對象已正確保存
    saved_session_feedback = db_session.query(SessionFeedback).filter(
        SessionFeedback.session_id == 1
    ).first()
    
    assert saved_session_feedback is not None
    assert saved_session_feedback.session_id == 1
    assert saved_session_feedback.rating == "applicable"
    assert saved_session_feedback.feedback_text == "整體建議很有用"
    assert saved_session_feedback.feedback_type == "immediate"