"""
使用者回饋 API 端點 (API-204)

實現兩層回饋機制：
1. Session 層級 - 整個問題推薦流程的效果評價
2. PracticeCard 層級 - 單個練習卡的品質評價
"""
from fastapi import APIRouter, Query, Depends, Body, Path
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ...database.base import get_db
from ...database.repositories import (
    SessionFeedbackRepository,
    PracticeCardFeedbackRepository
)
from ...models.session_feedback import SessionFeedback
from ...models.practice_card_feedback import PracticeCardFeedback
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class SessionFeedbackCreate(BaseModel):
    """創建會話回饋請求模型"""
    session_id: int
    rating: str  # "not_applicable" | "partially_applicable" | "applicable"
    feedback_text: Optional[str] = None
    feedback_type: str = "immediate"  # "immediate" | "delayed"

class PracticeCardFeedbackCreate(BaseModel):
    """創建練習卡回饋請求模型"""
    session_id: int
    practice_id: int
    rating: int  # 1-5 顆星
    feedback_text: Optional[str] = None
    is_favorite: bool = False

class PracticeCardFavoriteUpdate(BaseModel):
    """更新練習卡最愛狀態請求模型"""
    is_favorite: bool

@router.post("/session-feedback", tags=["feedback"])
async def create_session_feedback(
    feedback_data: SessionFeedbackCreate,
    db: Session = Depends(get_db)
):
    """
    創建會話回饋 (API-204.1)
    
    記錄對整個推薦流程的評分和自由文字回饋
    
    用戶可以評價：
    - "not_applicable" (❌ 不適用) - 推薦的練習卡與我的問題無關或不適合我
    - "partially_applicable" (△ 部分適用) - 有些內容有用，但大部分不適用
    - "applicable" (✓ 適用) - 相當有幫助
    """
    try:
        feedback_repo = SessionFeedbackRepository(db)
        
        # 創建會話回饋記錄
        feedback = SessionFeedback(
            session_id=feedback_data.session_id,
            rating=feedback_data.rating,
            feedback_text=feedback_data.feedback_text,
            feedback_type=feedback_data.feedback_type
        )
        
        created_feedback = feedback_repo.create(feedback)
        
        return {
            "status": "success",
            "feedback": {
                "id": created_feedback.id,
                "session_id": created_feedback.session_id,
                "rating": created_feedback.rating,
                "feedback_text": created_feedback.feedback_text,
                "feedback_type": created_feedback.feedback_type,
                "created_at": created_feedback.created_at
            }
        }
    except Exception as e:
        logger.error(f"創建會話回饋時出錯: {e}")
        return {
            "status": "error",
            "message": f"創建會話回饋時出錯: {str(e)}"
        }

@router.post("/practice-card-feedback", tags=["feedback"])
async def create_practice_card_feedback(
    feedback_data: PracticeCardFeedbackCreate,
    db: Session = Depends(get_db)
):
    """
    創建練習卡回饋 (API-204.3)
    
    記錄對單個練習卡的星數評分和自由文字回饋
    
    星數評分值域：1-5 顆星
    - 1 顆星 ⭐：不適用 - 練習卡與我的症狀無關或不適合我
    - 2 顆星 ⭐⭐：較不適用 - 有些內容有用，但大部分不適用
    - 3 顆星 ⭐⭐⭐：部分適用 - 有幫助但需要調整或補充
    - 4 顆星 ⭐⭐⭐⭐：適用 - 相當有幫助
    - 5 顆星 ⭐⭐⭐⭐⭐：非常適用 - 完全符合我的需求
    
    is_favorite：布林值，是否加入最愛清單（預設 false），可獨立於星數設定
    """
    try:
        feedback_repo = PracticeCardFeedbackRepository(db)
        
        # 創建練習卡回饋記錄
        feedback = PracticeCardFeedback(
            session_id=feedback_data.session_id,
            practice_id=feedback_data.practice_id,
            rating=feedback_data.rating,
            feedback_text=feedback_data.feedback_text,
            is_favorite=feedback_data.is_favorite
        )
        
        created_feedback = feedback_repo.create(feedback)
        
        return {
            "status": "success",
            "feedback": {
                "id": created_feedback.id,
                "session_id": created_feedback.session_id,
                "practice_id": created_feedback.practice_id,
                "rating": created_feedback.rating,
                "feedback_text": created_feedback.feedback_text,
                "is_favorite": created_feedback.is_favorite,
                "created_at": created_feedback.created_at
            }
        }
    except Exception as e:
        logger.error(f"創建練習卡回饋時出錯: {e}")
        return {
            "status": "error",
            "message": f"創建練習卡回饋時出錯: {str(e)}"
        }

@router.put("/practice-card-feedback/{feedback_id}/favorite", tags=["feedback"])
async def toggle_practice_card_favorite(
    feedback_id: int = Path(..., title="回饋ID", description="回饋的唯一標識符"),
    favorite_data: PracticeCardFavoriteUpdate = Body(..., title="最愛狀態", description="True表示加入最愛，False表示取消最愛"),
    db: Session = Depends(get_db)
):
    """
    切換練習卡最愛狀態 (API-204.5)
    
    更新練習卡最愛標記狀態
    
    可獨立於星數評分進行設置
    """
    try:
        feedback_repo = PracticeCardFeedbackRepository(db)
        
        # 獲取現有記錄
        existing_feedback = feedback_repo.get_by_id(feedback_id)
        if not existing_feedback:
            return {
                "status": "error",
                "message": "回饋不存在"
            }
        
        # 更新最愛狀態
        updated_feedback = feedback_repo.update(feedback_id, is_favorite=favorite_data.is_favorite)
        
        return {
            "status": "success",
            "feedback": {
                "id": updated_feedback.id,
                "session_id": updated_feedback.session_id,
                "practice_id": updated_feedback.practice_id,
                "rating": updated_feedback.rating,
                "feedback_text": updated_feedback.feedback_text,
                "is_favorite": updated_feedback.is_favorite,
                "created_at": updated_feedback.created_at
            }
        }
    except Exception as e:
        logger.error(f"更新練習卡最愛狀態時出錯: {e}")
        return {
            "status": "error",
            "message": f"更新練習卡最愛狀態時出錯: {str(e)}"
        }