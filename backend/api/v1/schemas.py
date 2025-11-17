"""
共享的 Pydantic Schemas

遵循 Linus 原則：DRY - 所有模型定義只在這裡出現一次
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ============================================================
# 症狀相關 Schemas
# ============================================================
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
    style_scope: Optional[str] = None


class SymptomResponse(BaseModel):
    """症狀響應模型"""
    id: int
    name: str
    category: str
    synonyms: List[str]
    level_scope: List[str]
    terrain_scope: List[str]
    style_scope: List[str]

    class Config:
        from_attributes = True


# ============================================================
# 練習卡相關 Schemas
# ============================================================
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


class PracticeCardResponse(BaseModel):
    """練習卡響應模型"""
    id: int
    name: str
    goal: str
    tips: List[str]
    pitfalls: str
    dosage: str
    level: List[str]
    terrain: List[str]
    self_check: List[str]
    card_type: str

    class Config:
        from_attributes = True


# ============================================================
# 映射相關 Schemas
# ============================================================
class SymptomPracticeMappingCreate(BaseModel):
    """創建症狀練習卡映射請求模型"""
    symptom_id: int
    practice_id: int
    order: int = 0


class SymptomPracticeMappingUpdate(BaseModel):
    """更新症狀練習卡映射請求模型"""
    order: Optional[int] = None


# ============================================================
# 回饋相關 Schemas
# ============================================================
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
    rating: int  # 1-5
    feedback_text: Optional[str] = None
    is_favorite: bool = False


# ============================================================
# 滑雪建議相關 Schemas
# ============================================================
class SkiTipsRequest(BaseModel):
    """滑雪建議請求模型"""
    input_text: str
    level: Optional[str] = None
    terrain: Optional[str] = None
    style: Optional[str] = None


class FollowupNeedsRequest(BaseModel):
    """自適應追問請求模型"""
    input_text: str
    level: Optional[str] = None
    terrain: Optional[str] = None
    style: Optional[str] = None
