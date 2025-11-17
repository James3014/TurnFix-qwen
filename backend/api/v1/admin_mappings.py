"""
症狀練習卡映射管理 API 端點

從 admin.py 拆分出來 - 遵循單一職責原則
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...database.base import get_db
from ...database.repositories import SymptomPracticeMappingRepository
from .schemas import SymptomPracticeMappingCreate
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/admin/symptom-practice-mappings", tags=["admin"])
async def create_mapping(
    mapping: SymptomPracticeMappingCreate,
    db: Session = Depends(get_db)
):
    """創建症狀練習卡映射 (API-205.3)"""
    try:
        mapping_repo = SymptomPracticeMappingRepository(db)
        new_mapping = mapping_repo.create_mapping(
            mapping.symptom_id,
            mapping.practice_id,
            mapping.order
        )

        return {
            "status": "success",
            "mapping": {
                "symptom_id": new_mapping.symptom_id,
                "practice_id": new_mapping.practice_id,
                "order": new_mapping.order
            }
        }
    except Exception as e:
        logger.error(f"創建映射失敗: {str(e)}")
        raise HTTPException(status_code=500, detail=f"創建映射失敗: {str(e)}")


@router.delete("/admin/symptom-practice-mappings/{symptom_id}/{practice_id}", tags=["admin"])
async def delete_mapping(
    symptom_id: int,
    practice_id: int,
    db: Session = Depends(get_db)
):
    """刪除症狀練習卡映射"""
    try:
        mapping_repo = SymptomPracticeMappingRepository(db)
        success = mapping_repo.delete_mapping(symptom_id, practice_id)

        if not success:
            raise HTTPException(status_code=404, detail="映射不存在")

        return {"status": "success", "message": "映射已刪除"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"刪除映射失敗: {str(e)}")
        raise HTTPException(status_code=500, detail=f"刪除映射失敗: {str(e)}")


@router.get("/admin/symptoms/{symptom_id}/practice-cards", tags=["admin"])
async def get_symptom_practice_cards(symptom_id: int, db: Session = Depends(get_db)):
    """獲取指定症狀的所有練習卡"""
    try:
        mapping_repo = SymptomPracticeMappingRepository(db)
        practice_cards = mapping_repo.get_practice_cards_by_symptom(symptom_id)

        # 驗證關聯數量
        card_count = len(practice_cards)
        warning = None
        if card_count < 3 or card_count > 5:
            warning = f"該症狀目前關聯 {card_count} 張練習卡，建議 3-5 張"

        return {
            "status": "success",
            "practice_cards": [
                {
                    "id": card.id,
                    "name": card.name,
                    "goal": card.goal,
                    "tips": card.tips,
                    "pitfalls": card.pitfalls,
                    "dosage": card.dosage,
                    "level": card.level,
                    "terrain": card.terrain,
                    "self_check": card.self_check,
                    "card_type": card.card_type
                }
                for card in practice_cards
            ],
            "count": card_count,
            "warning": warning
        }
    except Exception as e:
        logger.error(f"獲取症狀練習卡失敗: {str(e)}")
        raise HTTPException(status_code=500, detail=f"獲取症狀練習卡失敗: {str(e)}")
