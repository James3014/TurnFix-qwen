"""
資料準備工具集實用函數

提供通用的資料處理和驗證函數
"""
import json
import logging
from typing import List, Dict, Any, Optional
import re

logger = logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """
    清洗文本
    
    Args:
        text: 原始文本
        
    Returns:
        str: 清洗後的文本
    """
    try:
        # 移除多餘空白
        cleaned_text = re.sub(r'\s+', ' ', text.strip())
        
        # 移除特殊字符
        cleaned_text = re.sub(r'[^\w\s\u4e00-\u9fff.,!?;:()\[\]{}\-]', '', cleaned_text)
        
        return cleaned_text
        
    except Exception as e:
        logger.error(f"清洗文本時出錯: {e}")
        return text

def extract_keywords(text: str, keywords: List[str]) -> List[str]:
    """
    從文本中提取關鍵詞
    
    Args:
        text: 原始文本
        keywords: 關鍵詞列表
        
    Returns:
        List[str]: 匹配的關鍵詞
    """
    try:
        matched_keywords = []
        text_lower = text.lower()
        
        for keyword in keywords:
            if keyword.lower() in text_lower:
                matched_keywords.append(keyword)
        
        return matched_keywords
        
    except Exception as e:
        logger.error(f"提取關鍵詞時出錯: {e}")
        return []

def validate_json_structure(data: Dict[str, Any], required_fields: List[str]) -> bool:
    """
    驗證JSON結構
    
    Args:
        data: JSON數據
        required_fields: 必需字段列表
        
    Returns:
        bool: 驗證結果
    """
    try:
        for field in required_fields:
            if field not in data:
                return False
        return True
        
    except Exception as e:
        logger.error(f"驗證JSON結構時出錯: {e}")
        return False

def format_timestamp(timestamp: str) -> str:
    """
    格式化時間戳記
    
    Args:
        timestamp: 原始時間戳記
        
    Returns:
        str: 格式化後的時間戳記
    """
    try:
        # 移除時間戳記中的格式化符號
        formatted_timestamp = re.sub(r'[\[\]]', '', timestamp.strip())
        return formatted_timestamp
        
    except Exception as e:
        logger.error(f"格式化時間戳記時出錯: {e}")
        return timestamp

def detect_language(text: str) -> str:
    """
    檢測語言
    
    Args:
        text: 文本
        
    Returns:
        str: 檢測到的語言代碼
    """
    try:
        # 簡化實現：檢查是否包含中文字符
        chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
        if len(chinese_chars) > len(text) * 0.5:
            return "zh"
        else:
            return "en"
            
    except Exception as e:
        logger.error(f"檢測語言時出錯: {e}")
        return "unknown"

def split_into_segments(text: str, delimiter: str = '\n\n') -> List[str]:
    """
    分割文本為段落
    
    Args:
        text: 原始文本
        delimiter: 分隔符
        
    Returns:
        List[str]: 分段後的文本列表
    """
    try:
        segments = text.split(delimiter)
        # 移除空段落和過短段落
        return [s.strip() for s in segments if s.strip() and len(s.strip()) > 10]
        
    except Exception as e:
        logger.error(f"分割文本時出錯: {e}")
        return [text]

def merge_segments(segments: List[str], max_length: int = 500) -> List[str]:
    """
    合併段落以確保足夠的上下文
    
    Args:
        segments: 段落列表
        max_length: 最大長度
        
    Returns:
        List[str]: 合併後的段落列表
    """
    try:
        merged_segments = []
        current_segment = ""
        
        for segment in segments:
            if len(current_segment) + len(segment) <= max_length:
                current_segment += segment + " "
            else:
                if current_segment:
                    merged_segments.append(current_segment.strip())
                current_segment = segment + " "
        
        if current_segment:
            merged_segments.append(current_segment.strip())
            
        return merged_segments
        
    except Exception as e:
        logger.error(f"合併段落時出錯: {e}")
        return segments

def normalize_units(text: str) -> str:
    """
    標準化單位
    
    Args:
        text: 原始文本
        
    Returns:
        str: 標準化後的文本
    """
    try:
        # 標準化重量單位
        text = re.sub(r'(\d+)\s*kg', r'\1 公斤', text, flags=re.IGNORECASE)
        text = re.sub(r'(\d+)\s*m', r'\1 公尺', text, flags=re.IGNORECASE)
        text = re.sub(r'(\d+)\s*cm', r'\1 公分', text, flags=re.IGNORECASE)
        
        return text
        
    except Exception as e:
        logger.error(f"標準化單位時出錯: {e}")
        return text

def normalize_dates(text: str) -> str:
    """
    正規化日期格式
    
    Args:
        text: 原始文本
        
    Returns:
        str: 正規化後的文本
    """
    try:
        # 將各種日期格式統一為 YYYY-MM-DD
        text = re.sub(r'\d{4}/\d{1,2}/\d{1,2}', lambda m: m.group().replace('/', '-'), text)
        text = re.sub(r'\d{1,2}/\d{1,2}/\d{4}', lambda m: '-'.join(reversed(m.group().split('/'))), text)
        
        return text
        
    except Exception as e:
        logger.error(f"正規化日期格式時出錯: {e}")
        return text