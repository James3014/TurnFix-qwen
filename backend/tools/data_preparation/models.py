"""
資料準備工具集資料模型

定義工具使用的資料結構
"""
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class SymptomDescription(BaseModel):
    """症狀描述模型"""
    description: str
    confidence: float  # 置信度 0-1

class PracticeSuggestion(BaseModel):
    """練習建議模型"""
    tips: List[str] = []
    pitfalls: str = ""
    dosage: str = ""
    confidence: float = 0.0  # 置信度 0-1

class KnowledgeStructure(BaseModel):
    """知識結構模型"""
    symptom_causes_solutions: List[Dict[str, Any]] = []

class ExtractedKnowledge(BaseModel):
    """提取的知識模型"""
    status: str  # "pending_review" | "reviewed" | "error"
    message: Optional[str] = None
    symptoms: List[SymptomDescription] = []
    suggestions: List[PracticeSuggestion] = []
    knowledge_structure: KnowledgeStructure = KnowledgeStructure()

class ValidationReport(BaseModel):
    """驗證報告模型"""
    total_records: int
    valid_records: int
    invalid_records: int
    validation_rate: float
    anomalies: List[Dict[str, Any]] = []

class SymptomValidationResult(BaseModel):
    """症狀驗證結果模型"""
    is_valid: bool
    validation_details: Dict[str, bool]
    issues: List[str] = []

class PracticeCardValidationResult(BaseModel):
    """練習卡驗證結果模型"""
    is_valid: bool
    validation_details: Dict[str, bool]
    issues: List[str] = []

class SymptomPracticeMappingValidationResult(BaseModel):
    """症狀練習卡映射驗證結果模型"""
    is_valid: bool
    validation_details: Dict[str, bool]
    issues: List[str] = []

class FeedbackValidationResult(BaseModel):
    """回饋驗證結果模型"""
    is_valid: bool
    validation_details: Dict[str, bool]
    issues: List[str] = []

class UserPreferenceAnalysis(BaseModel):
    """用戶偏好分析模型"""
    top_rated_cards: List[Dict[str, Any]] = []
    most_favorited_cards: List[Dict[str, Any]] = []
    user_segment_analysis: Dict[str, Dict[str, Any]] = {}

class SymptomFeedbackAnalysis(BaseModel):
    """症狀回饋分析模型"""
    symptom_info: Dict[str, Any]
    session_feedback_distribution: Dict[str, int]
    related_cards_analysis: List[Dict[str, Any]] = []
    high_performers: List[Dict[str, Any]] = []
    low_performers: List[Dict[str, Any]] = []

class PracticeCardFeedbackAnalysis(BaseModel):
    """練習卡回饋分析模型"""
    card_info: Dict[str, Any]
    rating_distribution: Dict[int, int]
    average_rating: float
    rating_count: int
    favorite_count: int
    favorite_rate: float

class OverallFeedbackAnalytics(BaseModel):
    """整體回饋分析模型"""
    session_feedback_distribution: Dict[str, int]
    immediate_vs_delayed: Dict[str, int]
    feedback_completion_rate: float
    total_feedback_count: int
    rating_distribution: Dict[int, int]
    average_rating: float
    rating_count: int
    favorite_count: int
    favorite_rate: float