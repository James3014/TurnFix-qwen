"""
練習卡管理 API 端點

從 admin.py 拆分出來 - 遵循單一職責原則
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...database.base import get_db
from ...database.repositories import PracticeCardRepository
from ...models.practice_card import PracticeCard
from .schemas import PracticeCardCreate, PracticeCardUpdate
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/admin/practice-cards", tags=["admin"])
async def create_practice_card(
    practice_card: PracticeCardCreate,
    db: Session = Depends(get_db)
):
    """創建練習卡 (API-205.2)"""
    try:
        practice_repo = PracticeCardRepository(db)
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
        logger.error(f"創建練習卡失敗: {str(e)}")
        raise HTTPException(status_code=500, detail=f"創建練習卡失敗: {str(e)}")


@router.get("/admin/practice-cards", tags=["admin"])
async def get_all_practice_cards(db: Session = Depends(get_db)):
    """獲取所有練習卡"""
    try:
        practice_repo = PracticeCardRepository(db)
        cards = practice_repo.get_all()

        return {
            "status": "success",
            "practice_cards": [
                {
                    "id": c.id,
                    "name": c.name,
                    "goal": c.goal,
                    "tips": c.tips,
                    "pitfalls": c.pitfalls,
                    "dosage": c.dosage,
                    "level": c.level,
                    "terrain": c.terrain,
                    "self_check": c.self_check,
                    "card_type": c.card_type
                }
                for c in cards
            ],
            "count": len(cards)
        }
    except Exception as e:
        logger.error(f"獲取練習卡列表失敗: {str(e)}")
        raise HTTPException(status_code=500, detail=f"獲取練習卡列表失敗: {str(e)}")


@router.get("/admin/practice-cards/{practice_card_id}", tags=["admin"])
async def get_practice_card(practice_card_id: int, db: Session = Depends(get_db)):
    """獲取單個練習卡"""
    try:
        practice_repo = PracticeCardRepository(db)
        card = practice_repo.get_by_id(practice_card_id)

        if not card:
            raise HTTPException(status_code=404, detail="練習卡不存在")

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
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"獲取練習卡失敗: {str(e)}")
        raise HTTPException(status_code=500, detail=f"獲取練習卡失敗: {str(e)}")


@router.put("/admin/practice-cards/{practice_card_id}", tags=["admin"])
async def update_practice_card(
    practice_card_id: int,
    practice_card_update: PracticeCardUpdate,
    db: Session = Depends(get_db)
):
    """更新練習卡"""
    try:
        practice_repo = PracticeCardRepository(db)
        updated_card = practice_repo.update(
            practice_card_id,
            **practice_card_update.dict(exclude_unset=True)
        )

        if not updated_card:
            raise HTTPException(status_code=404, detail="練習卡不存在")

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
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新練習卡失敗: {str(e)}")
        raise HTTPException(status_code=500, detail=f"更新練習卡失敗: {str(e)}")


@router.delete("/admin/practice-cards/{practice_card_id}", tags=["admin"])
async def delete_practice_card(practice_card_id: int, db: Session = Depends(get_db)):
    """刪除練習卡"""
    try:
        practice_repo = PracticeCardRepository(db)
        success = practice_repo.delete(practice_card_id)

        if not success:
            raise HTTPException(status_code=404, detail="練習卡不存在")

        return {"status": "success", "message": "練習卡已刪除"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"刪除練習卡失敗: {str(e)}")
        raise HTTPException(status_code=500, detail=f"刪除練習卡失敗: {str(e)}")
