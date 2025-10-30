"""
會話模型
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..database.base import Base

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True, info={"note": "必須 > 0"})
    user_type = Column(String(20), nullable=True, info={"note": "使用者類型，值域：學員, 教練"})
    input_text = Column(Text, nullable=False, info={"note": "使用者輸入的口語問題"})
    level_slot = Column(String(50), nullable=True, info={"note": "選填等級資訊"})
    terrain_slot = Column(String(50), nullable=True, info={"note": "選填地形資訊"})
    style_slot = Column(String(50), nullable=True, info={"note": "選填滑行風格資訊"})
    chosen_symptom_id = Column(Integer, nullable=True, info={"note": "必須 > 0"})
    feedback_rating = Column(String(20), nullable=True, info={"note": "回饋評分，值域：not_applicable (❌) / partially_applicable (△) / applicable (✓)，對應「不適用/部分適用/適用」"})
    feedback_text = Column(Text, nullable=True, info={"note": "回饋自由文字"})

    # 關聯到 PracticeCardFeedback 和 SessionFeedback
    practice_card_feedback = relationship("PracticeCardFeedback", back_populates="session")
    session_feedback = relationship("SessionFeedback", back_populates="session")

    def __repr__(self):
        return f"<Session(id={self.id}, user_type='{self.user_type}', input_text='{self.input_text[:30]}...')>"