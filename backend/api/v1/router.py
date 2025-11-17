"""
API v1 路由配置

定義所有 API 端點的路由
保持簡單，避免過度工程

重構後的結構：
- admin.py 已拆分為 3 個獨立路由文件（單一職責）
- 每個路由文件 < 200 行
"""
from fastapi import APIRouter
from . import (
    ski_tips,
    followup,
    feedback,
    admin_symptoms,
    admin_practice_cards,
    admin_mappings,
    admin_feedback,
    personalization,
    video_demo,
    knowledge_management,
    favorites
)

router = APIRouter()

# 滑雪技巧建議路由
router.include_router(ski_tips.router, prefix="", tags=["ski-tips"])

# 自適應追問路由
router.include_router(followup.router, prefix="", tags=["followup"])

# 使用者回饋路由
router.include_router(feedback.router, prefix="", tags=["feedback"])

# 管理者後台路由 - 症狀管理
router.include_router(admin_symptoms.router, prefix="", tags=["admin"])

# 管理者後台路由 - 練習卡管理
router.include_router(admin_practice_cards.router, prefix="", tags=["admin"])

# 管理者後台路由 - 映射管理
router.include_router(admin_mappings.router, prefix="", tags=["admin"])

# 管理者回饋分析路由
router.include_router(admin_feedback.router, prefix="", tags=["admin-analytics"])

# 個人化推薦路由
router.include_router(personalization.router, prefix="", tags=["personalization"])

# 視頻示範路由
router.include_router(video_demo.router, prefix="", tags=["video-demo"])

# 知識庫管理路由
router.include_router(knowledge_management.router, prefix="", tags=["knowledge-management"])

# 最愛管理路由
router.include_router(favorites.router, prefix="", tags=["favorites"])

# 健康檢查端點
@router.get("/health")
def health_check():
    return {"status": "healthy"}
