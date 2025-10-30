"""
資料準備工具集分析器

提供知識分析和品質檢查功能
"""
import json
import logging
from typing import List, Dict, Any, Optional
from .models import (
    ExtractedKnowledge,
    SymptomValidationResult,
    PracticeCardValidationResult,
    SymptomPracticeMappingValidationResult,
    FeedbackValidationResult,
    ValidationReport
)
from .validators import (
    validate_symptom_data,
    validate_practice_card_data,
    validate_symptom_practice_mapping_data,
    validate_feedback_data
)

logger = logging.getLogger(__name__)

def analyze_extracted_knowledge(knowledge_data: ExtractedKnowledge) -> ValidationReport:
    """
    分析提取的知識品質 (TOOL-103)
    
    Args:
        knowledge_data: 提取的知識數據
        
    Returns:
        ValidationReport: 驗證報告
    """
    try:
        # 初始化統計數據
        total_records = 0
        valid_records = 0
        invalid_records = 0
        anomalies = []
        
        # 分析症狀數據
        for symptom in knowledge_data.symptoms:
            total_records += 1
            validation_result = validate_symptom_data(symptom.dict())
            if validation_result["is_valid"]:
                valid_records += 1
            else:
                invalid_records += 1
                anomalies.append({
                    "type": "symptom",
                    "record": symptom.dict(),
                    "issues": validation_result["issues"]
                })
        
        # 分析練習建議數據
        for suggestion in knowledge_data.suggestions:
            total_records += 1
            validation_result = validate_practice_card_data(suggestion.dict())
            if validation_result["is_valid"]:
                valid_records += 1
            else:
                invalid_records += 1
                anomalies.append({
                    "type": "practice_card",
                    "record": suggestion.dict(),
                    "issues": validation_result["issues"]
                })
        
        # 計算驗證率
        validation_rate = (valid_records / total_records * 100) if total_records > 0 else 0
        
        return ValidationReport(
            total_records=total_records,
            valid_records=valid_records,
            invalid_records=invalid_records,
            validation_rate=round(validation_rate, 2),
            anomalies=anomalies
        )
        
    except Exception as e:
        logger.error(f"分析提取的知識品質時出錯: {e}")
        return ValidationReport(
            total_records=0,
            valid_records=0,
            invalid_records=0,
            validation_rate=0,
            anomalies=[]
        )

def validate_knowledge_quality(knowledge_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    驗證知識品質 (TOOL-103.1 到 TOOL-103.3)
    
    Args:
        knowledge_data: 知識數據
        
    Returns:
        Dict[str, Any]: 驗證報告
    """
    try:
        # 檢查症狀名稱唯一性和格式一致性 (TOOL-103.1)
        symptom_names = [symptom.get("description", "") for symptom in knowledge_data.get("symptoms", [])]
        unique_symptoms = len(set(symptom_names))
        total_symptoms = len(symptom_names)
        
        # 驗證練習建議的完整性 (TOOL-103.2)
        practice_tips = [suggestion.get("tips", []) for suggestion in knowledge_data.get("suggestions", [])]
        complete_tips = all(len(tips) > 0 for tips in practice_tips)
        
        # 生成驗證報告，標記異常記錄 (TOOL-103.3)
        report = {
            "validation_status": "success",
            "symptom_uniqueness": {
                "unique_count": unique_symptoms,
                "total_count": total_symptoms,
                "consistency": unique_symptoms == total_symptoms
            },
            "practice_completeness": {
                "complete_tips": complete_tips,
                "tip_count": sum(len(tips) for tips in practice_tips)
            },
            "anomalies": []
        }
        
        # 檢查異常記錄
        if not complete_tips:
            report["anomalies"].append("練習建議缺少必要的要點")
        
        if unique_symptoms != total_symptoms:
            report["anomalies"].append("症狀名稱存在重複")
        
        # 檢查描述長度
        for symptom_name in symptom_names:
            if len(symptom_name) < 2:
                report["anomalies"].append(f"症狀描述過短: {symptom_name}")
        
        for tips in practice_tips:
            if len(tips) < 1:
                report["anomalies"].append("練習建議要點過少")
        
        return report
        
    except Exception as e:
        logger.error(f"驗證知識品質時出錯: {e}")
        # 降級策略：返回錯誤報告
        return {
            "validation_status": "error",
            "message": f"驗證知識品質時出錯: {str(e)}"
        }

def check_data_consistency(knowledge_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    檢查資料一致性 (TOOL-103.4)
    
    Args:
        knowledge_data: 知識數據
        
    Returns:
        Dict[str, Any]: 一致性檢查報告
    """
    try:
        report = {
            "consistency_status": "success",
            "checks": []
        }
        
        # 檢查症狀和練習建議的關聯性
        symptoms = knowledge_data.get("symptoms", [])
        suggestions = knowledge_data.get("suggestions", [])
        
        if len(symptoms) > 0 and len(suggestions) > 0:
            report["checks"].append({
                "type": "symptom_practice_mapping",
                "status": "passed",
                "message": "症狀和練習建議存在關聯"
            })
        elif len(symptoms) > 0 or len(suggestions) > 0:
            report["checks"].append({
                "type": "symptom_practice_mapping",
                "status": "warning",
                "message": "症狀和練習建議不匹配"
            })
        else:
            report["checks"].append({
                "type": "symptom_practice_mapping",
                "status": "failed",
                "message": "缺少症狀和練習建議"
            })
        
        # 檢查結構化知識表示
        knowledge_structure = knowledge_data.get("knowledge_structure", {})
        if knowledge_structure and "symptom_causes_solutions" in knowledge_structure:
            report["checks"].append({
                "type": "knowledge_structure",
                "status": "passed",
                "message": "結構化知識表示完整"
            })
        else:
            report["checks"].append({
                "type": "knowledge_structure",
                "status": "warning",
                "message": "結構化知識表示不完整"
            })
        
        return report
        
    except Exception as e:
        logger.error(f"檢查資料一致性時出錯: {e}")
        return {
            "consistency_status": "error",
            "message": f"檢查資料一致性時出錯: {str(e)}",
            "checks": []
        }

def generate_quality_report(knowledge_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    生成品質報告 (TOOL-103.5)
    
    Args:
        knowledge_data: 知識數據
        
    Returns:
        Dict[str, Any]: 品質報告
    """
    try:
        # 驗證知識品質
        validation_report = validate_knowledge_quality(knowledge_data)
        
        # 檢查資料一致性
        consistency_report = check_data_consistency(knowledge_data)
        
        # 生成綜合報告
        quality_report = {
            "quality_status": "success",
            "validation": validation_report,
            "consistency": consistency_report,
            "summary": {
                "total_symptoms": len(knowledge_data.get("symptoms", [])),
                "total_suggestions": len(knowledge_data.get("suggestions", [])),
                "quality_score": calculate_quality_score(validation_report, consistency_report)
            }
        }
        
        return quality_report
        
    except Exception as e:
        logger.error(f"生成品質報告時出錯: {e}")
        return {
            "quality_status": "error",
            "message": f"生成品質報告時出錯: {str(e)}",
            "validation": {},
            "consistency": {},
            "summary": {
                "total_symptoms": 0,
                "total_suggestions": 0,
                "quality_score": 0
            }
        }

def calculate_quality_score(validation_report: Dict[str, Any], consistency_report: Dict[str, Any]) -> float:
    """
    計算品質分數
    
    Args:
        validation_report: 驗證報告
        consistency_report: 一致性報告
        
    Returns:
        float: 品質分數 (0-100)
    """
    try:
        score = 100.0
        
        # 根據驗證結果調整分數
        if validation_report.get("validation_status") == "error":
            score -= 30
        elif validation_report.get("anomalies"):
            score -= len(validation_report["anomalies"]) * 5
            
        # 根據一致性檢查調整分數
        consistency_checks = consistency_report.get("checks", [])
        failed_checks = [check for check in consistency_checks if check.get("status") == "failed"]
        warning_checks = [check for check in consistency_checks if check.get("status") == "warning"]
        
        score -= len(failed_checks) * 10
        score -= len(warning_checks) * 5
        
        # 確保分數在 0-100 範圍內
        return max(0.0, min(100.0, score))
        
    except Exception as e:
        logger.error(f"計算品質分數時出錯: {e}")
        return 0.0