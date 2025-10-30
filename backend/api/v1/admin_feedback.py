"""
管理者回饋分析 API 端點 (API-207)

提供管理者回饋分析接口
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from ...database.base import get_db
from ...database.repositories import (
    SessionFeedbackRepository,
    PracticeCardFeedbackRepository,
    SymptomRepository
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin/feedback-analytics", tags=["admin", "feedback"])

@router.get("/summary")
def get_feedback_analytics_summary(db: Session = Depends(get_db)):
    """
    獲取回饋分析摘要 (API-207.1)
    
    返回回饋分析的摘要數據
    """
    try:
        session_feedback_repo = SessionFeedbackRepository(db)
        practice_card_feedback_repo = PracticeCardFeedbackRepository(db)
        
        # 獲取會話回饋分布
        all_session_feedback = session_feedback_repo.get_all()
        session_feedback_distribution = {"not_applicable": 0, "partially_applicable": 0, "applicable": 0}
        feedback_type_distribution = {"immediate": 0, "delayed": 0}
        
        for feedback in all_session_feedback:
            if feedback.rating in session_feedback_distribution:
                session_feedback_distribution[feedback.rating] += 1
            if feedback.feedback_type in feedback_type_distribution:
                feedback_type_distribution[feedback.feedback_type] += 1
                
        total_sessions = len(all_session_feedback)
        total_feedback = len(all_session_feedback)
        feedback_completion_rate = 1.0 if total_sessions > 0 else 0.0
        
        # 獲取練習卡回饋星數分布
        all_practice_feedback = practice_card_feedback_repo.get_all()
        rating_distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        favorite_count = 0
        
        for feedback in all_practice_feedback:
            if feedback.rating in rating_distribution:
                rating_distribution[feedback.rating] += 1
            if feedback.is_favorite:
                favorite_count += 1
                
        total_practice_count = len(all_practice_feedback)
        average_rating = sum(f.rating for f in all_practice_feedback) / total_practice_count if total_practice_count > 0 else 0
        favorite_rate = favorite_count / total_practice_count if total_practice_count > 0 else 0
        
        return {
            "status": "success",
            "session_feedback_distribution": session_feedback_distribution,
            "immediate_vs_delayed": feedback_type_distribution,
            "feedback_completion_rate": feedback_completion_rate,
            "total_feedback_count": total_feedback,
            "rating_distribution": rating_distribution,
            "average_rating": average_rating,
            "rating_count": total_practice_count,
            "favorite_count": favorite_count,
            "favorite_rate": favorite_rate
        }
    except Exception as e:
        logger.error(f"獲取回饋分析摘要時出錯: {e}")
        raise HTTPException(status_code=500, detail=f"獲取回饋分析摘要時出錯: {str(e)}")

@router.get("/practice-cards/{practice_card_id}")
def get_practice_card_feedback_analysis(practice_card_id: int, db: Session = Depends(get_db)):
    """
    獲取特定練習卡的回饋分析 (API-207.2)
    
    返回特定練習卡的回饋分析數據
    """
    try:
        practice_card_feedback_repo = PracticeCardFeedbackRepository(db)
        
        # 獲取練習卡信息
        card_info = practice_card_feedback_repo.get_practice_card_info(practice_card_id)
        
        # 獲取星數分布
        rating_distribution = practice_card_feedback_repo.get_rating_distribution_by_practice(practice_card_id)
        
        # 獲取平均評分
        average_rating = practice_card_feedback_repo.get_average_rating_by_practice(practice_card_id)
        
        # 獲取評分數量
        rating_count = practice_card_feedback_repo.get_rating_count_by_practice(practice_card_id)
        
        # 獲取最愛數量
        favorite_count = practice_card_feedback_repo.get_favorite_count_by_practice(practice_card_id)
        
        # 獲取最愛率
        total_ratings = practice_card_feedback_repo.get_rating_count_by_practice(practice_card_id)
        favorite_rate = (favorite_count / total_ratings) if total_ratings > 0 else 0
        
        return {
            "status": "success",
            "card_info": card_info,
            "rating_distribution": rating_distribution,
            "average_rating": average_rating,
            "rating_count": rating_count,
            "favorite_count": favorite_count,
            "favorite_rate": favorite_rate
        }
    except Exception as e:
        logger.error(f"獲取練習卡回饋分析時出錯: {e}")
        raise HTTPException(status_code=500, detail=f"獲取練習卡回饋分析時出錯: {str(e)}")

@router.get("/symptoms/{symptom_id}")
def get_symptom_feedback_analysis(symptom_id: int, db: Session = Depends(get_db)):
    """
    獲取特定症狀的回饋分析 (API-207.3)
    
    返回特定症狀的回饋分析數據
    """
    try:
        session_feedback_repo = SessionFeedbackRepository(db)
        
        # 獲取症狀信息
        symptom_info = session_feedback_repo.get_symptom_info(symptom_id)
        
        # 獲取會話回饋分布
        session_feedback_distribution = session_feedback_repo.get_rating_distribution_by_symptom(symptom_id)
        
        # 獲取相關練習卡分析
        related_cards_analysis = session_feedback_repo.get_related_cards_analysis_by_symptom(symptom_id)
        
        # 獲取高表現和低表現練習卡
        high_performers = session_feedback_repo.get_high_performers_by_symptom(symptom_id)
        low_performers = session_feedback_repo.get_low_performers_by_symptom(symptom_id)
        
        return {
            "status": "success",
            "symptom_info": symptom_info,
            "session_feedback_distribution": session_feedback_distribution,
            "related_cards_analysis": related_cards_analysis,
            "high_performers": high_performers,
            "low_performers": low_performers
        }
    except Exception as e:
        logger.error(f"獲取症狀回饋分析時出錯: {e}")
        raise HTTPException(status_code=500, detail=f"獲取症狀回饋分析時出錯: {str(e)}")

@router.get("/user-preferences")
def get_user_preference_analysis(db: Session = Depends(get_db)):
    """
    獲取用戶偏好分析 (API-207.4)
    
    返回用戶偏好分析數據
    """
    try:
        practice_card_feedback_repo = PracticeCardFeedbackRepository(db)
        
        # 獲取最高評分練習卡
        top_rated_cards = practice_card_feedback_repo.get_top_rated_cards()
        
        # 獲取最常被加入最愛的卡片
        most_favorited_cards = practice_card_feedback_repo.get_most_favorited_cards()
        
        # 獲取用戶段落分析
        user_segment_analysis = practice_card_feedback_repo.get_user_segment_analysis()
        
        return {
            "status": "success",
            "top_rated_cards": top_rated_cards,
            "most_favorited_cards": most_favorited_cards,
            "user_segment_analysis": user_segment_analysis
        }
    except Exception as e:
        logger.error(f"獲取用戶偏好分析時出錯: {e}")
        raise HTTPException(status_code=500, detail=f"獲取用戶偏好分析時出錯: {str(e)}")