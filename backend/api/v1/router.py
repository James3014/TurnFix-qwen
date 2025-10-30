"""
API v1 路由配置

定義所有 API 端點的路由
保持簡單，避免過度工程
"""
from fastapi import APIRouter
from . import ski_tips, followup, feedback, admin, admin_feedback, personalization, video_demo, knowledge_management

router = APIRouter()

# 滑雪技巧建議路由
router.include_router(ski_tips.router, prefix="", tags=["ski-tips"])

# 自適應追問路由
router.include_router(followup.router, prefix="", tags=["followup"])

# 使用者回饋路由
router.include_router(feedback.router, prefix="", tags=["feedback"])

# 管理者後台路由
router.include_router(admin.router, prefix="", tags=["admin"])

# 管理者回饋分析路由
router.include_router(admin_feedback.router, prefix="", tags=["admin-analytics"])

# 個人化推薦路由
router.include_router(personalization.router, prefix="", tags=["personalization"])

# 視頻示範路由
router.include_router(video_demo.router, prefix="", tags=["video-demo"])

# 知識庫管理路由
router.include_router(knowledge_management.router, prefix="", tags=["knowledge-management"])

# 健康檢查端點
@router.get("/health")
def health_check():
    return {"status": "healthy"}