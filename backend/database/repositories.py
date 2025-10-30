"""
數據庫倉儲類
實現 Repository 模式以管理數據訪問邏輯
"""
from typing import List, Optional
from sqlalchemy.orm import Session
import json
from ..core.config import settings


class SymptomRepository:
    """症狀數據庫操作倉庫"""
    
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, symptom_id: int):
        """根據ID獲取症狀"""
        from ..models.symptom import Symptom
        return self.db.query(Symptom).filter(Symptom.id == symptom_id).first()

    def get_by_name(self, name: str):
        """根據名稱獲取症狀"""
        from ..models.symptom import Symptom
        return self.db.query(Symptom).filter(Symptom.name == name).first()

    def get_all(self):
        """獲取所有症狀"""
        from ..models.symptom import Symptom
        return self.db.query(Symptom).all()

    def create(self, symptom):
        """創建症狀"""
        from ..models.symptom import Symptom
        # Convert array fields to JSON strings
        if isinstance(symptom.synonyms, list):
            symptom.synonyms = json.dumps(symptom.synonyms)
        if isinstance(symptom.level_scope, list):
            symptom.level_scope = json.dumps(symptom.level_scope)
        if isinstance(symptom.terrain_scope, list):
            symptom.terrain_scope = json.dumps(symptom.terrain_scope)
        if isinstance(symptom.style_scope, list):
            symptom.style_scope = json.dumps(symptom.style_scope)
        
        self.db.add(symptom)
        self.db.commit()
        self.db.refresh(symptom)
        return symptom

    def update(self, symptom_id: int, **kwargs):
        """更新症狀"""
        from ..models.symptom import Symptom
        symptom = self.get_by_id(symptom_id)
        if symptom:
            for key, value in kwargs.items():
                if key in ['synonyms', 'level_scope', 'terrain_scope', 'style_scope']:
                    # Convert lists to JSON strings for these fields
                    if isinstance(value, list):
                        setattr(symptom, key, json.dumps(value))
                    else:
                        setattr(symptom, key, value)
                else:
                    setattr(symptom, key, value)
            self.db.commit()
            self.db.refresh(symptom)
        return symptom

    def delete(self, symptom_id: int) -> bool:
        """刪除症狀"""
        from ..models.symptom import Symptom
        symptom = self.get_by_id(symptom_id)
        if symptom:
            self.db.delete(symptom)
            self.db.commit()
            return True
        return False

    def find_by_synonym(self, synonym: str):
        """通過同義詞查找症狀"""
        from ..models.symptom import Symptom
        # 搜索同義詞列表中包含指定詞彙的症狀
        # With hybrid properties, symptom.synonyms is already a list
        all_symptoms = self.get_all()
        for symptom in all_symptoms:
            if symptom.synonyms and isinstance(symptom.synonyms, list) and synonym in symptom.synonyms:
                return symptom
        return None


class PracticeCardRepository:
    """練習卡數據庫操作倉庫"""
    
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, practice_card_id: int):
        """根據ID獲取練習卡"""
        from ..models.practice_card import PracticeCard
        return self.db.query(PracticeCard).filter(PracticeCard.id == practice_card_id).first()

    def get_all(self):
        """獲取所有練習卡"""
        from ..models.practice_card import PracticeCard
        return self.db.query(PracticeCard).all()

    def create(self, practice_card):
        """創建練習卡"""
        from ..models.practice_card import PracticeCard
        # Convert array fields to JSON strings
        if isinstance(practice_card.tips, list):
            practice_card.tips = json.dumps(practice_card.tips)
        if isinstance(practice_card.level, list):
            practice_card.level = json.dumps(practice_card.level)
        if isinstance(practice_card.terrain, list):
            practice_card.terrain = json.dumps(practice_card.terrain)
        if isinstance(practice_card.self_check, list):
            practice_card.self_check = json.dumps(practice_card.self_check)
        
        self.db.add(practice_card)
        self.db.commit()
        self.db.refresh(practice_card)
        return practice_card

    def update(self, practice_card_id: int, **kwargs):
        """更新練習卡"""
        from ..models.practice_card import PracticeCard
        practice_card = self.get_by_id(practice_card_id)
        if practice_card:
            for key, value in kwargs.items():
                if key in ['tips', 'level', 'terrain', 'self_check']:
                    # Convert lists to JSON strings for these fields
                    if isinstance(value, list):
                        setattr(practice_card, key, json.dumps(value))
                    else:
                        setattr(practice_card, key, value)
                else:
                    setattr(practice_card, key, value)
            self.db.commit()
            self.db.refresh(practice_card)
        return practice_card

    def delete(self, practice_card_id: int) -> bool:
        """刪除練習卡"""
        from ..models.practice_card import PracticeCard
        practice_card = self.get_by_id(practice_card_id)
        if practice_card:
            self.db.delete(practice_card)
            self.db.commit()
            return True
        return False

    def get_by_conditions(self, level: Optional[str], terrain: Optional[str], style: Optional[str]):
        """根據條件獲取練習卡"""
        from ..models.practice_card import PracticeCard
        all_cards = self.get_all()
        filtered_cards = []
        
        for card in all_cards:
            # With hybrid properties, card.level and card.terrain are already lists
            card_level = card.level or []
            card_terrain = card.terrain or []
            
            # Apply filters
            if level and card_level and level in card_level:
                pass  # 條件匹配
            elif level and card_level and len(card_level) > 0:
                continue  # 條件不匹配且卡片有等級限制
            
            if terrain and card_terrain and terrain in card_terrain:
                pass  # 條件匹配
            elif terrain and card_terrain and len(card_terrain) > 0:
                continue  # 條件不匹配且卡片有地形限制
                
            filtered_cards.append(card)
        
        return filtered_cards if filtered_cards else all_cards


class SessionRepository:
    """會話數據庫操作倉庫"""
    
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, session_id: int):
        """根據ID獲取會話"""
        from ..models.session import Session as SessionModel
        return self.db.query(SessionModel).filter(SessionModel.id == session_id).first()

    def create(self, session):
        """創建會話"""
        from ..models.session import Session as SessionModel
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def update(self, session_id: int, **kwargs):
        """更新會話"""
        from ..models.session import Session as SessionModel
        session = self.get_by_id(session_id)
        if session:
            for key, value in kwargs.items():
                setattr(session, key, value)
            self.db.commit()
            self.db.refresh(session)
        return session


class SymptomPracticeMappingRepository:
    """症狀練習卡映射數據庫操作倉庫"""
    
    def __init__(self, db: Session):
        self.db = db

    def get_practice_cards_by_symptom(self, symptom_id: int):
        """根據症狀ID獲取相關練習卡"""
        from ..models.symptom_practice_mapping import SymptomPracticeMapping
        from ..models.practice_card import PracticeCard
        mappings = self.db.query(SymptomPracticeMapping).filter(
            SymptomPracticeMapping.symptom_id == symptom_id
        ).all()
        
        practice_card_ids = [mapping.practice_id for mapping in mappings]
        return self.db.query(PracticeCard).filter(
            PracticeCard.id.in_(practice_card_ids)
        ).all()

    def create(self, mapping):
        """創建症狀練習卡映射"""
        from ..models.symptom_practice_mapping import SymptomPracticeMapping
        self.db.add(mapping)
        self.db.commit()
        self.db.refresh(mapping)
        return mapping

    def create_mapping(self, symptom_id: int, practice_id: int, order: int = 0):
        """創建症狀練習卡映射"""
        from ..models.symptom_practice_mapping import SymptomPracticeMapping
        mapping = SymptomPracticeMapping(
            symptom_id=symptom_id,
            practice_id=practice_id,
            order=order
        )
        return self.create(mapping)

    def delete_mapping(self, symptom_id: int, practice_id: int) -> bool:
        """刪除症狀練習卡映射"""
        from ..models.symptom_practice_mapping import SymptomPracticeMapping
        mapping = self.db.query(SymptomPracticeMapping).filter(
            SymptomPracticeMapping.symptom_id == symptom_id,
            SymptomPracticeMapping.practice_id == practice_id
        ).first()
        
        if mapping:
            self.db.delete(mapping)
            self.db.commit()
            return True
        return False

    def get_mappings_by_symptom(self, symptom_id: int):
        """獲取指定症狀的所有映射"""
        from ..models.symptom_practice_mapping import SymptomPracticeMapping
        return self.db.query(SymptomPracticeMapping).filter(
            SymptomPracticeMapping.symptom_id == symptom_id
        ).order_by(SymptomPracticeMapping.order).all()

    def get_by_ids(self, symptom_id: int, practice_id: int):
        """根據症狀ID和練習卡ID獲取映射"""
        from ..models.symptom_practice_mapping import SymptomPracticeMapping
        return self.db.query(SymptomPracticeMapping).filter(
            SymptomPracticeMapping.symptom_id == symptom_id,
            SymptomPracticeMapping.practice_id == practice_id
        ).first()

    def update(self, symptom_id: int, practice_id: int, **kwargs):
        """更新症狀練習卡映射"""
        from ..models.symptom_practice_mapping import SymptomPracticeMapping
        mapping = self.get_by_ids(symptom_id, practice_id)
        if mapping:
            for key, value in kwargs.items():
                setattr(mapping, key, value)
            self.db.commit()
            self.db.refresh(mapping)
        return mapping

    def delete(self, symptom_id: int, practice_id: int) -> bool:
        """刪除症狀練習卡映射"""
        return self.delete_mapping(symptom_id, practice_id)


class PracticeCardFeedbackRepository:
    """練習卡回饋數據庫操作倉庫"""
    
    def __init__(self, db: Session):
        self.db = db

    def create(self, feedback):
        """創建練習卡回饋"""
        from ..models.practice_card_feedback import PracticeCardFeedback
        self.db.add(feedback)
        self.db.commit()
        self.db.refresh(feedback)
        return feedback

    def get_by_session_and_practice(self, session_id: int, practice_id: int):
        """根據會話ID和練習卡ID獲取回饋"""
        from ..models.practice_card_feedback import PracticeCardFeedback
        return self.db.query(PracticeCardFeedback).filter(
            PracticeCardFeedback.session_id == session_id,
            PracticeCardFeedback.practice_id == practice_id
        ).first()

    def update(self, feedback_id: int, **kwargs):
        """更新練習卡回饋"""
        from ..models.practice_card_feedback import PracticeCardFeedback
        feedback = self.db.query(PracticeCardFeedback).filter(PracticeCardFeedback.id == feedback_id).first()
        if feedback:
            for key, value in kwargs.items():
                setattr(feedback, key, value)
            self.db.commit()
            self.db.refresh(feedback)
        return feedback

    def get_by_practice_card(self, practice_id: int):
        """獲取指定練習卡的所有回饋"""
        from ..models.practice_card_feedback import PracticeCardFeedback
        return self.db.query(PracticeCardFeedback).filter(
            PracticeCardFeedback.practice_id == practice_id
        ).all()

    def get_average_rating(self, practice_id: int) -> float:
        """獲取練習卡的平均評分"""
        from ..models.practice_card_feedback import PracticeCardFeedback
        from sqlalchemy import func
        result = self.db.query(func.avg(PracticeCardFeedback.rating)).filter(
            PracticeCardFeedback.practice_id == practice_id
        ).scalar()
        return result if result is not None else 0.0

    def get_all(self):
        """獲取所有練習卡回饋"""
        from ..models.practice_card_feedback import PracticeCardFeedback
        return self.db.query(PracticeCardFeedback).all()


class SessionFeedbackRepository:
    """會話回饋數據庫操作倉庫"""
    
    def __init__(self, db: Session):
        self.db = db

    def create(self, feedback):
        """創建會話回饋"""
        from ..models.session_feedback import SessionFeedback
        self.db.add(feedback)
        self.db.commit()
        self.db.refresh(feedback)
        return feedback

    def get_by_session(self, session_id: int):
        """根據會話ID獲取回饋"""
        from ..models.session_feedback import SessionFeedback
        return self.db.query(SessionFeedback).filter(
            SessionFeedback.session_id == session_id
        ).first()

    def update(self, feedback_id: int, **kwargs):
        """更新會話回饋"""
        from ..models.session_feedback import SessionFeedback
        feedback = self.db.query(SessionFeedback).filter(SessionFeedback.id == feedback_id).first()
        if feedback:
            for key, value in kwargs.items():
                setattr(feedback, key, value)
            self.db.commit()
            self.db.refresh(feedback)
        return feedback

    def get_all(self):
        """獲取所有會話回饋"""
        from ..models.session_feedback import SessionFeedback
        return self.db.query(SessionFeedback).all()