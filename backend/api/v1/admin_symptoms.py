"""
症狀管理 API 端點

從 admin.py 拆分出來 - 遵循單一職責原則
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...database.base import get_db
from ...database.repositories import SymptomRepository
from ...models.symptom import Symptom
from .schemas import SymptomCreate, SymptomUpdate
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/admin/symptoms", tags=["admin"])
async def create_symptom(symptom: SymptomCreate, db: Session = Depends(get_db)):
    """創建症狀 (API-205.1)"""
    try:
        symptom_repo = SymptomRepository(db)
        new_symptom = Symptom(
            name=symptom.name,
            category=symptom.category,
            synonyms=symptom.synonyms,
            level_scope=symptom.level_scope,
            terrain_scope=symptom.terrain_scope,
            style_scope=symptom.style_scope
        )
        created_symptom = symptom_repo.create(new_symptom)

        return {
            "status": "success",
            "symptom": {
                "id": created_symptom.id,
                "name": created_symptom.name,
                "category": created_symptom.category,
                "synonyms": created_symptom.synonyms,
                "level_scope": created_symptom.level_scope,
                "terrain_scope": created_symptom.terrain_scope,
                "style_scope": created_symptom.style_scope
            }
        }
    except Exception as e:
        logger.error(f"創建症狀失敗: {str(e)}")
        raise HTTPException(status_code=500, detail=f"創建症狀失敗: {str(e)}")


@router.get("/admin/symptoms", tags=["admin"])
async def get_all_symptoms(db: Session = Depends(get_db)):
    """獲取所有症狀"""
    try:
        symptom_repo = SymptomRepository(db)
        symptoms = symptom_repo.get_all()

        return {
            "status": "success",
            "symptoms": [
                {
                    "id": s.id,
                    "name": s.name,
                    "category": s.category,
                    "synonyms": s.synonyms,
                    "level_scope": s.level_scope,
                    "terrain_scope": s.terrain_scope,
                    "style_scope": s.style_scope
                }
                for s in symptoms
            ],
            "count": len(symptoms)
        }
    except Exception as e:
        logger.error(f"獲取症狀列表失敗: {str(e)}")
        raise HTTPException(status_code=500, detail=f"獲取症狀列表失敗: {str(e)}")


@router.get("/admin/symptoms/{symptom_id}", tags=["admin"])
async def get_symptom(symptom_id: int, db: Session = Depends(get_db)):
    """獲取單個症狀"""
    try:
        symptom_repo = SymptomRepository(db)
        symptom = symptom_repo.get_by_id(symptom_id)

        if not symptom:
            raise HTTPException(status_code=404, detail="症狀不存在")

        return {
            "status": "success",
            "symptom": {
                "id": symptom.id,
                "name": symptom.name,
                "category": symptom.category,
                "synonyms": symptom.synonyms,
                "level_scope": symptom.level_scope,
                "terrain_scope": symptom.terrain_scope,
                "style_scope": symptom.style_scope
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"獲取症狀失敗: {str(e)}")
        raise HTTPException(status_code=500, detail=f"獲取症狀失敗: {str(e)}")


@router.put("/admin/symptoms/{symptom_id}", tags=["admin"])
async def update_symptom(
    symptom_id: int,
    symptom_update: SymptomUpdate,
    db: Session = Depends(get_db)
):
    """更新症狀"""
    try:
        symptom_repo = SymptomRepository(db)
        updated_symptom = symptom_repo.update(symptom_id, **symptom_update.dict(exclude_unset=True))

        if not updated_symptom:
            raise HTTPException(status_code=404, detail="症狀不存在")

        return {
            "status": "success",
            "symptom": {
                "id": updated_symptom.id,
                "name": updated_symptom.name,
                "category": updated_symptom.category,
                "synonyms": updated_symptom.synonyms,
                "level_scope": updated_symptom.level_scope,
                "terrain_scope": updated_symptom.terrain_scope,
                "style_scope": updated_symptom.style_scope
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新症狀失敗: {str(e)}")
        raise HTTPException(status_code=500, detail=f"更新症狀失敗: {str(e)}")


@router.delete("/admin/symptoms/{symptom_id}", tags=["admin"])
async def delete_symptom(symptom_id: int, db: Session = Depends(get_db)):
    """刪除症狀"""
    try:
        symptom_repo = SymptomRepository(db)
        success = symptom_repo.delete(symptom_id)

        if not success:
            raise HTTPException(status_code=404, detail="症狀不存在")

        return {"status": "success", "message": "症狀已刪除"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"刪除症狀失敗: {str(e)}")
        raise HTTPException(status_code=500, detail=f"刪除症狀失敗: {str(e)}")
