"""
資料準備工具集抽取器

提供知識抽取和結構化處理功能
"""
import json
import logging
from typing import List, Dict, Any, Optional
import re
from .utils import clean_text, extract_keywords

logger = logging.getLogger(__name__)

def extract_symptoms_from_coach_response(text: str) -> List[Dict[str, Any]]:
    """
    從教練答覆中抽取症狀描述 (DM-250.1)
    
    Args:
        text: 教練答覆文本
        
    Returns:
        List[Dict[str, Any]]: 抽取的症狀描述列表
    """
    try:
        # 清洗文本
        cleaned_text = clean_text(text)
        
        # 使用規則和NLP識別症狀關鍵詞和描述
        symptoms = []
        
        # 症狀關鍵詞模式
        symptom_patterns = [
            r'(?:症狀|問題|困難)[:：\s]*([^\n\r。！？]+)',
            r'(?:症狀描述|問題描述|困難描述)[:：\s]*([^\n\r。！？]+)',
            r'(?:主要問題|核心問題)[:：\s]*([^\n\r。！？]+)',
        ]
        
        # 尋找症狀描述
        for pattern in symptom_patterns:
            matches = re.findall(pattern, cleaned_text)
            for match in matches:
                symptoms.append({
                    "description": match.strip(),
                    "confidence": 0.8  # 預設置信度
                })
        
        # 如果沒找到特定模式，使用一般關鍵詞匹配
        if not symptoms:
            keywords = ["後坐", "重心", "不穩", "晃", "換刃", "刃"]
            matched_keywords = extract_keywords(cleaned_text, keywords)
            
            if matched_keywords:
                symptoms.append({
                    "description": " ".join(matched_keywords),
                    "confidence": 0.6  # 一般置信度
                })
        
        return symptoms
        
    except Exception as e:
        logger.error(f"從教練答覆中抽取症狀描述時出錯: {e}")
        return []

def extract_practice_suggestions_from_coach_response(text: str) -> List[Dict[str, Any]]:
    """
    從教練答覆中抽取練習建議 (DM-250.2)
    
    Args:
        text: 教練答覆文本
        
    Returns:
        List[Dict[str, Any]]: 抽取的練習建議列表
    """
    try:
        # 清洗文本
        cleaned_text = clean_text(text)
        
        # 使用規則識別動作要點、常見錯誤、建議次數
        suggestions = []
        
        # 動作要點模式
        tips_patterns = [
            r'(?:動作要點|練習要點|關鍵要點)[:：\s]*([^\n\r。！？]+)',
            r'(?:要點|重點)[:：\s]*([^\n\r。！？]+)',
        ]
        
        # 常見錯誤模式
        pitfalls_patterns = [
            r'(?:常見錯誤|錯誤修正|需要注意)[:：\s]*([^\n\r。！？]+)',
            r'(?:避免|不要)[:：\s]*([^\n\r。！？]+)',
        ]
        
        # 建議次數模式
        dosage_patterns = [
            r'(?:建議次數|建議時長|練習次數)[:：\s]*([^\n\r。！？]+)',
            r'(?:次數|時長)[:：\s]*([^\n\r。！？]+)',
        ]
        
        # 抽取動作要點
        tips = []
        for pattern in tips_patterns:
            matches = re.findall(pattern, cleaned_text)
            for match in matches:
                tips.extend([tip.strip() for tip in match.split("、") if tip.strip()])
        
        # 抽取常見錯誤
        pitfalls = []
        for pattern in pitfalls_patterns:
            matches = re.findall(pattern, cleaned_text)
            for match in matches:
                pitfalls.append(match.strip())
        
        # 抽取建議次數
        dosages = []
        for pattern in dosage_patterns:
            matches = re.findall(pattern, cleaned_text)
            for match in matches:
                dosages.append(match.strip())
        
        # 組裝建議
        if tips or pitfalls or dosages:
            suggestions.append({
                "tips": tips,
                "pitfalls": " ".join(pitfalls) if pitfalls else "",
                "dosage": " ".join(dosages) if dosages else "",
                "confidence": 0.8 if tips else 0.6
            })
        
        return suggestions
        
    except Exception as e:
        logger.error(f"從教練答覆中抽取練習建議時出錯: {e}")
        return []

def create_structured_knowledge_representation(
    symptoms: List[Dict[str, Any]], 
    suggestions: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    建立結構化知識表示 (DM-250.3)
    
    Args:
        symptoms: 症狀列表
        suggestions: 練習建議列表
        
    Returns:
        Dict[str, Any]: 結構化知識表示
    """
    try:
        # 建立症狀→原因→練習方案的對應關係
        knowledge_structure = {
            "symptom_causes_solutions": []
        }
        
        # 為每個症狀建立對應關係
        for symptom in symptoms:
            knowledge_structure["symptom_causes_solutions"].append({
                "symptom": symptom["description"],
                "confidence": symptom["confidence"],
                "solutions": [
                    {
                        "tips": suggestion.get("tips", []),
                        "pitfalls": suggestion.get("pitfalls", ""),
                        "dosage": suggestion.get("dosage", ""),
                        "confidence": suggestion["confidence"]
                    }
                    for suggestion in suggestions
                ]
            })
        
        return knowledge_structure
        
    except Exception as e:
        logger.error(f"建立結構化知識表示時出錯: {e}")
        return {
            "symptom_causes_solutions": []
        }

def extract_knowledge_from_coach_response(text: str) -> Dict[str, Any]:
    """
    從教練答覆中自動提取知識 (DM-250)
    
    Args:
        text: 教練答覆文本
        
    Returns:
        Dict[str, Any]: 提取的知識
    """
    try:
        # 抽取症狀描述
        symptoms = extract_symptoms_from_coach_response(text)
        
        # 抽取練習建議
        suggestions = extract_practice_suggestions_from_coach_response(text)
        
        # 建立結構化知識表示
        knowledge_structure = create_structured_knowledge_representation(symptoms, suggestions)
        
        # 標記為待審核狀態
        return {
            "status": "pending_review",
            "symptoms": symptoms,
            "suggestions": suggestions,
            "knowledge_structure": knowledge_structure
        }
        
    except Exception as e:
        logger.error(f"從教練答覆中提取知識時出錯: {e}")
        return {
            "status": "error",
            "message": f"從教練答覆中提取知識時出錯: {str(e)}",
            "symptoms": [],
            "suggestions": [],
            "knowledge_structure": {}
        }

def extract_knowledge_from_video_transcript(text: str) -> Dict[str, Any]:
    """
    從影片逐字稿中自動提取知識
    
    Args:
        text: 影片逐字稿文本
        
    Returns:
        Dict[str, Any]: 提取的知識
    """
    try:
        # 清洗文本
        cleaned_text = clean_text(text)
        
        # 抽取症狀描述
        symptoms = extract_symptoms_from_video_transcript(cleaned_text)
        
        # 抽取練習建議
        suggestions = extract_practice_suggestions_from_video_transcript(cleaned_text)
        
        # 建立結構化知識表示
        knowledge_structure = create_structured_knowledge_representation(symptoms, suggestions)
        
        # 標記為待審核狀態
        return {
            "status": "pending_review",
            "symptoms": symptoms,
            "suggestions": suggestions,
            "knowledge_structure": knowledge_structure
        }
        
    except Exception as e:
        logger.error(f"從影片逐字稿中提取知識時出錯: {e}")
        return {
            "status": "error",
            "message": f"從影片逐字稿中提取知識時出錯: {str(e)}",
            "symptoms": [],
            "suggestions": [],
            "knowledge_structure": {}
        }

def extract_symptoms_from_video_transcript(text: str) -> List[Dict[str, Any]]:
    """
    從影片逐字稿中抽取症狀描述
    
    Args:
        text: 影片逐字稿文本
        
    Returns:
        List[Dict[str, Any]]: 抽取的症狀描述列表
    """
    try:
        # 使用規則和NLP識別症狀關鍵詞和描述
        symptoms = []
        
        # 症狀關鍵詞模式
        symptom_patterns = [
            r'(?:症狀|問題|困難)[:：\s]*([^\n\r。！？]+)',
            r'(?:主要問題|核心問題)[:：\s]*([^\n\r。！？]+)',
        ]
        
        # 尋找症狀描述
        for pattern in symptom_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                symptoms.append({
                    "description": match.strip(),
                    "confidence": 0.7  # 預設置信度
                })
        
        # 如果沒找到特定模式，使用一般關鍵詞匹配
        if not symptoms:
            keywords = ["後坐", "重心", "不穩", "晃", "換刃", "刃"]
            matched_keywords = extract_keywords(text, keywords)
            
            if matched_keywords:
                symptoms.append({
                    "description": " ".join(matched_keywords),
                    "confidence": 0.5  # 一般置信度
                })
        
        return symptoms
        
    except Exception as e:
        logger.error(f"從影片逐字稿中抽取症狀描述時出錯: {e}")
        return []

def extract_practice_suggestions_from_video_transcript(text: str) -> List[Dict[str, Any]]:
    """
    從影片逐字稿中抽取練習建議
    
    Args:
        text: 影片逐字稿文本
        
    Returns:
        List[Dict[str, Any]]: 抽取的練習建議列表
    """
    try:
        # 使用規則識別動作要點、常見錯誤、建議次數
        suggestions = []
        
        # 動作要點模式
        tips_patterns = [
            r'(?:動作要點|練習要點|關鍵要點)[:：\s]*([^\n\r。！？]+)',
            r'(?:要點|重點)[:：\s]*([^\n\r。！？]+)',
        ]
        
        # 常見錯誤模式
        pitfalls_patterns = [
            r'(?:常見錯誤|錯誤修正|需要注意)[:：\s]*([^\n\r。！？]+)',
            r'(?:避免|不要)[:：\s]*([^\n\r。！？]+)',
        ]
        
        # 建議次數模式
        dosage_patterns = [
            r'(?:建議次數|建議時長|練習次數)[:：\s]*([^\n\r。！？]+)',
            r'(?:次數|時長)[:：\s]*([^\n\r。！？]+)',
        ]
        
        # 抽取動作要點
        tips = []
        for pattern in tips_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                tips.extend([tip.strip() for tip in match.split("、") if tip.strip()])
        
        # 抽取常見錯誤
        pitfalls = []
        for pattern in pitfalls_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                pitfalls.append(match.strip())
        
        # 抽取建議次數
        dosages = []
        for pattern in dosage_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                dosages.append(match.strip())
        
        # 組裝建議
        if tips or pitfalls or dosages:
            suggestions.append({
                "tips": tips,
                "pitfalls": " ".join(pitfalls) if pitfalls else "",
                "dosage": " ".join(dosages) if dosages else "",
                "confidence": 0.7 if tips else 0.5
            })
        
        return suggestions
        
    except Exception as e:
        logger.error(f"從影片逐字稿中抽取練習建議時出錯: {e}")
        return []