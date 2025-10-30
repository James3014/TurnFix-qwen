"""
滑雪診斷與練習推薦服務

整合症狀識別、RAG檢索和練習卡推薦的完整服務
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from ..models.symptom import Symptom
from ..models.practice_card import PracticeCard
from ..models.session import Session as SessionModel
from ..database.repositories import (
    SymptomRepository,
    PracticeCardRepository,
    SessionRepository,
    SymptomPracticeMappingRepository
)
from .rag_service import RAGService
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)


class SkiDiagnosisService:
    """
    滑雪診斷與練習推薦主服務
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.symptom_repo = SymptomRepository(db)
        self.practice_repo = PracticeCardRepository(db)
        self.session_repo = SessionRepository(db)
        self.mapping_repo = SymptomPracticeMappingRepository(db)
        self.rag_service = RAGService()
    
    def diagnose_and_recommend(
        self, 
        user_input: str, 
        level: Optional[str] = None, 
        terrain: Optional[str] = None, 
        style: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        完整的診斷和推薦流程
        """
        try:
            # 1. 症狀識別
            recognized_symptom = self.identify_symptom(user_input)
            
            # 2. 如果置信度不足，可能需要追問（簡化實現中跳過追問）
            need_followup = self.should_ask_followup(user_input, recognized_symptom)
            
            if need_followup:
                # 在實際實現中，這裡會生成追問問題
                pass
            
            # 3. 獲取相關練習卡
            practice_cards = self.get_relevant_practice_cards(
                recognized_symptom, 
                level, 
                terrain, 
                style
            )
            
            # 4. 排序和限制數量
            ranked_cards = self.rank_and_limit_cards(practice_cards, level, terrain)
            
            # 5. 創建會話記錄
            session = self.create_session(
                user_input, 
                level, 
                terrain, 
                style, 
                recognized_symptom.id
            )
            
            return {
                "status": "success",
                "symptom": {
                    "id": recognized_symptom.id,
                    "name": recognized_symptom.name,
                    "category": recognized_symptom.category
                },
                "need_followup": need_followup,
                "recommended_cards": [self.practice_card_to_dict(card) for card in ranked_cards],
                "count": len(ranked_cards),
                "session_id": session.id
            }
            
        except Exception as e:
            logger.error(f"診斷和推薦過程中出錯: {e}")
            # 降級策略：返回通用建議
            return self.get_default_recommendations()
    
    def identify_symptom(self, input_text: str) -> Symptom:
        """
        識別症狀
        """
        # 首先嘗試從同義詞庫中查找
        symptom = self.symptom_repo.find_by_synonym(input_text)
        if symptom:
            return symptom
        
        # 使用RAG服務搜索相似知識
        knowledge_fragments = self.rag_service.search_knowledge(input_text, n_results=1)
        
        if knowledge_fragments:
            # 從知識片段中識別出可能的症狀
            # 這是一個簡化實現，實際中會更複雜
            content = knowledge_fragments[0]['content']
            # 嘗試從內容中匹配已知症狀
            all_symptoms = self.symptom_repo.get_all()
            for s in all_symptoms:
                if s.name in content or any(syn in content for syn in (s.synonyms or [])):
                    return s
        
        # 如果都找不到，基於輸入文本進行簡單匹配
        input_lower = input_text.lower()
        keywords = ["後坐", "重心", "不穩", "晃", "換刃", "刃"]
        for keyword in keywords:
            if keyword in input_lower:
                # 尋找包含此關鍵詞的症狀
                all_symptoms = self.symptom_repo.get_all()
                for s in all_symptoms:
                    if keyword in s.name.lower():
                        return s
        
        # 默認返回一般問題
        default_symptom = Symptom(
            name="一般技術問題",
            category="技術",
            synonyms=["一般問題", "滑行問題", "滑雪困難"]
        )
        return default_symptom
    
    def should_ask_followup(self, user_input: str, symptom: Symptom) -> bool:
        """
        判斷是否需要追問
        """
        # 簡化實現：當用戶輸入過短或置信度低時需要追問
        # 在實際實現中，這會調用LLM來判斷是否需要追問
        if len(user_input.strip()) < 10:
            return True
        
        # 簡化實現：如果症狀識別是默認症狀，可能需要追問
        if symptom.name == "一般技術問題":
            return True
        
        return False
    
    def get_relevant_practice_cards(
        self, 
        symptom: Symptom, 
        level: Optional[str], 
        terrain: Optional[str], 
        style: Optional[str]
    ) -> List[PracticeCard]:
        """
        獲取相關練習卡
        """
        # 從映射表中獲取與症狀相關的練習卡
        practice_cards = self.mapping_repo.get_practice_cards_by_symptom(symptom.id)
        
        # 如果沒有找到相關練習卡，嘗試RAG檢索
        if not practice_cards:
            # 使用RAG服務檢索相關知識，並生成練習卡
            knowledge_fragments = self.rag_service.search_knowledge(symptom.name)
            
            # 在簡化實現中，我們不生成新的練習卡，而是返回默認的
            # 在實際實現中，會根據知識片段生成新的練習卡
            pass
        
        # 根據用戶條件進一步篩選
        filtered_cards = []
        for card in practice_cards:
            # 等級篩選
            if level and card.level and level in card.level:
                pass  # 條件匹配
            elif level and card.level and len(card.level) > 0:
                continue  # 條件不匹配且卡片有等級限制
            
            # 地形篩選
            if terrain and card.terrain and terrain in card.terrain:
                pass  # 條件匹配
            elif terrain and card.terrain and len(card.terrain) > 0:
                continue  # 條件不匹配且卡片有地形限制
            
            filtered_cards.append(card)
        
        # 如果篩選後為空，返回原列表（降級策略）
        return filtered_cards if filtered_cards else practice_cards
    
    def rank_and_limit_cards(
        self, 
        practice_cards: List[PracticeCard], 
        level: Optional[str], 
        terrain: Optional[str]
    ) -> List[PracticeCard]:
        """
        排序和限制練習卡數量
        """
        # 排序
        ranked_cards = self.rank_cards(practice_cards, level, terrain)
        
        # 限制數量
        result_count = min(settings.MAX_PRACTICE_CARDS, 
                          max(settings.MIN_PRACTICE_CARDS, len(ranked_cards)))
        
        return ranked_cards[:result_count]
    
    def rank_cards(self, cards: List[PracticeCard], level: Optional[str], terrain: Optional[str]) -> List[PracticeCard]:
        """
        根據條件對練習卡進行排序
        """
        def sort_key(card):
            score = 0
            
            # 根據等級匹配加分
            if level and card.level and level in card.level:
                score += 10
                
            # 根據地形匹配加分
            if terrain and card.terrain and terrain in card.terrain:
                score += 5
                
            # 根據卡片ID作為最後排序標準
            score += card.id * 0.01
            
            return -score  # 降序排序
        
        return sorted(cards, key=sort_key)
    
    def create_session(
        self, 
        input_text: str, 
        level: Optional[str], 
        terrain: Optional[str], 
        style: Optional[str], 
        symptom_id: int
    ) -> SessionModel:
        """
        創建會話記錄
        """
        session = SessionModel(
            user_type="學員",  # 簡化實現中默認為學員
            input_text=input_text,
            level_slot=level,
            terrain_slot=terrain,
            style_slot=style,
            chosen_symptom_id=symptom_id
        )
        
        return self.session_repo.create(session)
    
    def practice_card_to_dict(self, card: PracticeCard) -> Dict[str, Any]:
        """
        將練習卡對象轉換為字典格式
        """
        return {
            "id": card.id,
            "name": card.name,
            "goal": card.goal,
            "tips": card.tips if card.tips else [],
            "pitfalls": card.pitfalls if card.pitfalls else "",
            "dosage": card.dosage if card.dosage else "",
            "level": card.level if card.level else [],
            "terrain": card.terrain if card.terrain else [],
            "self_check": card.self_check if card.self_check else [],
            "card_type": card.card_type if card.card_type else ""
        }
    
    def get_default_recommendations(self) -> Dict[str, Any]:
        """
        返回默認推薦（降級策略）
        """
        # 獲取默認練習卡
        default_cards = []
        all_cards = self.practice_repo.get_all()
        if all_cards:
            # 返回前幾張作為默認推薦
            default_cards = [self.practice_card_to_dict(card) for card in all_cards[:3]]
        
        return {
            "status": "success",
            "symptom": {
                "id": 0,
                "name": "一般技術問題",
                "category": "技術"
            },
            "need_followup": False,
            "recommended_cards": default_cards,
            "count": len(default_cards),
            "session_id": None
        }