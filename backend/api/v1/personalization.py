"""
個人化推薦 API 端點

實現個人化推薦演化功能
"""
from fastapi import APIRouter, Query, Depends, Body
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ...database.base import get_db
from ...services.personalization_service import (
    get_user_preference_analysis,
    get_personalized_recommendations
)

router = APIRouter()


class PersonalizedRecommendationResponse(BaseModel):
    """個人化推薦響應模型"""
    message: str
    recommendations: List[Dict[str, Any]]


@router.get("/personalization/user-preferences", tags=["personalization"])
async def get_user_preferences(
    session_id: int = Query(..., title="用戶會話ID", description="用戶會話的唯一標識符"),
    db: Session = Depends(get_db)
):
    """
    獲取用戶偏好分析 (UXP-1814.1)
    
    根據用戶評分歷史，識別用戶偏好的卡片類型
    """
    preference_analysis = get_user_preference_analysis(db, session_id)
    
    return {
        "status": "success",
        "preference_analysis": preference_analysis
    }


@router.get("/personalization/recommendations/{practice_id}", tags=["personalization"])
async def get_practice_personalized_recommendations(
    practice_id: int,
    session_id: int = Query(..., title="用戶會話ID", description="用戶會話的唯一標識符"),
    db: Session = Depends(get_db)
):
    """
    獲取特定練習卡的個性化推薦 (UXP-1814.2)
    
    根據用戶評分歷史，提供與當前練習卡類似的推薦
    """
    recommendations = get_personalized_recommendations(db, session_id, practice_id)
    
    return {
        "status": "success",
        "recommendations": recommendations
    }