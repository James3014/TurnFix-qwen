"""
最愛練習卡管理 API

獨立路由 - 遵循 Linus 原則：
1. 單一職責
2. SQL 查詢在 Repository 層，不在 API 層
3. 統一使用 HTTPException 錯誤處理
"""
from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from ...database.base import get_db
from ...database.repositories import PracticeCardFeedbackRepository
from ...models.practice_card_feedback import PracticeCardFeedback

router = APIRouter()


@router.get("/user/favorite-cards", tags=["favorites"])
async def get_user_favorite_cards(db: Session = Depends(get_db)):
    """
    獲取用戶的所有最愛練習卡 (API-206.1)
    """
    try:
        feedback_repo = PracticeCardFeedbackRepository(db)
        favorites_data = feedback_repo.get_favorites_with_cards()

        favorite_cards = []
        for item in favorites_data:
            feedback = item["feedback"]
            card = item["card"]

            favorite_cards.append({
                "card": {
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
                },
                "user_rating": feedback.rating,
                "user_notes": feedback.feedback_text,
                "favorited_at": feedback.created_at
            })

        return {
            "status": "success",
            "favorite_cards": favorite_cards,
            "count": len(favorite_cards)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"獲取最愛練習卡時出錯: {str(e)}")


@router.post("/user/favorite-cards/{practice_card_id}", tags=["favorites"])
async def toggle_favorite_card(
    practice_card_id: int,
    is_favorite: bool = Body(...),
    session_id: int = Body(...),
    db: Session = Depends(get_db)
):
    """
    更新練習卡的最愛狀態 (API-206.2)
    """
    try:
        feedback_repo = PracticeCardFeedbackRepository(db)
        existing_feedback = feedback_repo.get_by_session_and_practice(session_id, practice_card_id)

        if existing_feedback:
            updated_feedback = feedback_repo.update(existing_feedback.id, is_favorite=is_favorite)
        else:
            updated_feedback = feedback_repo.create(PracticeCardFeedback(
                session_id=session_id,
                practice_id=practice_card_id,
                rating=0,
                is_favorite=is_favorite
            ))

        return {
            "status": "success",
            "message": f"練習卡已{'加入' if is_favorite else '移除'}最愛清單",
            "feedback": {
                "id": updated_feedback.id,
                "is_favorite": updated_feedback.is_favorite
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新最愛狀態時出錯: {str(e)}")


@router.delete("/user/favorite-cards/{practice_card_id}", tags=["favorites"])
async def remove_favorite_card(
    practice_card_id: int,
    session_id: int = Body(...),
    db: Session = Depends(get_db)
):
    """
    移除最愛標記 (API-206.3)
    """
    try:
        feedback_repo = PracticeCardFeedbackRepository(db)
        existing_feedback = feedback_repo.get_by_session_and_practice(session_id, practice_card_id)

        if existing_feedback:
            updated_feedback = feedback_repo.update(existing_feedback.id, is_favorite=False)
            return {
                "status": "success",
                "message": "練習卡已移除最愛清單",
                "feedback": {
                    "id": updated_feedback.id,
                    "is_favorite": updated_feedback.is_favorite
                }
            }
        else:
            return {"status": "success", "message": "練習卡不在最愛清單中"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"移除最愛標記時出錯: {str(e)}")
