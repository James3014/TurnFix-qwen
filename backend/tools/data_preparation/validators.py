"""
資料準備工具集驗證器

提供數據驗證和品質檢查功能
"""
import json
import logging
from typing import List, Dict, Any, Optional
from .utils import validate_json_structure

logger = logging.getLogger(__name__)

def validate_symptom_data(symptom_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    驗證症狀數據
    
    Args:
        symptom_data: 症狀數據
        
    Returns:
        Dict[str, Any]: 驗證結果
    """
    try:
        # 檢查必需字段
        required_fields = ["name", "category"]
        is_valid = validate_json_structure(symptom_data, required_fields)
        
        # 檢查症狀名稱唯一性和格式一致性
        name = symptom_data.get("name", "")
        category = symptom_data.get("category", "")
        
        # 檢查症狀名稱長度
        name_length_valid = len(name.strip()) >= 2 and len(name.strip()) <= 100
        
        # 檢查類別值域
        valid_categories = ["技術", "裝備"]
        category_valid = category in valid_categories
        
        # 檢查陣列字段
        synonyms = symptom_data.get("synonyms", [])
        level_scope = symptom_data.get("level_scope", [])
        terrain_scope = symptom_data.get("terrain_scope", [])
        style_scope = symptom_data.get("style_scope", [])
        
        # 驗證陣列字段類型
        arrays_valid = (
            isinstance(synonyms, list) and
            isinstance(level_scope, list) and
            isinstance(terrain_scope, list) and
            isinstance(style_scope, list)
        )
        
        # 總體驗證結果
        overall_valid = is_valid and name_length_valid and category_valid and arrays_valid
        
        return {
            "is_valid": overall_valid,
            "validation_details": {
                "required_fields": is_valid,
                "name_length": name_length_valid,
                "category_valid": category_valid,
                "arrays_valid": arrays_valid
            },
            "issues": []
        }
        
    except Exception as e:
        logger.error(f"驗證症狀數據時出錯: {e}")
        return {
            "is_valid": False,
            "validation_details": {
                "required_fields": False,
                "name_length": False,
                "category_valid": False,
                "arrays_valid": False
            },
            "issues": [f"驗證症狀數據時出錯: {str(e)}"]
        }

def validate_practice_card_data(card_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    驗證練習卡數據
    
    Args:
        card_data: 練習卡數據
        
    Returns:
        Dict[str, Any]: 驗證結果
    """
    try:
        # 檢查必需字段
        required_fields = ["name", "goal"]
        is_valid = validate_json_structure(card_data, required_fields)
        
        # 檢查練習卡名稱長度
        name = card_data.get("name", "")
        name_length_valid = len(name.strip()) >= 2 and len(name.strip()) <= 150
        
        # 檢查練習目標長度
        goal = card_data.get("goal", "")
        goal_length_valid = len(goal.strip()) >= 5 and len(goal.strip()) <= 500
        
        # 檢查陣列字段
        tips = card_data.get("tips", [])
        level = card_data.get("level", [])
        terrain = card_data.get("terrain", [])
        self_check = card_data.get("self_check", [])
        
        # 驗證陣列字段類型
        arrays_valid = (
            isinstance(tips, list) and
            isinstance(level, list) and
            isinstance(terrain, list) and
            isinstance(self_check, list)
        )
        
        # 總體驗證結果
        overall_valid = is_valid and name_length_valid and goal_length_valid and arrays_valid
        
        return {
            "is_valid": overall_valid,
            "validation_details": {
                "required_fields": is_valid,
                "name_length": name_length_valid,
                "goal_length": goal_length_valid,
                "arrays_valid": arrays_valid
            },
            "issues": []
        }
        
    except Exception as e:
        logger.error(f"驗證練習卡數據時出錯: {e}")
        return {
            "is_valid": False,
            "validation_details": {
                "required_fields": False,
                "name_length": False,
                "goal_length": False,
                "arrays_valid": False
            },
            "issues": [f"驗證練習卡數據時出錯: {str(e)}"]
        }

def validate_symptom_practice_mapping_data(mapping_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    驗證症狀練習卡映射數據
    
    Args:
        mapping_data: 映射數據
        
    Returns:
        Dict[str, Any]: 驗證結果
    """
    try:
        # 檢查必需字段
        required_fields = ["symptom_id", "practice_id"]
        is_valid = validate_json_structure(mapping_data, required_fields)
        
        # 檢查ID值域
        symptom_id = mapping_data.get("symptom_id", 0)
        practice_id = mapping_data.get("practice_id", 0)
        
        ids_valid = symptom_id > 0 and practice_id > 0
        
        # 檢查排序值
        order = mapping_data.get("order", 0)
        order_valid = isinstance(order, int) and order >= 0
        
        # 總體驗證結果
        overall_valid = is_valid and ids_valid and order_valid
        
        return {
            "is_valid": overall_valid,
            "validation_details": {
                "required_fields": is_valid,
                "ids_valid": ids_valid,
                "order_valid": order_valid
            },
            "issues": []
        }
        
    except Exception as e:
        logger.error(f"驗證症狀練習卡映射數據時出錯: {e}")
        return {
            "is_valid": False,
            "validation_details": {
                "required_fields": False,
                "ids_valid": False,
                "order_valid": False
            },
            "issues": [f"驗證症狀練習卡映射數據時出錯: {str(e)}"]
        }

def validate_feedback_data(feedback_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    驗證回饋數據
    
    Args:
        feedback_data: 回饋數據
        
    Returns:
        Dict[str, Any]: 驗證結果
    """
    try:
        # 檢查必需字段
        required_fields = ["session_id"]
        is_valid = validate_json_structure(feedback_data, required_fields)
        
        # 檢查會話ID值域
        session_id = feedback_data.get("session_id", 0)
        session_id_valid = session_id > 0
        
        # 檢查評分值域（如果有提供）
        rating = feedback_data.get("rating", "")
        if rating:
            valid_ratings = ["not_applicable", "partially_applicable", "applicable"]
            rating_valid = rating in valid_ratings
        else:
            rating_valid = True  # 可選字段
            
        # 檢查星數評分值域（如果有提供）
        star_rating = feedback_data.get("star_rating", 0)
        if star_rating:
            star_rating_valid = isinstance(star_rating, int) and star_rating >= 1 and star_rating <= 5
        else:
            star_rating_valid = True  # 可選字段
            
        # 總體驗證結果
        overall_valid = is_valid and session_id_valid and rating_valid and star_rating_valid
        
        return {
            "is_valid": overall_valid,
            "validation_details": {
                "required_fields": is_valid,
                "session_id_valid": session_id_valid,
                "rating_valid": rating_valid,
                "star_rating_valid": star_rating_valid
            },
            "issues": []
        }
        
    except Exception as e:
        logger.error(f"驗證回饋數據時出錯: {e}")
        return {
            "is_valid": False,
            "validation_details": {
                "required_fields": False,
                "session_id_valid": False,
                "rating_valid": False,
                "star_rating_valid": False
            },
            "issues": [f"驗證回饋數據時出錯: {str(e)}"]
        }

def generate_validation_report(validation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    生成驗證報告
    
    Args:
        validation_results: 驗證結果列表
        
    Returns:
        Dict[str, Any]: 驗證報告
    """
    try:
        total_records = len(validation_results)
        valid_records = sum(1 for result in validation_results if result.get("is_valid", False))
        invalid_records = total_records - valid_records
        
        # 記錄異常數據
        anomalies = []
        for i, result in enumerate(validation_results):
            if not result.get("is_valid", False):
                anomalies.append({
                    "record_index": i,
                    "issues": result.get("issues", [])
                })
        
        return {
            "total_records": total_records,
            "valid_records": valid_records,
            "invalid_records": invalid_records,
            "validation_rate": round(valid_records / total_records * 100, 2) if total_records > 0 else 0,
            "anomalies": anomalies
        }
        
    except Exception as e:
        logger.error(f"生成驗證報告時出錯: {e}")
        return {
            "total_records": 0,
            "valid_records": 0,
            "invalid_records": 0,
            "validation_rate": 0,
            "anomalies": []
        }