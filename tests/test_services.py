"""
服務層測試
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.base import Base
from backend.models.symptom import Symptom
from backend.models.practice_card import PracticeCard
from backend.models.session import Session
from backend.database.models import SymptomPracticeMapping
from backend.services.simple_ski_tips import (
    identify_symptom,
    filter_cards_by_conditions,
    rank_cards,
    card_to_dict
)
from backend.database.repositories import SymptomRepository, PracticeCardRepository


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


def test_identify_symptom(db_session):
    """測試症狀識別功能"""
    # 準備測試數據
    symptom_repo = SymptomRepository(db_session)
    symptom = Symptom(
        name="重心太後",
        category="技術",
        synonyms=["後坐", "重心不穩"]
    )
    created_symptom = symptom_repo.create(symptom)
    
    # 測試通過同義詞識別
    identified = identify_symptom(symptom_repo, "轉彎會後坐")
    assert identified is not None
    assert identified.name == "重心太後"
    assert identified.id == created_symptom.id
    
    # 測試通過名稱識別
    identified2 = identify_symptom(symptom_repo, "重心太後")
    assert identified2 is not None
    assert identified2.name == "重心太後"
    assert identified2.id == created_symptom.id
    
    # 測試找不到時返回默認值
    identified3 = identify_symptom(symptom_repo, "完全不相關的詞")
    assert identified3 is not None
    assert identified3.name == "一般技術問題"


def test_filter_cards_by_conditions(db_session):
    """測試根據條件篩選練習卡"""
    # 準備測試數據
    practice_repo = PracticeCardRepository(db_session)
    
    card1 = PracticeCard(
        name="初級練習卡",
        goal="初級目標",
        level=["初級"],
        terrain=["綠線"],
        card_type="技術"
    )
    card2 = PracticeCard(
        name="中級練習卡",
        goal="中級目標",
        level=["中級"],
        terrain=["藍線"],
        card_type="技術"
    )
    card3 = PracticeCard(
        name="通用練習卡",
        goal="通用目標",
        level=[],
        terrain=[],
        card_type="基礎"
    )
    
    created_card1 = practice_repo.create(card1)
    created_card2 = practice_repo.create(card2)
    created_card3 = practice_repo.create(card3)
    
    # 測試按等級篩選
    # Cards with no level restrictions (empty level list) should also be included
    filtered_by_level = filter_cards_by_conditions(
        db_session, 
        [created_card1, created_card2, created_card3], 
        "初級", 
        None, 
        None
    )
    assert len(filtered_by_level) == 2  # Includes "初級練習卡" (matches level) and "通用練習卡" (no restrictions)
    names = {card.name for card in filtered_by_level}
    assert names == {"初級練習卡", "通用練習卡"}
    
    # 測試按地形篩選
    # Cards with no terrain restrictions (empty terrain list) should also be included
    filtered_by_terrain = filter_cards_by_conditions(
        db_session, 
        [created_card1, created_card2, created_card3], 
        None, 
        "藍線", 
        None
    )
    assert len(filtered_by_terrain) == 2  # Includes "中級練習卡" (matches terrain) and "通用練習卡" (no restrictions)
    names = {card.name for card in filtered_by_terrain}
    assert names == {"中級練習卡", "通用練習卡"}
    
    # 測試篩選後為空時的降級策略
    filtered_empty = filter_cards_by_conditions(
        db_session, 
        [created_card3],  # 只有通用卡
        "初級", 
        "藍線", 
        None
    )
    assert len(filtered_empty) == 1
    assert filtered_empty[0].name == "通用練習卡"


def test_rank_cards():
    """測試練習卡排序功能"""
    # 創建測試練習卡
    card1 = PracticeCard(
        id=1,
        name="匹配等級",
        goal="目標1",
        level=["初級"],
        terrain=["藍線"],
        card_type="技術"
    )
    card2 = PracticeCard(
        id=2,
        name="匹配地形",
        goal="目標2",
        level=["中級"],
        terrain=["藍線"],
        card_type="技術"
    )
    card3 = PracticeCard(
        id=3,
        name="不匹配",
        goal="目標3",
        level=["高級"],
        terrain=["黑線"],
        card_type="技術"
    )
    
    # 測試排序 - 初級用戶，藍線地形
    ranked = rank_cards([card1, card2, card3], "初級", "藍線")
    assert len(ranked) == 3
    
    # 期望順序：card1 (匹配等級和地形) > card2 (只匹配地形) > card3 (不匹配)
    # 但因為card1只匹配等級，card2匹配地形，地形權重較低，所以card1排第一
    assert ranked[0].id == 1  # 匹配等級的排第一
    assert ranked[1].id == 2  # 匹配地形的排第二
    assert ranked[2].id == 3  # 不匹配的排最後


def test_card_to_dict():
    """測試練習卡轉字典功能"""
    card = PracticeCard(
        id=1,
        name="測試練習卡",
        goal="測試目標",
        tips=["要點1", "要點2"],
        pitfalls="常見錯誤",
        dosage="3次/天",
        level=["初級"],
        terrain=["綠線"],
        self_check=["檢查點1", "檢查點2"],
        card_type="技術"
    )
    
    card_dict = card_to_dict(card)
    
    assert card_dict["id"] == 1
    assert card_dict["name"] == "測試練習卡"
    assert card_dict["goal"] == "測試目標"
    assert card_dict["tips"] == ["要點1", "要點2"]
    assert card_dict["pitfalls"] == "常見錯誤"
    assert card_dict["dosage"] == "3次/天"
    assert card_dict["level"] == ["初級"]
    assert card_dict["terrain"] == ["綠線"]
    assert card_dict["self_check"] == ["檢查點1", "檢查點2"]
    assert card_dict["card_type"] == "技術"