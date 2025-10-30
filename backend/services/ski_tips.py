"""
滑雪技巧建議服務

簡單直接的函數實現，避免企業級複雜度
"""
from typing import Dict, List, Optional, Any
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)

# 模擬數據 - 在實際實現中會從資料庫或RAG系統獲取
SYMPTOM_MAPPING = {
    "後坐": {"id": 1, "name": "重心太後", "category": "技術"},
    "重心": {"id": 1, "name": "重心太後", "category": "技術"},
    "不穩": {"id": 2, "name": "重心不穩", "category": "技術"},
    "晃": {"id": 2, "name": "重心不穩", "category": "技術"},
    "換刃": {"id": 3, "name": "換刃困難", "category": "技術"},
    "刃": {"id": 3, "name": "換刃困難", "category": "技術"},
}

PRACTICE_CARDS = [
    {
        "id": 101,
        "name": "J型轉彎練習",
        "goal": "完成外腳承重再過中立",
        "tips": ["視線外緣", "外腳 70–80%", "中立後換刃"],
        "pitfalls": "避免提前壓內腳",
        "dosage": "藍線 6 次/趟 ×3 趟",
        "level": ["初級", "中級"],
        "terrain": ["綠線", "藍線"],
        "self_check": ["是否在換刃前感到外腳壓力峰值？"],
        "card_type": "技術"
    },
    {
        "id": 102,
        "name": "重心轉移練習",
        "goal": "改善重心控制",
        "tips": ["身體前傾", "膝蓋彎曲", "重心保持在腳掌中心"],
        "pitfalls": "避免重心過後或過前",
        "dosage": "平地 10 次 ×3 組",
        "level": ["初級", "中級"],
        "terrain": ["綠線"],
        "self_check": ["重心是否能穩定在腳掌中心？"],
        "card_type": "基礎"
    },
    {
        "id": 201,
        "name": "基礎滑行練習",
        "goal": "提升基本滑行穩定性",
        "tips": ["膝蓋微彎", "重心稍前", "保持平衡"],
        "pitfalls": "避免僵直站立",
        "dosage": "平地 5 分鐘",
        "level": ["初級"],
        "terrain": ["綠線"],
        "self_check": ["滑行時是否感到穩定？"],
        "card_type": "基礎"
    }
]

def get_ski_tips(user_input: str, level: Optional[str] = None, 
                 terrain: Optional[str] = None, style: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    獲取滑雪技巧建議的主函數
    
    簡單直接，不做過度工程
    """
    try:
        # 1. 症狀識別 - 簡單的字符串匹配，可擴展為更複雜的NLP
        recognized_symptom = identify_symptom(user_input)
        
        # 2. 根據症狀篩選練習卡
        eligible_cards = filter_cards_by_symptom(recognized_symptom["id"])
        
        # 3. 根據用戶條件進一步篩選
        filtered_cards = filter_cards_by_conditions(eligible_cards, level, terrain, style)
        
        # 4. 排序並返回前3-5張
        ranked_cards = rank_cards(filtered_cards, level, terrain)
        
        # 5. 限制返回數量
        result_count = min(settings.MAX_PRACTICE_CARDS, 
                          max(settings.MIN_PRACTICE_CARDS, len(ranked_cards)))
        return ranked_cards[:result_count]
        
    except Exception as e:
        logger.error(f"獲取滑雪建議時出錯: {e}")
        # 降級策略：返回通用建議
        return get_default_tips()

def identify_symptom(input_text: str) -> Dict[str, Any]:
    """
    識別症狀 - 簡單實現，可擴展為更複雜的AI模型
    """
    input_lower = input_text.lower()
    
    # 簡單的關鍵詞匹配
    for keyword, symptom in SYMPTOM_MAPPING.items():
        if keyword in input_lower:
            return symptom
    
    # 默認返回一般問題
    return {"id": 0, "name": "一般技術問題", "category": "技術"}

def filter_cards_by_symptom(symptom_id: int) -> List[Dict[str, Any]]:
    """
    根據症狀ID篩選練習卡
    """
    # 在實際實現中，這會從資料庫或RAG系統獲取相關卡片
    return [card for card in PRACTICE_CARDS if card["id"] in [101, 102]]

def filter_cards_by_conditions(
    cards: List[Dict[str, Any]], 
    level: Optional[str], 
    terrain: Optional[str], 
    style: Optional[str]
) -> List[Dict[str, Any]]:
    """
    根據用戶條件篩選練習卡
    """
    filtered_cards = []
    
    for card in cards:
        # 等級篩選
        if level and level in card.get("level", []) and len(card["level"]) > 0:
            pass  # 條件匹配
        elif level and len(card["level"]) > 0:
            continue  # 條件不匹配且卡片有等級限制
        
        # 地形篩選
        if terrain and terrain in card.get("terrain", []) and len(card["terrain"]) > 0:
            pass  # 條件匹配
        elif terrain and len(card["terrain"]) > 0:
            continue  # 條件不匹配且卡片有地形限制
        
        filtered_cards.append(card)
    
    # 如果篩選後為空，返回原列表（降級策略）
    return filtered_cards if filtered_cards else cards

def rank_cards(cards: List[Dict[str, Any]], level: Optional[str], terrain: Optional[str]) -> List[Dict[str, Any]]:
    """
    根據條件對練習卡進行排序
    """
    def sort_key(card):
        score = 0
        
        # 根據等級匹配加分
        if level and level in card.get("level", []):
            score += 10
            
        # 根據地形匹配加分
        if terrain and terrain in card.get("terrain", []):
            score += 5
            
        # 根據卡片ID作為最後排序標準
        score += card["id"] * 0.01
        
        return -score  # 降序排序
    
    return sorted(cards, key=sort_key)

def get_default_tips() -> List[Dict[str, Any]]:
    """
    返回默認建議（降級策略）
    """
    return [card for card in PRACTICE_CARDS if card["id"] == 201]