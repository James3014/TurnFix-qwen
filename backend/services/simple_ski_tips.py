"""
簡化版滑雪技巧建議服務

遵循 Linus 的"好品味"原則：
- 消除不必要的複雜度
- 使用簡單函數而非複雜物件導向設計
- 保持實現簡單直接
- 專注於解決核心問題
"""
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from ..core.config import settings
from ..models.symptom import Symptom
from ..models.practice_card import PracticeCard
from ..database.repositories import (
    SymptomRepository,
    PracticeCardRepository,
    SymptomPracticeMappingRepository
)
import json
import logging

logger = logging.getLogger(__name__)


def get_ski_tips(db: Session, user_input: str, level: Optional[str] = None, 
                 terrain: Optional[str] = None, style: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    獲取滑雪技巧建議的主函數
    
    簡單直接，不做過度工程
    """
    try:
        # 初始化倉庫
        symptom_repo = SymptomRepository(db)
        practice_repo = PracticeCardRepository(db)
        mapping_repo = SymptomPracticeMappingRepository(db)
        
        # 1. 症狀識別 - 簡單的字符串匹配，可擴展為更複雜的NLP
        recognized_symptom = identify_symptom(symptom_repo, user_input)
        
        # 2. 根據症狀ID獲取相關練習卡
        practice_cards = mapping_repo.get_practice_cards_by_symptom(recognized_symptom.id)
        
        # 3. 根據用戶條件進一步篩選
        filtered_cards = filter_cards_by_conditions(db, practice_cards, level, terrain, style)
        
        # 4. 排序並返回前3-5張
        ranked_cards = rank_cards(filtered_cards, level, terrain)
        
        # 5. 限制返回數量
        result_count = min(settings.MAX_PRACTICE_CARDS, 
                          max(settings.MIN_PRACTICE_CARDS, len(ranked_cards)))
        return [card_to_dict(card) for card in ranked_cards[:result_count]]
        
    except Exception as e:
        logger.error(f"獲取滑雪建議時出錯: {e}")
        # 降級策略：返回通用建議
        return [card_to_dict(card) for card in get_default_tips(db)]


def identify_symptom(symptom_repo: SymptomRepository, input_text: str) -> Symptom:
    """
    識別症狀 - 簡單實現，可擴展為更複雜的AI模型
    """
    input_lower = input_text.lower()
    
    # 檢查同義詞庫 - this will find symptoms where any of their synonyms appear in the input
    all_symptoms = symptom_repo.get_all()
    for symptom in all_symptoms:
        if symptom.synonyms and isinstance(symptom.synonyms, list):
            for synonym in symptom.synonyms:
                if synonym in input_lower:
                    return symptom
    
    # 簡單的關鍵詞匹配
    keywords = ["後坐", "重心", "不穩", "晃", "換刃", "刃"]
    for keyword in keywords:
        if keyword in input_lower:
            # 尋找包含此關鍵詞的症狀
            for s in all_symptoms:
                if keyword in s.name.lower():
                    return s
    
    # 默認返回一般問題
    default_symptom = Symptom(
        name="一般技術問題",
        category="技術"
    )
    return default_symptom


# 不需要filter_cards_by_symptom函數了，因為我們使用SymptomPracticeMappingRepository


def filter_cards_by_conditions(
    db: Session,
    practice_cards: List[PracticeCard], 
    level: Optional[str], 
    terrain: Optional[str], 
    style: Optional[str]
) -> List[PracticeCard]:
    """
    根據用戶條件篩選練習卡
    """
    filtered_cards = []
    
    for card in practice_cards:
        # With hybrid properties, card.level and card.terrain are already lists
        card_level = card.level or []
        card_terrain = card.terrain or []
        
        # 等級篩選
        if level and card_level and level in card_level:
            pass  # 條件匹配
        elif level and card_level and len(card_level) > 0:
            continue  # 條件不匹配且卡片有等級限制
        
        # 地形篩選
        if terrain and card_terrain and terrain in card_terrain:
            pass  # 條件匹配
        elif terrain and card_terrain and len(card_terrain) > 0:
            continue  # 條件不匹配且卡片有地形限制
        
        filtered_cards.append(card)
    
    # 如果篩選後為空，返回原列表（降級策略）
    return filtered_cards if filtered_cards else practice_cards


def rank_cards(cards: List[PracticeCard], level: Optional[str], terrain: Optional[str]) -> List[PracticeCard]:
    """
    根據條件對練習卡進行排序
    """
    def sort_key(card):
        score = 0
        
        # With hybrid properties, card.level and card.terrain are already lists
        card_level = card.level or []
        card_terrain = card.terrain or []
        
        # 根據等級匹配加分
        if level and card_level and level in card_level:
            score += 10
            
        # 根據地形匹配加分
        if terrain and card_terrain and terrain in card_terrain:
            score += 5
            
        # 根據卡片ID作為最後排序標準
        score += card.id * 0.01
        
        return -score  # 降序排序
    
    return sorted(cards, key=sort_key)


def get_default_tips(db: Session) -> List[PracticeCard]:
    """
    返回默認建議（降級策略）
    """
    practice_repo = PracticeCardRepository(db)
    # 獲取ID為201的基礎滑行練習卡
    card = practice_repo.get_by_id(201)
    if card:
        return [card]
    # 如果找不到特定卡，返回第一個可用的練習卡
    all_cards = practice_repo.get_all()
    return [all_cards[0]] if all_cards else []


def card_to_dict(card: PracticeCard) -> Dict[str, Any]:
    """
    將練習卡對象轉換為字典格式
    """
    return {
        "id": card.id,
        "name": card.name,
        "goal": card.goal,
        "tips": card.tips if card.tips else [],
        "pitfalls": card.pitfalls if card.pitfalls else "",
        "dosage": card.dosage if card.dosage else "",
        "level": card.level if card.level else [],
        "terrain": card.terrain if card.terrain else [],
        "self_check": card.self_check if card.self_check else [],
        "card_type": card.card_type if card.card_type else ""
    }


# 兼容性接口 - 保持與舊版API的兼容性
def process_ski_tips_request(db: Session, user_input: str, **kwargs) -> Dict[str, Any]:
    """
    處理滑雪技巧建議請求的兼容性接口
    
    保持與舊版API的兼容性
    """
    level = kwargs.get('level')
    terrain = kwargs.get('terrain')
    style = kwargs.get('style')
    
    tips = get_ski_tips(db, user_input, level, terrain, style)
    
    return {
        "status": "success",
        "recommended_cards": tips,
        "count": len(tips)
    }