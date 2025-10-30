"""
自適應追問服務 (API-203)

實現 LLM 輔助的置信度判斷和追問問題生成
"""
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from ..models.symptom import Symptom
from ..models.practice_card import PracticeCard
import json
import logging

logger = logging.getLogger(__name__)

# 通用問題庫 (模擬實現)
COMMON_FOLLOWUP_QUESTIONS = [
    {"question": "請問您目前的滑雪等級是？(初級/中級/高級)", "type": "level"},
    {"question": "您通常在哪種地形滑行？(綠線/藍線/黑線)", "type": "terrain"},
    {"question": "您滑行的主要風格是？(平花/自由式/競速)", "type": "style"},
    {"question": "能否更詳細描述您遇到的問題？", "type": "clarification"},
    {"question": "這個問題在什麼情況下特別明顯？", "type": "clarification"},
    {"question": "您覺得造成這個問題的主要原因可能是什麼？", "type": "clarification"},
]

def assess_confidence(user_input: str, recognized_symptom: Symptom, 
                     level: Optional[str], terrain: Optional[str], style: Optional[str]) -> Tuple[float, List[str]]:
    """
    評估症狀辨識的置信度 (API-203.1)
    
    使用簡單規則而非真實LLM來模擬置信度判斷
    
    Args:
        user_input: 使用者輸入的口語問題
        recognized_symptom: 已辨識的症狀
        level: 使用者提供的等級資訊
        terrain: 使用者提供的地形資訊
        style: 使用者提供的滑行風格資訊
        
    Returns:
        Tuple[float, List[str]]: (置信度分數 0-1, 缺失資訊列表)
    """
    confidence = 1.0
    missing_slots = []
    
    # 計算置信度分數
    if len(user_input.strip()) < 10:
        confidence -= 0.3  # 描述過於簡短
        
    # 檢查缺失 Slot 資訊
    if not level:
        missing_slots.append("level")
        confidence -= 0.15
    if not terrain:
        missing_slots.append("terrain")
        confidence -= 0.15
    if not style:
        missing_slots.append("style")
        confidence -= 0.10
        
    # 如果有多個同義症狀競爭，降低置信度
    # 這裡簡化處理，假設如果有同義詞則競爭較激烈
    if recognized_symptom.synonyms and len(recognized_symptom.synonyms) > 2:
        confidence -= 0.2
        
    # 確保置信度在 0-1 範圍內
    confidence = max(0.0, min(1.0, confidence))
    
    return confidence, missing_slots

def generate_followup_questions(confidence: float, missing_slots: List[str], 
                              user_input: str) -> List[Dict[str, str]]:
    """
    生成追問問題 (API-203.2)
    
    根據置信度和缺失資訊生成追問問題
    
    Args:
        confidence: 置信度分數
        missing_slots: 缺失資訊列表
        user_input: 使用者輸入
        
    Returns:
        List[Dict[str, str]]: 追問問題列表
    """
    questions = []
    
    # 如果置信度低於 0.7，需要追問
    if confidence < 0.7:
        # 優先使用通用問題庫
        if "level" in missing_slots:
            questions.append({"question": "請問您目前的滑雪等級是？(初級/中級/高級)", "type": "level"})
        if "terrain" in missing_slots:
            questions.append({"question": "您通常在哪種地形滑行？(綠線/藍線/黑線)", "type": "terrain"})
        if "style" in missing_slots:
            questions.append({"question": "您滑行的主要風格是？(平花/自由式/競速)", "type": "style"})
            
        # 如果還需要更多問題或描述太簡短
        if len(questions) < 2 or len(user_input.strip()) < 15:
            # 添加澄清問題
            questions.append({"question": "能否更詳細描述您遇到的問題？", "type": "clarification"})
            
        # 限制最多 2 個問題
        questions = questions[:2]
        
    return questions

def get_followup_needs(db: Session, user_input: str, 
                      level: Optional[str], terrain: Optional[str], style: Optional[str]) -> Dict[str, any]:
    """
    獲取是否需要追問及追問問題 (API-203 主函數)
    
    Args:
        db: 資料庫會話
        user_input: 使用者輸入的口語問題
        level: 使用者提供的等級資訊
        terrain: 使用者提供的地形資訊
        style: 使用者提供的滑行風格資訊
        
    Returns:
        Dict: 是否需要追問及追問問題
    """
    try:
        # 首先識別症狀
        from ..database.repositories import SymptomRepository
        symptom_repo = SymptomRepository(db)
        
        # 簡單的症狀識別實現
        recognized_symptom = identify_simple_symptom(symptom_repo, user_input)
        
        # 評估置信度
        confidence, missing_slots = assess_confidence(user_input, recognized_symptom, level, terrain, style)
        
        # 判斷是否需要追問
        need_followup = confidence < 0.7 and (missing_slots or len(user_input.strip()) < 15)
        
        # 生成追問問題
        questions = []
        if need_followup:
            questions = generate_followup_questions(confidence, missing_slots, user_input)
        
        return {
            "need_followup": need_followup,
            "confidence": confidence,
            "missing_slots": missing_slots,
            "questions": questions
        }
        
    except Exception as e:
        logger.error(f"評估追問需求時出錯: {e}")
        # 降級策略：不追問
        return {
            "need_followup": False,
            "confidence": 1.0,
            "missing_slots": [],
            "questions": []
        }

def identify_simple_symptom(symptom_repo, input_text: str):
    """
    簡單的症狀識別實現
    
    Args:
        symptom_repo: 症狀倉儲
        input_text: 輸入文本
        
    Returns:
        Symptom: 識別的症狀
    """
    input_lower = input_text.lower()
    
    # 檢查同義詞庫
    symptom = symptom_repo.find_by_synonym(input_text)
    if symptom:
        return symptom
    
    # 簡單的關鍵詞匹配
    keywords = ["後坐", "重心", "不穩", "晃", "換刃", "刃"]
    for keyword in keywords:
        if keyword in input_lower:
            # 尋找包含此關鍵詞的症狀
            all_symptoms = symptom_repo.get_all()
            for s in all_symptoms:
                if keyword in s.name.lower() or (s.synonyms and keyword in str(s.synonyms).lower()):
                    return s
    
    # 默認返回一般問題
    from ..models.symptom import Symptom as SymptomModel
    default_symptom = SymptomModel(
        name="一般技術問題",
        category="技術"
    )
    return default_symptom