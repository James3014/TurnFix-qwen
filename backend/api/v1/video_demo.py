"""
視頻示範鏈接 API 端點

實現 UXP-1815 功能：視頻示範鏈接
"""
from fastapi import APIRouter, Query, Depends, Body
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ...database.base import get_db
from ...services.video_demo_service import get_video_suggestions
from ...core.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


class VideoSuggestionResponse(BaseModel):
    """視頻建議響應模型"""
    videos: List[Dict[str, Any]]
    message: str


@router.get("/video-suggestions/{practice_card_id}", tags=["video-demo"])
async def get_practice_card_video_suggestions(
    practice_card_id: int,
    db: Session = Depends(get_db)
):
    """
    獲取練習卡的視頻示範建議 (UXP-1815.1)
    
    根據練習卡內容搜索相關的 YouTube 視頻
    """
    try:
        # 從資料庫獲取練習卡信息
        from ...models.practice_card import PracticeCard
        practice_card = db.query(PracticeCard).filter(PracticeCard.id == practice_card_id).first()
        
        if not practice_card:
            return {
                "status": "error",
                "message": "練習卡不存在"
            }
        
        # 搜索相關視頻
        api_key = settings.YOUTUBE_API_KEY
        videos = get_video_suggestions(practice_card.name, practice_card.goal, api_key)
        
        # 檢查是否有找到視頻
        if not videos:
            message = f"未找到與「{practice_card.name}」相關的視頻示範"
        else:
            message = f"找到 {len(videos)} 個與「{practice_card.name}」相關的視頻示範"
        
        return {
            "status": "success",
            "videos": videos,
            "message": message
        }
    except Exception as e:
        logger.error(f"獲取視頻建議時出錯: {e}")
        return {
            "status": "error",
            "message": f"獲取視頻建議時出錯: {str(e)}"
        }