"""
管理者後台 API 端點 (API-205)

實現管理者後台功能：
1. 症狀管理
2. 練習卡管理
3. 症狀↔練習卡映射管理
4. 同義詞庫管理
"""
from fastapi import APIRouter, Query, Depends, Body, Path
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ...database.base import get_db
from ...database.repositories import (
    SymptomRepository,
    PracticeCardRepository,
    SymptomPracticeMappingRepository
)
from ...models.symptom import Symptom
from ...models.practice_card import PracticeCard
from ...models.symptom_practice_mapping import SymptomPracticeMapping
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class SymptomCreate(BaseModel):
    """創建症狀請求模型"""
    name: str
    category: str
    synonyms: List[str] = []
    level_scope: List[str] = []
    terrain_scope: List[str] = []
    style_scope: List[str] = []

class SymptomUpdate(BaseModel):
    """更新症狀請求模型"""
    name: Optional[str] = None
    category: Optional[str] = None
    synonyms: Optional[List[str]] = None
    level_scope: Optional[List[str]] = None
    terrain_scope: Optional[List[str]] = None
    style_scope: Optional[List[str]] = None

class PracticeCardCreate(BaseModel):
    """創建練習卡請求模型"""
    name: str
    goal: str
    tips: List[str] = []
    pitfalls: str = ""
    dosage: str = ""
    level: List[str] = []
    terrain: List[str] = []
    self_check: List[str] = []
    card_type: str = ""

class PracticeCardUpdate(BaseModel):
    """更新練習卡請求模型"""
    name: Optional[str] = None
    goal: Optional[str] = None
    tips: Optional[List[str]] = None
    pitfalls: Optional[str] = None
    dosage: Optional[str] = None
    level: Optional[List[str]] = None
    terrain: Optional[List[str]] = None
    self_check: Optional[List[str]] = None
    card_type: Optional[str] = None

class SymptomPracticeMappingCreate(BaseModel):
    """創建症狀練習卡映射請求模型"""
    symptom_id: int
    practice_id: int
    order: int = 0

class SymptomPracticeMappingUpdate(BaseModel):
    """更新症狀練習卡映射請求模型"""
    order: Optional[int] = None

@router.post("/admin/symptoms", tags=["admin"])
async def create_symptom(
    symptom: SymptomCreate,
    db: Session = Depends(get_db)
):
    """
    創建症狀 (API-205.1)
    
    提供 CRUD 接口用於管理症狀種子
    """
    try:
        symptom_repo = SymptomRepository(db)
        
        # 創建症狀對象
        new_symptom = Symptom(
            name=symptom.name,
            category=symptom.category,
            synonyms=symptom.synonyms,
            level_scope=symptom.level_scope,
            terrain_scope=symptom.terrain_scope,
            style_scope=symptom.style_scope
        )
        
        # 保存到資料庫
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
        logger.error(f"創建症狀時出錯: {e}")
        return {
            "status": "error",
            "message": f"創建症狀時出錯: {str(e)}"
        }

@router.get("/admin/symptoms/{symptom_id}", tags=["admin"])
async def get_symptom(
    symptom_id: int = Path(..., title="症狀ID", description="症狀的唯一標識符"),
    db: Session = Depends(get_db)
):
    """
    獲取症狀 (API-205.1)
    
    提供 CRUD 接口用於管理症狀種子
    """
    try:
        symptom_repo = SymptomRepository(db)
        symptom = symptom_repo.get_by_id(symptom_id)
        
        if not symptom:
            return {
                "status": "error",
                "message": "症狀不存在"
            }
        
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
    except Exception as e:
        logger.error(f"獲取症狀時出錯: {e}")
        return {
            "status": "error",
            "message": f"獲取症狀時出錯: {str(e)}"
        }

@router.put("/admin/symptoms/{symptom_id}", tags=["admin"])
async def update_symptom(
    symptom_id: int = Path(..., title="症狀ID", description="症狀的唯一標識符"),
    symptom_update: SymptomUpdate = Body(..., title="症狀更新資訊", description="要更新的症狀欄位"),
    db: Session = Depends(get_db)
):
    """
    更新症狀 (API-205.1)
    
    提供 CRUD 接口用於管理症狀種子
    """
    try:
        symptom_repo = SymptomRepository(db)
        updated_symptom = symptom_repo.update(symptom_id, **symptom_update.dict(exclude_unset=True))
        
        if not updated_symptom:
            return {
                "status": "error",
                "message": "症狀不存在"
            }
        
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
    except Exception as e:
        logger.error(f"更新症狀時出錯: {e}")
        return {
            "status": "error",
            "message": f"更新症狀時出錯: {str(e)}"
        }

@router.delete("/admin/symptoms/{symptom_id}", tags=["admin"])
async def delete_symptom(
    symptom_id: int = Path(..., title="症狀ID", description="症狀的唯一標識符"),
    db: Session = Depends(get_db)
):
    """
    刪除症狀 (API-205.1)
    
    提供 CRUD 接口用於管理症狀種子
    """
    try:
        symptom_repo = SymptomRepository(db)
        success = symptom_repo.delete(symptom_id)
        
        if not success:
            return {
                "status": "error",
                "message": "症狀不存在"
            }
        
        return {
            "status": "success",
            "message": "症狀已刪除"
        }
    except Exception as e:
        logger.error(f"刪除症狀時出錯: {e}")
        return {
            "status": "error",
            "message": f"刪除症狀時出錯: {str(e)}"
        }

@router.post("/admin/practice-cards", tags=["admin"])
async def create_practice_card(
    practice_card: PracticeCardCreate,
    db: Session = Depends(get_db)
):
    """
    創建練習卡 (API-205.2)
    
    提供 CRUD 接口用於管理練習卡
    """
    try:
        practice_repo = PracticeCardRepository(db)
        
        # 創建練習卡對象
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
        
        # 保存到資料庫
        created_card = practice_repo.create(new_card)
        
        return {
            "status": "success",
            "practice_card": {
                "id": created_card.id,
                "name": created_card.name,
                "goal": created_card.goal,
                "tips": created_card.tips,
                "pitfalls": created_card.pitfalls,
                "dosage": created_card.dosage,
                "level": created_card.level,
                "terrain": created_card.terrain,
                "self_check": created_card.self_check,
                "card_type": created_card.card_type
            }
        }
    except Exception as e:
        logger.error(f"創建練習卡時出錯: {e}")
        return {
            "status": "error",
            "message": f"創建練習卡時出錯: {str(e)}"
        }

@router.get("/admin/practice-cards/{practice_card_id}", tags=["admin"])
async def get_practice_card(
    practice_card_id: int = Path(..., title="練習卡ID", description="練習卡的唯一標識符"),
    db: Session = Depends(get_db)
):
    """
    獲取練習卡 (API-205.2)
    
    提供 CRUD 接口用於管理練習卡
    """
    try:
        practice_repo = PracticeCardRepository(db)
        card = practice_repo.get_by_id(practice_card_id)
        
        if not card:
            return {
                "status": "error",
                "message": "練習卡不存在"
            }
        
        return {
            "status": "success",
            "practice_card": {
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
        }
    except Exception as e:
        logger.error(f"獲取練習卡時出錯: {e}")
        return {
            "status": "error",
            "message": f"獲取練習卡時出錯: {str(e)}"
        }

@router.put("/admin/practice-cards/{practice_card_id}", tags=["admin"])
async def update_practice_card(
    practice_card_id: int = Path(..., title="練習卡ID", description="練習卡的唯一標識符"),
    practice_card_update: PracticeCardUpdate = Body(..., title="練習卡更新資訊", description="要更新的練習卡欄位"),
    db: Session = Depends(get_db)
):
    """
    更新練習卡 (API-205.2)
    
    提供 CRUD 接口用於管理練習卡
    """
    try:
        practice_repo = PracticeCardRepository(db)
        updated_card = practice_repo.update(practice_card_id, **practice_card_update.dict(exclude_unset=True))
        
        if not updated_card:
            return {
                "status": "error",
                "message": "練習卡不存在"
            }
        
        return {
            "status": "success",
            "practice_card": {
                "id": updated_card.id,
                "name": updated_card.name,
                "goal": updated_card.goal,
                "tips": updated_card.tips,
                "pitfalls": updated_card.pitfalls,
                "dosage": updated_card.dosage,
                "level": updated_card.level,
                "terrain": updated_card.terrain,
                "self_check": updated_card.self_check,
                "card_type": updated_card.card_type
            }
        }
    except Exception as e:
        logger.error(f"更新練習卡時出錯: {e}")
        return {
            "status": "error",
            "message": f"更新練習卡時出錯: {str(e)}"
        }

@router.delete("/admin/practice-cards/{practice_card_id}", tags=["admin"])
async def delete_practice_card(
    practice_card_id: int = Path(..., title="練習卡ID", description="練習卡的唯一標識符"),
    db: Session = Depends(get_db)
):
    """
    刪除練習卡 (API-205.2)
    
    提供 CRUD 接口用於管理練習卡
    """
    try:
        practice_repo = PracticeCardRepository(db)
        success = practice_repo.delete(practice_card_id)
        
        if not success:
            return {
                "status": "error",
                "message": "練習卡不存在"
            }
        
        return {
            "status": "success",
            "message": "練習卡已刪除"
        }
    except Exception as e:
        logger.error(f"刪除練習卡時出錯: {e}")
        return {
            "status": "error",
            "message": f"刪除練習卡時出錯: {str(e)}"
        }

@router.post("/admin/symptom-practice-mappings", tags=["admin"])
async def create_symptom_practice_mapping(
    mapping: SymptomPracticeMappingCreate,
    db: Session = Depends(get_db)
):
    """
    創建症狀練習卡映射 (API-205.3)
    
    提供接口管理症狀↔練習卡的關聯
    """
    try:
        mapping_repo = SymptomPracticeMappingRepository(db)
        
        # 創建映射對象
        new_mapping = SymptomPracticeMapping(
            symptom_id=mapping.symptom_id,
            practice_id=mapping.practice_id,
            order=mapping.order
        )
        
        # 保存到資料庫
        created_mapping = mapping_repo.create(new_mapping)
        
        return {
            "status": "success",
            "mapping": {
                "symptom_id": created_mapping.symptom_id,
                "practice_id": created_mapping.practice_id,
                "order": created_mapping.order
            }
        }
    except Exception as e:
        logger.error(f"創建症狀練習卡映射時出錯: {e}")
        return {
            "status": "error",
            "message": f"創建症狀練習卡映射時出錯: {str(e)}"
        }

@router.delete("/admin/symptom-practice-mappings/{symptom_id}/{practice_id}", tags=["admin"])
async def delete_symptom_practice_mapping(
    symptom_id: int = Path(..., title="症狀ID", description="症狀的唯一標識符"),
    practice_id: int = Path(..., title="練習卡ID", description="練習卡的唯一標識符"),
    db: Session = Depends(get_db)
):
    """
    刪除症狀練習卡映射 (API-205.3)
    
    提供接口管理症狀↔練習卡的關聯
    """
    try:
        mapping_repo = SymptomPracticeMappingRepository(db)
        success = mapping_repo.delete_mapping(symptom_id, practice_id)
        
        if not success:
            return {
                "status": "error",
                "message": "映射不存在"
            }
        
        return {
            "status": "success",
            "message": "映射已刪除"
        }
    except Exception as e:
        logger.error(f"刪除症狀練習卡映射時出錯: {e}")
        return {
            "status": "error",
            "message": f"刪除症狀練習卡映射時出錯: {str(e)}"
        }

@router.get("/admin/symptoms/{symptom_id}/practice-cards", tags=["admin"])
async def get_symptom_practice_cards(
    symptom_id: int = Path(..., title="症狀ID", description="症狀的唯一標識符"),
    db: Session = Depends(get_db)
):
    """
    獲取指定症狀的所有練習卡 (API-205.3)
    
    提供接口管理症狀↔練習卡的關聯
    """
    try:
        mapping_repo = SymptomPracticeMappingRepository(db)
        practice_cards = mapping_repo.get_practice_cards_by_symptom(symptom_id)
        
        # 驗證關聯數量 (API-202.4)
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
        logger.error(f"獲取症狀練習卡時出錯: {e}")
        return {
            "status": "error",
            "message": f"獲取症狀練習卡時出錯: {str(e)}"
        }