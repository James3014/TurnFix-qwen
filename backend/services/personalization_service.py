"""
個人化推薦演化服務

根據用戶評分歷史，識別用戶偏好的卡片類型，並提供個性化推薦
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from ..models.practice_card import PracticeCard
from ..models.practice_card_feedback import PracticeCardFeedback
from ..database.repositories import PracticeCardFeedbackRepository
from collections import Counter


def get_user_preference_analysis(db: Session, user_session_id: int) -> Dict[str, Any]:
    """
    分析用戶偏好，識別用戶偏好的卡片類型
    
    Args:
        db: 資料庫連接
        user_session_id: 用戶會話ID
    
    Returns:
        包含用戶偏好分析結果的字典
    """
    feedback_repo = PracticeCardFeedbackRepository(db)
    
    # 獲取用戶的所有評分記錄
    user_feedbacks = db.query(PracticeCardFeedback).filter(
        PracticeCardFeedback.session_id == user_session_id
    ).all()
    
    if not user_feedbacks:
        return {
            "message": "用戶評分記錄不足，無法進行偏好分析",
            "top_categories": [],
            "similar_cards": []
        }
    
    # 統計評分和卡片類型
    high_rated_cards = []
    categories = []
    
    for feedback in user_feedbacks:
        if feedback.rating >= 4:  # 高評分卡片 (4-5星)
            high_rated_cards.append(feedback.practice_id)
            card = db.query(PracticeCard).filter(PracticeCard.id == feedback.practice_id).first()
            if card and card.card_type:
                categories.append(card.card_type.lower())
    
    # 找出最常見的卡片類型
    category_counts = Counter(categories)
    top_categories = [cat for cat, _ in category_counts.most_common(3)]
    
    # 根據偏好類型推薦類似卡片
    similar_cards = []
    if top_categories:
        similar_cards = db.query(PracticeCard).filter(
            PracticeCard.card_type.in_(top_categories),
            PracticeCard.id.notin_(high_rated_cards)  # 排除已評分的卡片
        ).limit(5).all()
    
    return {
        "top_categories": top_categories,
        "similar_cards": [
            {
                "id": card.id,
                "name": card.name,
                "goal": card.goal,
                "card_type": card.card_type,
                "tips": card.tips if card.tips else [],
                "pitfalls": card.pitfalls if card.pitfalls else "",
                "dosage": card.dosage if card.dosage else "",
                "self_check": card.self_check if card.self_check else [],
                "level": card.level if card.level else [],
                "terrain": card.terrain if card.terrain else []
            }
            for card in similar_cards
        ],
        "message": f"根據您的評分歷史，您可能也喜歡「{', '.join(top_categories[:2])}」類型的練習卡"
    }


def get_personalized_recommendations(db: Session, user_session_id: int, current_practice_id: int) -> Dict[str, Any]:
    """
    為當前練習卡提供個性化推薦
    
    Args:
        db: 資料庫連接
        user_session_id: 用戶會話ID
        current_practice_id: 當前練習卡ID
    
    Returns:
        包含個性化推薦的字典
    """
    # 獲取當前卡片信息
    current_card = db.query(PracticeCard).filter(PracticeCard.id == current_practice_id).first()
    if not current_card:
        return {"recommendations": []}
    
    # 獲取用戶偏好分析
    preference_analysis = get_user_preference_analysis(db, user_session_id)
    
    # 獲取用戶高評分卡片
    user_feedbacks = db.query(PracticeCardFeedback).filter(
        PracticeCardFeedback.session_id == user_session_id,
        PracticeCardFeedback.rating >= 4
    ).all()
    
    high_rated_card_ids = [fb.practice_id for fb in user_feedbacks]
    
    # 根據當前卡片類型和其他偏好找到類似卡片
    similar_cards = db.query(PracticeCard).filter(
        PracticeCard.card_type == current_card.card_type,
        PracticeCard.id != current_practice_id,
        PracticeCard.id.notin_(high_rated_card_ids)  # 排除已高評分的卡片
    ).limit(3).all()
    
    # 同時根據用戶偏好類型找卡片
    recommended_by_preference = []
    if preference_analysis["top_categories"]:
        recommended_by_preference = db.query(PracticeCard).filter(
            PracticeCard.card_type.in_(preference_analysis["top_categories"]),
            PracticeCard.id != current_practice_id,
            PracticeCard.id.notin_([card.id for card in similar_cards]),
            PracticeCard.id.notin_(high_rated_card_ids)  # 排除已高評分的卡片
        ).limit(2).all()
    
    # 合併推薦結果
    all_recommendations = similar_cards + recommended_by_preference
    
    return {
        "message": f"根據您之前的評分，您可能也會喜歡「{current_card.card_type}」相關的練習卡",
        "recommendations": [
            {
                "id": card.id,
                "name": card.name,
                "goal": card.goal,
                "card_type": card.card_type,
                "similar_to_previous": card.card_type == current_card.card_type,
                "based_on_preference": card.card_type in preference_analysis["top_categories"]
            }
            for card in all_recommendations
        ]
    }