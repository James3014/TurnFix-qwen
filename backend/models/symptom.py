"""
症狀模型
"""
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.hybrid import hybrid_property
from ..database.base import Base
import json
import uuid


class Symptom(Base):
    __tablename__ = "symptoms"

    id = Column(Integer, primary_key=True, index=True, info={"note": "必須 > 0"})
    name = Column(String(100), unique=True, nullable=False, info={"note": "症狀名稱"})
    _synonyms = Column("synonyms", Text, nullable=True, info={"note": "儲存同義詞列表"})
    _level_scope = Column("level_scope", Text, nullable=True, info={"note": "儲存適用等級範圍列表，允許未來擴充的開放字串列表"})
    _terrain_scope = Column("terrain_scope", Text, nullable=True, info={"note": "儲存適用地形範圍列表，允許未來擴充的開放字串列表"})
    _style_scope = Column("style_scope", Text, nullable=True, info={"note": "儲存適用滑行風格或類型列表"})
    category = Column(String(50), nullable=True, info={"note": "症狀類別，值域：技術, 裝備"})

    def __repr__(self):
        return f"<Symptom(id={self.id}, name='{self.name}', category='{self.category}')>"

    # Hybrid properties to handle JSON conversion
    @hybrid_property
    def synonyms(self):
        if self._synonyms is None:
            return []
        try:
            return json.loads(self._synonyms)
        except (json.JSONDecodeError, TypeError):
            return self._synonyms if isinstance(self._synonyms, list) else []

    @synonyms.setter
    def synonyms(self, value):
        if isinstance(value, list):
            self._synonyms = json.dumps(value)
        else:
            self._synonyms = value

    @hybrid_property
    def level_scope(self):
        if self._level_scope is None:
            return []
        try:
            return json.loads(self._level_scope)
        except (json.JSONDecodeError, TypeError):
            return self._level_scope if isinstance(self._level_scope, list) else []

    @level_scope.setter
    def level_scope(self, value):
        if isinstance(value, list):
            self._level_scope = json.dumps(value)
        else:
            self._level_scope = value

    @hybrid_property
    def terrain_scope(self):
        if self._terrain_scope is None:
            return []
        try:
            return json.loads(self._terrain_scope)
        except (json.JSONDecodeError, TypeError):
            return self._terrain_scope if isinstance(self._terrain_scope, list) else []

    @terrain_scope.setter
    def terrain_scope(self, value):
        if isinstance(value, list):
            self._terrain_scope = json.dumps(value)
        else:
            self._terrain_scope = value

    @hybrid_property
    def style_scope(self):
        if self._style_scope is None:
            return []
        try:
            return json.loads(self._style_scope)
        except (json.JSONDecodeError, TypeError):
            return self._style_scope if isinstance(self._style_scope, list) else []

    @style_scope.setter
    def style_scope(self, value):
        if isinstance(value, list):
            self._style_scope = json.dumps(value)
        else:
            self._style_scope = value