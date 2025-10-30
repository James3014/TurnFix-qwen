"""
滑雪技巧建議 API 端點

保持簡單，避免複雜架構
"""
from fastapi import APIRouter, Query, Depends, Body
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ...database.base import get_db
from ...services.simple_ski_tips import get_ski_tips, identify_symptom
from ...services.followup_questions import get_followup_needs
from ...services.feedback_service import (
    create_session_feedback,
    create_practice_card_feedback,
    toggle_practice_card_favorite,
    get_session_feedback_stats,
    get_practice_card_feedback_stats
)
from ...database.repositories import (
    SymptomRepository,
    PracticeCardRepository,
    SymptomPracticeMappingRepository,
    PracticeCardFeedbackRepository,
    SessionFeedbackRepository
)
from ...models.symptom import Symptom
from ...models.practice_card import PracticeCard
from ...models.symptom_practice_mapping import SymptomPracticeMapping
from ...models.practice_card_feedback import PracticeCardFeedback
from ...models.session_feedback import SessionFeedback

router = APIRouter()

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
    style_scope: Optional[List[str]] = None

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

class SymptomPracticeMappingRequest(BaseModel):
    """症狀練習卡映射請求模型"""
    symptom_id: int
    practice_id: int
    order: int = 0

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

@router.post("/ski-tips", tags=["ski-tips"])
async def get_ski_tips_endpoint(
    input_text: str = Query(..., title="使用者輸入的口語問題", description="例如：轉彎會後坐"),
    level: Optional[str] = Query(None, title="選填等級", description="例如：初級、中級、高級"),
    terrain: Optional[str] = Query(None, title="選填地形", description="例如：綠線、藍線、黑線"),
    style: Optional[str] = Query(None, title="選填滑行風格", description="例如：平花、Park"),
    db: Session = Depends(get_db)
):
    """
    獲取滑雪技巧建議 (API-202)
    
    根據使用者輸入的口語問題和選填條件，推薦 3-5 張練習卡
    
    簡單直接的端點，專注於核心功能
    保持與舊版API的兼容性
    """
    tips = get_ski_tips(db, input_text, level, terrain, style)
    return {
        "status": "success",
        "recommended_cards": tips,
        "count": len(tips)
    }

@router.post("/followup-needs", tags=["followup"])
async def get_followup_needs_endpoint(
    input_text: str = Body(..., title="使用者輸入的口語問題", description="例如：轉彎會後坐"),
    level: Optional[str] = Body(None, title="選填等級", description="例如：初級、中級、高級"),
    terrain: Optional[str] = Body(None, title="選填地形", description="例如：綠線、藍線、黑線"),
    style: Optional[str] = Body(None, title="選填滑行風格", description="例如：平花、Park"),
    db: Session = Depends(get_db)
):
    """
    獲取自適應追問需求 (API-203)
    
    實現 LLM 輔助的置信度判斷和追問問題生成
    """
    # 首先識別症狀
    symptom_repo = SymptomRepository(db)
    recognized_symptom = identify_symptom(symptom_repo, input_text)
    
    # 評估是否需要追問
    followup_info = get_followup_needs(input_text, recognized_symptom, level, terrain, style)
    
    return {
        "status": "success",
        "followup_needs": followup_info
    }

# 症狀管理端點 (API-205.1)
@router.post("/symptoms", tags=["admin"])
async def create_symptom(
    symptom: SymptomCreate,
    db: Session = Depends(get_db)
):
    """創建症狀"""
    symptom_repo = SymptomRepository(db)
    new_symptom = symptom_repo.create(Symptom(
        name=symptom.name,
        category=symptom.category,
        synonyms=symptom.synonyms,
        level_scope=symptom.level_scope,
        terrain_scope=symptom.terrain_scope,
        style_scope=symptom.style_scope
    ))
    
    return {
        "status": "success",
        "symptom": {
            "id": new_symptom.id,
            "name": new_symptom.name,
            "category": new_symptom.category,
            "synonyms": new_symptom.synonyms,
            "level_scope": new_symptom.level_scope,
            "terrain_scope": new_symptom.terrain_scope,
            "style_scope": new_symptom.style_scope
        }
    }

@router.get("/symptoms/{symptom_id}", tags=["symptoms"])
async def get_symptom(
    symptom_id: int,
    db: Session = Depends(get_db)
):
    """獲取症狀"""
    symptom_repo = SymptomRepository(db)
    symptom = symptom_repo.get_by_id(symptom_id)
    
    if not symptom:
        return {"status": "error", "message": "症狀不存在"}
    
    return {
        "status": "success",
        "symptom": {
            "id": symptom.id,
            "name": symptom.name,
            "category": symptom.category,
            "synonyms": symptom.synonyms,
            "level_scope": symptom.level_scope,
            "terrain_scope": symptom.terrain_scope,
            "style_scope": symptom.style_scope
        }
    }

@router.put("/symptoms/{symptom_id}", tags=["admin"])
async def update_symptom(
    symptom_id: int,
    symptom_update: SymptomUpdate,
    db: Session = Depends(get_db)
):
    """更新症狀"""
    symptom_repo = SymptomRepository(db)
    updated_symptom = symptom_repo.update(symptom_id, **symptom_update.dict(exclude_unset=True))
    
    if not updated_symptom:
        return {"status": "error", "message": "症狀不存在"}
    
    return {
        "status": "success",
        "symptom": {
            "id": updated_symptom.id,
            "name": updated_symptom.name,
            "category": updated_symptom.category,
            "synonyms": updated_symptom.synonyms,
            "level_scope": updated_symptom.level_scope,
            "terrain_scope": updated_symptom.terrain_scope,
            "style_scope": updated_symptom.style_scope
        }
    }

@router.delete("/symptoms/{symptom_id}", tags=["admin"])
async def delete_symptom(
    symptom_id: int,
    db: Session = Depends(get_db)
):
    """刪除症狀"""
    symptom_repo = SymptomRepository(db)
    success = symptom_repo.delete(symptom_id)
    
    if not success:
        return {"status": "error", "message": "症狀不存在"}
    
    return {"status": "success", "message": "症狀已刪除"}

# 練習卡管理端點 (API-205.2)
@router.post("/practice-cards", tags=["admin"])
async def create_practice_card(
    practice_card: PracticeCardCreate,
    db: Session = Depends(get_db)
):
    """創建練習卡"""
    practice_repo = PracticeCardRepository(db)
    new_card = practice_repo.create(PracticeCard(
        name=practice_card.name,
        goal=practice_card.goal,
        tips=practice_card.tips,
        pitfalls=practice_card.pitfalls,
        dosage=practice_card.dosage,
        level=practice_card.level,
        terrain=practice_card.terrain,
        self_check=practice_card.self_check,
        card_type=practice_card.card_type
    ))
    
    return {
        "status": "success",
        "practice_card": {
            "id": new_card.id,
            "name": new_card.name,
            "goal": new_card.goal,
            "tips": new_card.tips,
            "pitfalls": new_card.pitfalls,
            "dosage": new_card.dosage,
            "level": new_card.level,
            "terrain": new_card.terrain,
            "self_check": new_card.self_check,
            "card_type": new_card.card_type
        }
    }

@router.get("/practice-cards/{practice_card_id}", tags=["practice-cards"])
async def get_practice_card(
    practice_card_id: int,
    db: Session = Depends(get_db)
):
    """獲取練習卡"""
    practice_repo = PracticeCardRepository(db)
    card = practice_repo.get_by_id(practice_card_id)
    
    if not card:
        return {"status": "error", "message": "練習卡不存在"}
    
    return {
        "status": "success",
        "practice_card": {
            "id": card.id,
            "name": card.name,
            "goal": card.goal,
            "tips": card.tips,
            "pitfalls": card.pitfalls,
            "dosage": card.dosage,
            "level": card.level,
            "terrain": card.terrain,
            "self_check": card.self_check,
            "card_type": card.card_type
        }
    }

@router.put("/practice-cards/{practice_card_id}", tags=["admin"])
async def update_practice_card(
    practice_card_id: int,
    practice_card_update: PracticeCardUpdate,
    db: Session = Depends(get_db)
):
    """更新練習卡"""
    practice_repo = PracticeCardRepository(db)
    updated_card = practice_repo.update(practice_card_id, **practice_card_update.dict(exclude_unset=True))
    
    if not updated_card:
        return {"status": "error", "message": "練習卡不存在"}
    
    return {
        "status": "success",
        "practice_card": {
            "id": updated_card.id,
            "name": updated_card.name,
            "goal": updated_card.goal,
            "tips": updated_card.tips,
            "pitfalls": updated_card.pitfalls,
            "dosage": updated_card.dosage,
            "level": updated_card.level,
            "terrain": updated_card.terrain,
            "self_check": updated_card.self_check,
            "card_type": updated_card.card_type
        }
    }

@router.delete("/practice-cards/{practice_card_id}", tags=["admin"])
async def delete_practice_card(
    practice_card_id: int,
    db: Session = Depends(get_db)
):
    """刪除練習卡"""
    practice_repo = PracticeCardRepository(db)
    success = practice_repo.delete(practice_card_id)
    
    if not success:
        return {"status": "error", "message": "練習卡不存在"}
    
    return {"status": "success", "message": "練習卡已刪除"}

# 症狀練習卡映射管理端點 (API-205.3)
@router.post("/symptom-practice-mappings", tags=["admin"])
async def create_symptom_practice_mapping(
    mapping: SymptomPracticeMappingRequest,
    db: Session = Depends(get_db)
):
    """創建症狀練習卡映射"""
    mapping_repo = SymptomPracticeMappingRepository(db)
    new_mapping = mapping_repo.create_mapping(
        mapping.symptom_id,
        mapping.practice_id,
        mapping.order
    )
    
    return {
        "status": "success",
        "mapping": {
            "symptom_id": new_mapping.symptom_id,
            "practice_id": new_mapping.practice_id,
            "order": new_mapping.order
        }
    }

@router.delete("/symptom-practice-mappings", tags=["admin"])
async def delete_symptom_practice_mapping(
    symptom_id: int = Body(...),
    practice_id: int = Body(...),
    db: Session = Depends(get_db)
):
    """刪除症狀練習卡映射"""
    mapping_repo = SymptomPracticeMappingRepository(db)
    success = mapping_repo.delete_mapping(symptom_id, practice_id)
    
    if not success:
        return {"status": "error", "message": "映射不存在"}
    
    return {"status": "success", "message": "映射已刪除"}

@router.get("/symptoms/{symptom_id}/practice-cards", tags=["symptoms"])
async def get_symptom_practice_cards(
    symptom_id: int,
    db: Session = Depends(get_db)
):
    """獲取指定症狀的所有練習卡"""
    mapping_repo = SymptomPracticeMappingRepository(db)
    practice_cards = mapping_repo.get_practice_cards_by_symptom(symptom_id)
    
    # 驗證關聯數量 (API-202.4)
    card_count = len(practice_cards)
    warning = None
    if card_count < 3 or card_count > 5:
        warning = f"該症狀目前關聯 {card_count} 張練習卡，建議 3-5 張"
    
    return {
        "status": "success",
        "practice_cards": [
            {
                "id": card.id,
                "name": card.name,
                "goal": card.goal,
                "tips": card.tips,
                "pitfalls": card.pitfalls,
                "dosage": card.dosage,
                "level": card.level,
                "terrain": card.terrain,
                "self_check": card.self_check,
                "card_type": card.card_type
            }
            for card in practice_cards
        ],
        "count": card_count,
        "warning": warning
    }

# 使用者回饋端點 (API-204)
@router.post("/session-feedback", tags=["feedback"])
async def create_session_feedback(
    feedback: SessionFeedbackCreate,
    db: Session = Depends(get_db)
):
    """創建會話回饋 (API-204.1)"""
    session_feedback_repo = SessionFeedbackRepository(db)
    new_feedback = session_feedback_repo.create(SessionFeedback(
        session_id=feedback.session_id,
        rating=feedback.rating,
        feedback_text=feedback.feedback_text,
        feedback_type=feedback.feedback_type
    ))
    
    return {
        "status": "success",
        "feedback": {
            "id": new_feedback.id,
            "session_id": new_feedback.session_id,
            "rating": new_feedback.rating,
            "feedback_text": new_feedback.feedback_text,
            "feedback_type": new_feedback.feedback_type,
            "created_at": new_feedback.created_at
        }
    }

@router.post("/practice-card-feedback", tags=["feedback"])
async def create_practice_card_feedback(
    feedback: PracticeCardFeedbackCreate,
    db: Session = Depends(get_db)
):
    """創建練習卡回饋 (API-204.3)"""
    feedback_repo = PracticeCardFeedbackRepository(db)
    new_feedback = feedback_repo.create(PracticeCardFeedback(
        session_id=feedback.session_id,
        practice_id=feedback.practice_id,
        rating=feedback.rating,
        feedback_text=feedback.feedback_text,
        is_favorite=feedback.is_favorite
    ))
    
    return {
        "status": "success",
        "feedback": {
            "id": new_feedback.id,
            "session_id": new_feedback.session_id,
            "practice_id": new_feedback.practice_id,
            "rating": new_feedback.rating,
            "feedback_text": new_feedback.feedback_text,
            "is_favorite": new_feedback.is_favorite,
            "created_at": new_feedback.created_at
        }
    }

@router.put("/practice-card-feedback/{feedback_id}/favorite", tags=["feedback"])
async def toggle_practice_card_favorite(
    feedback_id: int,
    is_favorite: bool = Body(...),
    db: Session = Depends(get_db)
):
    """切換練習卡最愛狀態 (API-204.5)"""
    feedback_repo = PracticeCardFeedbackRepository(db)
    updated_feedback = feedback_repo.update(feedback_id, is_favorite=is_favorite)
    
    if not updated_feedback:
        return {"status": "error", "message": "回饋不存在"}
    
    return {
        "status": "success",
        "feedback": {
            "id": updated_feedback.id,
            "is_favorite": updated_feedback.is_favorite
        }
    }

# 最愛清單管理端點 (API-206)
@router.get("/user/favorite-cards", tags=["user"])
async def get_user_favorite_cards(
    db: Session = Depends(get_db)
):
    """
    獲取用戶的所有最愛練習卡 (API-206.1)
    
    返回用戶標記為最愛的所有練習卡及其評分和備註
    """
    try:
        feedback_repo = PracticeCardFeedbackRepository(db)
        # 獲取所有標記為最愛的回饋
        favorite_feedbacks = db.query(PracticeCardFeedback).filter(
            PracticeCardFeedback.is_favorite == True
        ).all()
        
        # 獲取對應的練習卡
        favorite_cards = []
        for feedback in favorite_feedbacks:
            card = db.query(PracticeCard).filter(PracticeCard.id == feedback.practice_id).first()
            if card:
                favorite_cards.append({
                    "card": {
                        "id": card.id,
                        "name": card.name,
                        "goal": card.goal,
                        "tips": card.tips,
                        "pitfalls": card.pitfalls,
                        "dosage": card.dosage,
                        "level": card.level,
                        "terrain": card.terrain,
                        "self_check": card.self_check,
                        "card_type": card.card_type
                    },
                    "user_rating": feedback.rating,
                    "user_notes": feedback.feedback_text,
                    "favorited_at": feedback.created_at
                })
        
        return {
            "status": "success",
            "favorite_cards": favorite_cards,
            "count": len(favorite_cards)
        }
    except Exception as e:
        return {"status": "error", "message": f"獲取最愛練習卡時出錯: {str(e)}"}

@router.post("/user/favorite-cards/{practice_card_id}", tags=["user"])
async def toggle_favorite_card(
    practice_card_id: int,
    is_favorite: bool = Body(..., title="最愛狀態", description="True表示加入最愛，False表示取消最愛"),
    session_id: int = Body(..., title="會話ID", description="用戶會話ID"),
    db: Session = Depends(get_db)
):
    """
    更新練習卡的最愛狀態 (API-206.2)
    
    更新練習卡的最愛標記狀態
    """
    try:
        # 查找現有的回饋記錄
        feedback_repo = PracticeCardFeedbackRepository(db)
        existing_feedback = feedback_repo.get_by_session_and_practice(session_id, practice_card_id)
        
        if existing_feedback:
            # 更新現有回饋的最愛狀態
            updated_feedback = feedback_repo.update(existing_feedback.id, is_favorite=is_favorite)
        else:
            # 創建新的回饋記錄
            updated_feedback = feedback_repo.create(PracticeCardFeedback(
                session_id=session_id,
                practice_id=practice_card_id,
                rating=0,  # 默認評分
                is_favorite=is_favorite
            ))
        
        return {
            "status": "success",
            "message": f"練習卡已{'加入' if is_favorite else '移除'}最愛清單",
            "feedback": {
                "id": updated_feedback.id,
                "is_favorite": updated_feedback.is_favorite
            }
        }
    except Exception as e:
        return {"status": "error", "message": f"更新最愛狀態時出錯: {str(e)}"}

@router.delete("/user/favorite-cards/{practice_card_id}", tags=["user"])
async def remove_favorite_card(
    practice_card_id: int,
    session_id: int = Body(..., title="會話ID", description="用戶會話ID"),
    db: Session = Depends(get_db)
):
    """
    移除最愛標記 (API-206.3)
    
    取消練習卡的最愛標記
    """
    try:
        feedback_repo = PracticeCardFeedbackRepository(db)
        existing_feedback = feedback_repo.get_by_session_and_practice(session_id, practice_card_id)
        
        if existing_feedback:
            updated_feedback = feedback_repo.update(existing_feedback.id, is_favorite=False)
            return {
                "status": "success",
                "message": "練習卡已移除最愛清單",
                "feedback": {
                    "id": updated_feedback.id,
                    "is_favorite": updated_feedback.is_favorite
                }
            }
        else:
            return {"status": "success", "message": "練習卡不在最愛清單中"}
    except Exception as e:
        return {"status": "error", "message": f"移除最愛標記時出錯: {str(e)}"}

