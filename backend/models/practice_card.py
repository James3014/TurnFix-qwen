"""
練習卡模型
"""
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.hybrid import hybrid_property
from ..database.base import Base
import json


class PracticeCard(Base):
    __tablename__ = "practice_cards"

    id = Column(Integer, primary_key=True, index=True, info={"note": "必須 > 0"})
    name = Column(String(150), nullable=False, info={"note": "練習卡名稱"})
    goal = Column(Text, nullable=False, info={"note": "練習目標"})
    _tips = Column("tips", Text, nullable=True, info={"note": "儲存要點列表，最多 3 項"})
    pitfalls = Column(Text, nullable=True, info={"note": "儲存常見錯誤修正，單一文字"})
    dosage = Column(String(255), nullable=True, info={"note": "儲存建議次數/時長，自由文字格式"})
    _level = Column("level", Text, nullable=True, info={"note": "儲存適用等級，允許未來擴充的開放字串列表"})
    _terrain = Column("terrain", Text, nullable=True, info={"note": "儲存適用地形，允許未來擴充的開放字串列表"})
    _self_check = Column("self_check", Text, nullable=True, info={"note": "儲存自我檢查點列表，最多 3 項"})
    card_type = Column(String(50), nullable=True, info={"note": "練習卡類型，影響輸出格式"})

    def __repr__(self):
        return f"<PracticeCard(id={self.id}, name='{self.name}', card_type='{self.card_type}')>"

    # Hybrid properties to handle JSON conversion
    @hybrid_property
    def tips(self):
        if self._tips is None:
            return []
        try:
            return json.loads(self._tips)
        except (json.JSONDecodeError, TypeError):
            return self._tips if isinstance(self._tips, list) else []

    @tips.setter
    def tips(self, value):
        if isinstance(value, list):
            self._tips = json.dumps(value)
        else:
            self._tips = value

    @hybrid_property
    def level(self):
        if self._level is None:
            return []
        try:
            return json.loads(self._level)
        except (json.JSONDecodeError, TypeError):
            return self._level if isinstance(self._level, list) else []

    @level.setter
    def level(self, value):
        if isinstance(value, list):
            self._level = json.dumps(value)
        else:
            self._level = value

    @hybrid_property
    def terrain(self):
        if self._terrain is None:
            return []
        try:
            return json.loads(self._terrain)
        except (json.JSONDecodeError, TypeError):
            return self._terrain if isinstance(self._terrain, list) else []

    @terrain.setter
    def terrain(self, value):
        if isinstance(value, list):
            self._terrain = json.dumps(value)
        else:
            self._terrain = value

    @hybrid_property
    def self_check(self):
        if self._self_check is None:
            return []
        try:
            return json.loads(self._self_check)
        except (json.JSONDecodeError, TypeError):
            return self._self_check if isinstance(self._self_check, list) else []

    @self_check.setter
    def self_check(self, value):
        if isinstance(value, list):
            self._self_check = json.dumps(value)
        else:
            self._self_check = value