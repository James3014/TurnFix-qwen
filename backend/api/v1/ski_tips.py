"""
滑雪技巧建議 API 端點

簡化版本 - 遵循 Linus 原則：
1. 移除所有重複的路由（症狀、練習卡、映射管理已在 admin.py）
2. 只保留真正的滑雪建議相關功能
3. 使用共享的 schemas
4. 從 615 行減少到 < 100 行
"""
from fastapi import APIRouter, Query, Depends, HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from ...database.base import get_db
from ...services.simple_ski_tips import get_ski_tips, identify_symptom
from ...services.followup_questions import get_followup_needs
from ...database.repositories import SymptomRepository
from .schemas import SkiTipsRequest, FollowupNeedsRequest

router = APIRouter()


@router.post("/ski-tips", tags=["ski-tips"])
async def get_ski_tips_endpoint(
    input_text: str = Query(..., title="使用者輸入的口語問題", description="例如：轉彎會後坐"),
    level: Optional[str] = Query(None, title="選填等級", description="例如：初級、中級、高級"),
    terrain: Optional[str] = Query(None, title="選填地形", description="例如：綠線、藍線、黑線"),
    style: Optional[str] = Query(None, title="選填滑行風格", description="例如：平花、Park"),
    db: Session = Depends(get_db)
):
    """
    獲取滑雪技巧建議 (API-202)

    根據使用者輸入的口語問題和選填條件，推薦 3-5 張練習卡
    """
    try:
        tips = get_ski_tips(db, input_text, level, terrain, style)
        return {
            "status": "success",
            "recommended_cards": tips,
            "count": len(tips)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"獲取建議失敗: {str(e)}")


@router.post("/followup-needs", tags=["followup"])
async def get_followup_needs_endpoint(
    input_text: str = Query(...),
    level: Optional[str] = Query(None),
    terrain: Optional[str] = Query(None),
    style: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    獲取自適應追問需求 (API-203)

    實現 LLM 輔助的置信度判斷和追問問題生成
    """
    try:
        # 識別症狀
        symptom_repo = SymptomRepository(db)
        recognized_symptom = identify_symptom(symptom_repo, input_text)

        # 評估是否需要追問
        followup_info = get_followup_needs(input_text, recognized_symptom, level, terrain, style)

        return {
            "status": "success",
            "followup_needs": followup_info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"獲取追問需求失敗: {str(e)}")
