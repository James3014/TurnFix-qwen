"""
數據庫倉庫類測試
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.base import Base
from backend.models.symptom import Symptom
from backend.models.practice_card import PracticeCard
from backend.database.repositories import (
    SymptomRepository,
    PracticeCardRepository,
    SessionRepository,
    SymptomPracticeMappingRepository,
    PracticeCardFeedbackRepository,
    SessionFeedbackRepository
)


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


def test_symptom_repository(db_session):
    """測試症狀倉庫"""
    repo = SymptomRepository(db_session)
    
    # 測試創建症狀
    symptom = Symptom(
        name="測試症狀",
        category="技術",
        synonyms=["測試", "問題"],
        level_scope=["初級"],
        terrain_scope=["綠線"],
        style_scope=["平花"]
    )
    created_symptom = repo.create(symptom)
    
    # 驗證創建成功
    assert created_symptom.id is not None
    assert created_symptom.name == "測試症狀"
    
    # 測試根據ID獲取
    retrieved_symptom = repo.get_by_id(created_symptom.id)
    assert retrieved_symptom is not None
    assert retrieved_symptom.name == "測試症狀"
    
    # 測試根據名稱獲取
    retrieved_by_name = repo.get_by_name("測試症狀")
    assert retrieved_by_name is not None
    assert retrieved_by_name.id == created_symptom.id
    
    # 測試更新
    updated_symptom = repo.update(created_symptom.id, name="更新症狀")
    assert updated_symptom is not None
    assert updated_symptom.name == "更新症狀"
    
    # 測試獲取所有
    all_symptoms = repo.get_all()
    assert len(all_symptoms) == 1
    assert all_symptoms[0].name == "更新症狀"
    
    # 測試通過同義詞查找
    found_symptom = repo.find_by_synonym("測試")
    assert found_symptom is not None
    assert found_symptom.id == created_symptom.id
    
    # 測試刪除
    deleted = repo.delete(created_symptom.id)
    assert deleted is True
    
    # 驗證已刪除
    deleted_symptom = repo.get_by_id(created_symptom.id)
    assert deleted_symptom is None


def test_practice_card_repository(db_session):
    """測試練習卡倉庫"""
    repo = PracticeCardRepository(db_session)
    
    # 測試創建練習卡
    practice_card = PracticeCard(
        name="測試練習卡",
        goal="測試目標",
        tips=["測試要點"],
        pitfalls="測試錯誤",
        dosage="測試時長",
        level=["初級"],
        terrain=["綠線"],
        self_check=["測試檢查"],
        card_type="技術"
    )
    created_card = repo.create(practice_card)
    
    # 驗證創建成功
    assert created_card.id is not None
    assert created_card.name == "測試練習卡"
    
    # 測試根據ID獲取
    retrieved_card = repo.get_by_id(created_card.id)
    assert retrieved_card is not None
    assert retrieved_card.name == "測試練習卡"
    
    # 測試更新
    updated_card = repo.update(created_card.id, name="更新練習卡")
    assert updated_card is not None
    assert updated_card.name == "更新練習卡"
    
    # 測試獲取所有
    all_cards = repo.get_all()
    assert len(all_cards) == 1
    assert all_cards[0].name == "更新練習卡"
    
    # 測試根據條件獲取
    cards_by_conditions = repo.get_by_conditions("初級", "綠線", None)
    assert len(cards_by_conditions) == 1
    assert cards_by_conditions[0].name == "更新練習卡"
    
    # 測試刪除
    deleted = repo.delete(created_card.id)
    assert deleted is True
    
    # 驗證已刪除
    deleted_card = repo.get_by_id(created_card.id)
    assert deleted_card is None


def test_symptom_practice_mapping_repository(db_session):
    """測試症狀練習卡映射倉庫"""
    symptom_repo = SymptomRepository(db_session)
    practice_repo = PracticeCardRepository(db_session)
    mapping_repo = SymptomPracticeMappingRepository(db_session)
    
    # 創建測試數據
    symptom = Symptom(name="測試症狀", category="技術")
    practice_card = PracticeCard(
        name="測試練習卡",
        goal="測試目標",
        card_type="技術"
    )
    
    created_symptom = symptom_repo.create(symptom)
    created_card = practice_repo.create(practice_card)
    
    # 測試創建映射
    mapping = mapping_repo.create_mapping(created_symptom.id, created_card.id, 0)
    assert mapping is not None
    assert mapping.symptom_id == created_symptom.id
    assert mapping.practice_id == created_card.id
    
    # 測試根據症狀ID獲取練習卡
    cards_by_symptom = mapping_repo.get_practice_cards_by_symptom(created_symptom.id)
    assert len(cards_by_symptom) == 1
    assert cards_by_symptom[0].id == created_card.id
    
    # 測試獲取指定症狀的所有映射
    mappings_by_symptom = mapping_repo.get_mappings_by_symptom(created_symptom.id)
    assert len(mappings_by_symptom) == 1
    assert mappings_by_symptom[0].symptom_id == created_symptom.id
    assert mappings_by_symptom[0].practice_id == created_card.id
    
    # 測試刪除映射
    deleted = mapping_repo.delete_mapping(created_symptom.id, created_card.id)
    assert deleted is True
    
    # 驗證已刪除
    mappings_after_delete = mapping_repo.get_mappings_by_symptom(created_symptom.id)
    assert len(mappings_after_delete) == 0