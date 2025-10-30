"""
資料準備工具集導入器

提供知識庫導入功能
"""
import json
import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from ...database.base import get_db
from ...database.repositories import (
    SymptomRepository,
    PracticeCardRepository,
    SymptomPracticeMappingRepository
)
from ...models.symptom import Symptom
from ...models.practice_card import PracticeCard
from ...models.symptom_practice_mapping import SymptomPracticeMapping
from .models import ExtractedKnowledge
from .analyzer import analyze_extracted_knowledge

logger = logging.getLogger(__name__)

def import_knowledge_to_database(
    knowledge_data: ExtractedKnowledge,
    db: Session
) -> Dict[str, Any]:
    """
    將知識導入到資料庫 (TOOL-105)
    
    Args:
        knowledge_data: 提取的知識數據
        db: 資料庫會話
        
    Returns:
        Dict[str, Any]: 導入結果
    """
    try:
        # 初始化倉儲
        symptom_repo = SymptomRepository(db)
        practice_repo = PracticeCardRepository(db)
        mapping_repo = SymptomPracticeMappingRepository(db)
        
        # 分析知識品質
        validation_report = analyze_extracted_knowledge(knowledge_data)
        
        if validation_report.invalid_records > 0:
            logger.warning(f"知識數據存在 {validation_report.invalid_records} 個無效記錄")
        
        # 導入症狀
        imported_symptoms = []
        for symptom in knowledge_data.symptoms:
            new_symptom = Symptom(
                name=symptom.name,
                category=symptom.category,
                synonyms=symptom.synonyms,
                level_scope=symptom.level_scope,
                terrain_scope=symptom.terrain_scope,
                style_scope=symptom.style_scope
            )
            
            created_symptom = symptom_repo.create(new_symptom)
            imported_symptoms.append(created_symptom)
        
        # 導入練習卡
        imported_practice_cards = []
        for practice_card in knowledge_data.practice_cards:
            new_card = PracticeCard(
                name=practice_card.name,
                goal=practice_card.goal,
                tips=practice_card.tips,
                pitfalls=practice_card.pitfalls,
                dosage=practice_card.dosage,
                level=practice_card.level,
                terrain=practice_card.terrain,
                self_check=practice_card.self_check,
                card_type=practice_card.card_type
            )
            
            created_card = practice_repo.create(new_card)
            imported_practice_cards.append(created_card)
        
        # 導入症狀練習卡映射
        imported_mappings = []
        for mapping in knowledge_data.symptom_practice_mappings:
            new_mapping = SymptomPracticeMapping(
                symptom_id=mapping.symptom_id,
                practice_id=mapping.practice_id,
                order=mapping.order
            )
            
            created_mapping = mapping_repo.create(new_mapping)
            imported_mappings.append(created_mapping)
        
        return {
            "status": "success",
            "imported_data": {
                "symptoms": len(imported_symptoms),
                "practice_cards": len(imported_practice_cards),
                "mappings": len(imported_mappings)
            },
            "validation_report": validation_report.dict()
        }
        
    except Exception as e:
        logger.error(f"導入知識到資料庫時出錯: {e}")
        return {
            "status": "error",
            "message": f"導入知識到資料庫時出錯: {str(e)}"
        }

def import_knowledge_from_json_file(
    file_path: str,
    db: Session
) -> Dict[str, Any]:
    """
    從JSON文件導入知識 (TOOL-105.1)
    
    Args:
        file_path: JSON文件路徑
        db: 資料庫會話
        
    Returns:
        Dict[str, Any]: 導入結果
    """
    try:
        # 讀取JSON文件
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        
        # 解析知識數據
        knowledge_data = parse_knowledge_from_json(raw_data)
        
        # 導入到資料庫
        result = import_knowledge_to_database(knowledge_data, db)
        
        return result
        
    except FileNotFoundError:
        logger.error(f"文件不存在: {file_path}")
        return {
            "status": "error",
            "message": f"文件不存在: {file_path}"
        }
    except json.JSONDecodeError as e:
        logger.error(f"解析JSON文件時出錯: {e}")
        return {
            "status": "error",
            "message": f"解析JSON文件時出錯: {str(e)}"
        }
    except Exception as e:
        logger.error(f"從JSON文件導入知識時出錯: {e}")
        return {
            "status": "error",
            "message": f"從JSON文件導入知識時出錯: {str(e)}"
        }

def parse_knowledge_from_json(raw_data: Dict[str, Any]) -> ExtractedKnowledge:
    """
    從JSON數據解析知識 (TOOL-105.1)
    
    Args:
        raw_data: 原始JSON數據
        
    Returns:
        ExtractedKnowledge: 解析後的知識數據
    """
    try:
        # 解析症狀數據
        symptoms = []
        for symptom_data in raw_data.get("symptoms", []):
            symptoms.append({
                "name": symptom_data.get("name", ""),
                "category": symptom_data.get("category", ""),
                "synonyms": symptom_data.get("synonyms", []),
                "level_scope": symptom_data.get("level_scope", []),
                "terrain_scope": symptom_data.get("terrain_scope", []),
                "style_scope": symptom_data.get("style_scope", [])
            })
        
        # 解析練習卡數據
        practice_cards = []
        for card_data in raw_data.get("practice_cards", []):
            practice_cards.append({
                "name": card_data.get("name", ""),
                "goal": card_data.get("goal", ""),
                "tips": card_data.get("tips", []),
                "pitfalls": card_data.get("pitfalls", ""),
                "dosage": card_data.get("dosage", ""),
                "level": card_data.get("level", []),
                "terrain": card_data.get("terrain", []),
                "self_check": card_data.get("self_check", []),
                "card_type": card_data.get("card_type", "")
            })
        
        # 解析症狀練習卡映射數據
        symptom_practice_mappings = []
        for mapping_data in raw_data.get("symptom_practice_mappings", []):
            symptom_practice_mappings.append({
                "symptom_id": mapping_data.get("symptom_id", 0),
                "practice_id": mapping_data.get("practice_id", 0),
                "order": mapping_data.get("order", 0)
            })
        
        # 建立ExtractedKnowledge對象
        knowledge_data = ExtractedKnowledge(
            status="pending_review",
            symptoms=symptoms,
            practice_cards=practice_cards,
            symptom_practice_mappings=symptom_practice_mappings,
            knowledge_structure=raw_data.get("knowledge_structure", {})
        )
        
        return knowledge_data
        
    except Exception as e:
        logger.error(f"解析知識數據時出錯: {e}")
        raise

def validate_before_import(knowledge_data: ExtractedKnowledge) -> Dict[str, Any]:
    """
    導入前驗證 (TOOL-105.2)
    
    Args:
        knowledge_data: 知識數據
        
    Returns:
        Dict[str, Any]: 驗證結果
    """
    try:
        # 分析知識品質
        validation_report = analyze_extracted_knowledge(knowledge_data)
        
        # 檢查是否有嚴重錯誤
        has_serious_errors = validation_report.invalid_records > validation_report.total_records * 0.3
        
        return {
            "validation_status": "success",
            "can_import": not has_serious_errors,
            "validation_report": validation_report.dict(),
            "serious_errors": has_serious_errors
        }
        
    except Exception as e:
        logger.error(f"導入前驗證時出錯: {e}")
        return {
            "validation_status": "error",
            "can_import": False,
            "message": f"導入前驗證時出錯: {str(e)}",
            "serious_errors": True
        }

def generate_import_report(import_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    生成導入報告 (TOOL-105.3)
    
    Args:
        import_result: 導入結果
        
    Returns:
        Dict[str, Any]: 導入報告
    """
    try:
        if import_result["status"] != "success":
            return {
                "report_status": "error",
                "message": "導入失敗，無法生成報告"
            }
        
        imported_data = import_result["imported_data"]
        validation_report = import_result["validation_report"]
        
        report = {
            "report_status": "success",
            "import_summary": {
                "total_symptoms_imported": imported_data["symptoms"],
                "total_practice_cards_imported": imported_data["practice_cards"],
                "total_mappings_imported": imported_data["mappings"],
                "import_time": "2025-10-29 10:00:00"  # 模擬導入時間
            },
            "validation_summary": {
                "total_records": validation_report["total_records"],
                "valid_records": validation_report["valid_records"],
                "invalid_records": validation_report["invalid_records"],
                "validation_rate": validation_report["validation_rate"]
            },
            "anomalies": validation_report["anomalies"]
        }
        
        return report
        
    except Exception as e:
        logger.error(f"生成導入報告時出錯: {e}")
        return {
            "report_status": "error",
            "message": f"生成導入報告時出錯: {str(e)}"
        }