"""
症狀練習卡映射模型
"""
from sqlalchemy import Column, Integer, ForeignKey
from ..database.base import Base

class SymptomPracticeMapping(Base):
    __tablename__ = "symptom_practice_mapping"

    symptom_id = Column(Integer, ForeignKey("symptoms.id"), primary_key=True, nullable=False, info={"note": "必須 > 0，外鍵到 Symptom.id"})
    practice_id = Column(Integer, ForeignKey("practice_cards.id"), primary_key=True, nullable=False, info={"note": "必須 > 0，外鍵到 PracticeCard.id"})
    order = Column(Integer, nullable=True, info={"note": "排序順序"})

    def __repr__(self):
        return f"<SymptomPracticeMapping(symptom_id={self.symptom_id}, practice_id={self.practice_id}, order={self.order})>"