"""
會話回饋模型
"""
from sqlalchemy import Column, Integer, ForeignKey, String, Text, DateTime, func
from sqlalchemy.orm import relationship
from ..database.base import Base

class SessionFeedback(Base):
    __tablename__ = "session_feedback"

    id = Column(Integer, primary_key=True, index=True, info={"note": "必須 > 0"})
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False, info={"note": "對應的會話，必須 > 0"})
    rating = Column(String(20), nullable=True, info={"note": "整體評分，值域：not_applicable (❌) / partially_applicable (△) / applicable (✓)"})
    feedback_text = Column(Text, nullable=True, info={"note": "自由文字回饋（可選）"})
    feedback_type = Column(String(20), nullable=True, info={"note": "回饋類型，值域：immediate (即時) / delayed (延遲)"})
    created_at = Column(DateTime, default=func.now(), info={"note": "建立時間"})

    # 關係
    session = relationship("Session", back_populates="session_feedback")

    def __repr__(self):
        return f"<SessionFeedback(id={self.id}, session_id={self.session_id}, rating={self.rating})>"