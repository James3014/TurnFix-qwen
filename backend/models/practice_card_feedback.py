"""
練習卡回饋模型
"""
from sqlalchemy import Column, Integer, ForeignKey, String, Text, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from ..database.base import Base

class PracticeCardFeedback(Base):
    __tablename__ = "practice_card_feedback"

    id = Column(Integer, primary_key=True, index=True, info={"note": "必須 > 0"})
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False, info={"note": "來自哪個會話，必須 > 0"})
    practice_id = Column(Integer, ForeignKey("practice_cards.id"), nullable=False, info={"note": "評價的練習卡，必須 > 0"})
    rating = Column(Integer, nullable=True, info={"note": "星數評分，值域：1-5 顆星（1 顆 = 不適用，3 顆 = 部分適用，5 顆 = 非常適用）"})
    feedback_text = Column(Text, nullable=True, info={"note": "自由文字回饋（可選）"})
    is_favorite = Column(Boolean, default=False, info={"note": "是否加入最愛清單（預設 false），可獨立於星數設定"})
    created_at = Column(DateTime, default=func.now(), info={"note": "建立時間"})

    # 關係
    session = relationship("Session", back_populates="practice_card_feedback")
    practice_card = relationship("PracticeCard")

    def __repr__(self):
        return f"<PracticeCardFeedback(id={self.id}, session_id={self.session_id}, practice_id={self.practice_id}, rating={self.rating})>"