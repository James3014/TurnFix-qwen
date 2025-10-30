"""
自適應追問 API 端點 (API-203)

實現 LLM 輔助的置信度判斷和追問問題生成
"""
from fastapi import APIRouter, Query, Depends, Body
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ...database.base import get_db
from ...services.followup_questions import get_followup_needs

router = APIRouter()

class FollowupRequest(BaseModel):
    """追問請求模型"""
    input_text: str
    level: Optional[str] = None
    terrain: Optional[str] = None
    style: Optional[str] = None

class FollowupResponse(BaseModel):
    """追問響應模型"""
    need_followup: bool
    confidence: float
    missing_slots: List[str]
    questions: List[Dict[str, str]]

@router.post("/followup-needs", tags=["followup"])
async def get_followup_needs_endpoint(
    request: FollowupRequest,
    db: Session = Depends(get_db)
):
    """
    獲取自適應追問需求 (API-203)
    
    實現 LLM 輔助的置信度判斷和追問問題生成
    """
    try:
        # 調用服務層獲取追問需求
        followup_info = get_followup_needs(
            db,
            request.input_text,
            request.level,
            request.terrain,
            request.style
        )
        
        return {
            "status": "success",
            "followup_needs": followup_info
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"獲取追問需求時出錯: {str(e)}"
        }