"""
資料提取與處理服務 (DM-250)

實現從教練答覆中自動提取症狀描述和練習建議的流程
"""
from typing import List, Dict, Any, Optional
import re
import logging
from sqlalchemy.orm import Session
from ..models.symptom import Symptom
from ..models.practice_card import PracticeCard
from ..database.repositories import SymptomRepository, PracticeCardRepository

logger = logging.getLogger(__name__)

def extract_symptoms_from_text(text: str) -> List[Dict[str, str]]:
    """
    從文本中提取症狀信息 (DM-250.1)
    
    使用規則和NLP識別症狀關鍵詞和描述
    
    Args:
        text: 輸入文本
        
    Returns:
        List[Dict[str, str]]: 提取的症狀信息列表
    """
    try:
        symptoms = []
        
        # 定義症狀模式
        symptom_patterns = [
            r'(重心.*?太.*?後)',  # 如：重心太後
            r'(後坐|向後坐)',      # 如：後坐
            r'(無法.*?換刃)',     # 如：無法換刃
            r'(重心.*?太.*?前)',  # 如：重心太前
            r'(換刃.*?困難)',     # 如：換刃困難
            r'(轉彎.*?不.*?穩)',  # 如：轉彎不穩
            r'(速度.*?控制.*?不.*?好)', # 如：速度控制不好
            r'(平衡.*?不.*?好)',   # 如：平衡不好
            r'(姿勢.*?不.*?正確)',  # 如：姿勢不正確
        ]
        
        # 搜索症狀
        for pattern in symptom_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if match not in [s.get('name') for s in symptoms]:
                    symptoms.append({
                        'name': match.strip(),
                        'category': '技術',
                        'source_text': match.strip()
                    })
        
        # 特定的症狀關鍵詞
        specific_keywords = [
            '後坐', '重心', '換刃', '轉彎', '平衡', '姿勢', '速度控制', '壓力分配'
        ]
        
        for keyword in specific_keywords:
            if keyword in text and not any(keyword in s['name'] for s in symptoms):
                symptoms.append({
                    'name': keyword,
                    'category': '技術',
                    'source_text': keyword
                })
        
        logger.info(f"從文本中提取了 {len(symptoms)} 個症狀")
        return symptoms
        
    except Exception as e:
        logger.error(f"提取症狀時出錯: {e}")
        # 降級策略：返回空列表
        return []


def extract_practice_suggestions_from_text(text: str) -> List[Dict[str, str]]:
    """
    從文本中提取練習建議 (DM-250.2)
    
    識別動作要點、常見錯誤、建議次數
    
    Args:
        text: 輸入文本
        
    Returns:
        List[Dict[str, str]]: 提取的練習建議列表
    """
    try:
        suggestions = []
        
        # 定義建議模式
        tip_patterns = [
            r'(要點：|動作要點：)([^。]*?)[。.。]',  # 如：要點：保持重心向前
            r'(建議.*?：)([^。]*?)[。.。]',
            r'(應該.*?：)([^。]*?)[。.。]',
        ]
        
        for pattern in tip_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                suggestions.append({
                    'type': 'tip',
                    'content': match[1].strip(),
                    'source_text': match[0] + match[1]
                })
        
        # 搜索常見錯誤和建議次數
        error_patterns = [
            r'(避免|不要.*?：?)([^。]*?)[。.。]',
            r'(常見錯誤：?)([^。]*?)[。.。]',
        ]
        
        for pattern in error_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                suggestions.append({
                    'type': 'pitfall',
                    'content': match[1].strip(),
                    'source_text': match[0] + match[1]
                })
        
        dosage_patterns = [
            r'(\d+)\s*(次|趟|圈|分鐘)',
            r'每(\d+).*?[\s,，](\d+).*?[次趟圈分鐘]',
        ]
        
        for pattern in dosage_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                dosage = ''.join(match) if isinstance(match, tuple) else match
                suggestions.append({
                    'type': 'dosage',
                    'content': dosage.strip(),
                    'source_text': dosage.strip()
                })
        
        logger.info(f"從文本中提取了 {len(suggestions)} 個練習建議")
        return suggestions
        
    except Exception as e:
        logger.error(f"提取練習建議時出錯: {e}")
        # 降級策略：返回空列表
        return []


def create_structured_knowledge(symptoms: List[Dict[str, str]], 
                                suggestions: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    建立結構化知識表示 (DM-250.3)
    
    症狀 → 原因 → 練習方案的對應關係
    
    Args:
        symptoms: 症狀列表
        suggestions: 建議列表
        
    Returns:
        Dict[str, Any]: 結構化知識表示
    """
    try:
        knowledge_structure = {}
        
        for symptom in symptoms:
            symptom_name = symptom['name']
            knowledge_structure[symptom_name] = {
                'symptom': symptom,
                'related_suggestions': [],
                'practice_schemes': []
            }
            
            # 找到與症狀相關的建議
            for suggestion in suggestions:
                if suggestion['type'] == 'tip' or suggestion['type'] == 'pitfall':
                    knowledge_structure[symptom_name]['related_suggestions'].append(suggestion)
                elif suggestion['type'] == 'dosage':
                    knowledge_structure[symptom_name]['practice_schemes'].append(suggestion)
        
        logger.info(f"建立結構化知識表示，包含 {len(knowledge_structure)} 個症狀")
        return knowledge_structure
        
    except Exception as e:
        logger.error(f"建立結構化知識表示時出錯: {e}")
        # 降級策略：返回空字典
        return {}


def mark_as_pending_review(content: Dict[str, Any]) -> Dict[str, Any]:
    """
    實現人工審核機制 (DM-250.4)
    
    將自動抽取結果標記為待審核，管理者可人工確認
    
    Args:
        content: 內容
        
    Returns:
        Dict[str, Any]: 標記後的內容
    """
    try:
        content['review_status'] = 'pending'
        content['needs_human_verification'] = True
        
        logger.info("內容已標記為待審核")
        return content
        
    except Exception as e:
        logger.error(f"標記為待審核時出錯: {e}")
        # 降級策略：返回原始內容
        return content


def extract_and_structure_knowledge(text: str) -> Dict[str, Any]:
    """
    完整的知識提取和結構化流程
    
    Args:
        text: 輸入文本
        
    Returns:
        Dict[str, Any]: 完整的結構化知識
    """
    try:
        # 提取症狀
        symptoms = extract_symptoms_from_text(text)
        
        # 提取練習建議
        suggestions = extract_practice_suggestions_from_text(text)
        
        # 建立結構化知識
        structured_knowledge = create_structured_knowledge(symptoms, suggestions)
        
        # 標記為待審核
        marked_knowledge = mark_as_pending_review(structured_knowledge)
        
        # 添加源文本信息
        marked_knowledge['source_text'] = text
        marked_knowledge['extraction_timestamp'] = __import__('datetime').datetime.now().isoformat()
        
        logger.info("完成完整的知識提取和結構化流程")
        return marked_knowledge
        
    except Exception as e:
        logger.error(f"知識提取和結構化流程出錯: {e}")
        # 降級策略：返回基本結構
        return {
            'symptoms': [],
            'suggestions': [],
            'structured_knowledge': {},
            'review_status': 'error',
            'source_text': text
        }


def save_extracted_knowledge(db: Session, knowledge: Dict[str, Any]):
    """
    保存提取的知識到數據庫
    
    Args:
        db: 數據庫連接
        knowledge: 提取的知識
    """
    try:
        symptom_repo = SymptomRepository(db)
        
        # 保存症狀
        for symptom_name, data in knowledge.get('structured_knowledge', {}).items():
            symptom_data = data['symptom']
            existing_symptom = symptom_repo.get_by_name(symptom_name)
            
            if not existing_symptom:
                # 創建新症狀
                new_symptom = Symptom(
                    name=symptom_data['name'],
                    category=symptom_data['category'],
                    synonyms=[symptom_data['source_text']] if 'source_text' in symptom_data else []
                )
                symptom_repo.create(new_symptom)
            else:
                # 更新現有症狀的同義詞
                synonyms = existing_symptom.synonyms or []
                if symptom_data['source_text'] not in synonyms:
                    synonyms.append(symptom_data['source_text'])
                    symptom_repo.update(existing_symptom.id, synonyms=synonyms)
        
        logger.info(f"保存了 {len(knowledge.get('structured_knowledge', {}))} 個症狀到數據庫")
        
    except Exception as e:
        logger.error(f"保存提取的知識時出錯: {e}")
        raise


# 兼容性接口 - 保持與舊版API的兼容性
def process_data_extraction_request(text: str) -> Dict[str, Any]:
    """
    處理資料提取請求的兼容性接口
    
    保持與舊版API的兼容性
    """
    knowledge = extract_and_structure_knowledge(text)
    
    return {
        "status": "success",
        "extracted_knowledge": knowledge,
        "symptoms_count": len(knowledge.get('structured_knowledge', {}))
    }