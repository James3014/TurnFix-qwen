"""
簡化版資料模型

使用字典型結構而非複雜的 Pydantic 模型
保持簡單直接，避免過度工程
"""
from typing import Dict, List, Optional, Any

# 症狀模型
def create_symptom_model(
    id: int,
    name: str,
    synonyms: Optional[List[str]] = None,
    level_scope: Optional[List[str]] = None,
    terrain_scope: Optional[List[str]] = None,
    style_scope: Optional[List[str]] = None,
    category: str = "技術"
) -> Dict[str, Any]:
    """
    創建症狀模型
    
    使用字典型結構而非複雜的 Pydantic 模型
    保持簡單直接，避免過度工程
    """
    return {
        "id": id,
        "name": name,
        "synonyms": synonyms or [],
        "level_scope": level_scope or [],
        "terrain_scope": terrain_scope or [],
        "style_scope": style_scope or [],
        "category": category
    }

# 練習卡模型
def create_practice_card_model(
    id: int,
    name: str,
    goal: str,
    tips: Optional[List[str]] = None,
    pitfalls: str = "",
    dosage: str = "",
    level: Optional[List[str]] = None,
    terrain: Optional[List[str]] = None,
    self_check: Optional[List[str]] = None,
    card_type: str = "基礎"
) -> Dict[str, Any]:
    """
    創建練習卡模型
    
    使用字典型結構而非複雜的 Pydantic 模型
    保持簡單直接，避免過度工程
    """
    return {
        "id": id,
        "name": name,
        "goal": goal,
        "tips": tips or [],
        "pitfalls": pitfalls,
        "dosage": dosage,
        "level": level or [],
        "terrain": terrain or [],
        "self_check": self_check or [],
        "card_type": card_type
    }

# 會話模型
def create_session_model(
    id: int,
    user_type: str = "學員",
    input_text: str = "",
    level_slot: Optional[str] = None,
    terrain_slot: Optional[str] = None,
    style_slot: Optional[str] = None,
    chosen_symptom_id: int = 0,
    feedback_rating: Optional[str] = None,
    feedback_text: Optional[str] = None
) -> Dict[str, Any]:
    """
    創建會話模型
    
    使用字典型結構而非複雜的 Pydantic 模型
    保持簡單直接，避免過度工程
    """
    return {
        "id": id,
        "user_type": user_type,
        "input_text": input_text,
        "level_slot": level_slot,
        "terrain_slot": terrain_slot,
        "style_slot": style_slot,
        "chosen_symptom_id": chosen_symptom_id,
        "feedback_rating": feedback_rating,
        "feedback_text": feedback_text
    }

# 症狀練習卡映射模型
def create_symptom_practice_mapping_model(
    symptom_id: int,
    practice_id: int,
    order: int = 0
) -> Dict[str, Any]:
    """
    創建症狀練習卡映射模型
    
    使用字典型結構而非複雜的 Pydantic 模型
    保持簡單直接，避免過度工程
    """
    return {
        "symptom_id": symptom_id,
        "practice_id": practice_id,
        "order": order
    }