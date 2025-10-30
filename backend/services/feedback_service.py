"""
使用者回饋服務 (API-204)

實現兩層回饋機制的業務邏輯：
1. Session 層級 - 整個問題推薦流程的效果評價
2. PracticeCard 層級 - 單個練習卡的品質評價
"""
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from ..database.repositories import (
    SessionFeedbackRepository,
    PracticeCardFeedbackRepository
)
from ..models.session_feedback import SessionFeedback
from ..models.practice_card_feedback import PracticeCardFeedback
import logging

logger = logging.getLogger(__name__)

def create_session_feedback(
    db: Session,
    session_id: int,
    rating: str,
    feedback_text: Optional[str] = None,
    feedback_type: str = "immediate"
) -> SessionFeedback:
    """
    創建會話回饋 (API-204.1)
    
    記錄對整個推薦流程的評分 (`SessionFeedback`)
    
    Args:
        db: 資料庫會話
        session_id: 會話ID
        rating: 評分 ("not_applicable" | "partially_applicable" | "applicable")
        feedback_text: 自由文字回饋（可選）
        feedback_type: 回饋類型 ("immediate" | "delayed")
        
    Returns:
        SessionFeedback: 創建的會話回饋記錄
    """
    try:
        feedback_repo = SessionFeedbackRepository(db)
        
        # 創建會話回饋記錄
        feedback = SessionFeedback(
            session_id=session_id,
            rating=rating,
            feedback_text=feedback_text,
            feedback_type=feedback_type
        )
        
        created_feedback = feedback_repo.create(feedback)
        logger.info(f"成功創建會話回饋: session_id={session_id}, rating={rating}")
        
        return created_feedback
        
    except Exception as e:
        logger.error(f"創建會話回饋時出錯: {e}")
        raise

def create_practice_card_feedback(
    db: Session,
    session_id: int,
    practice_id: int,
    rating: int,
    feedback_text: Optional[str] = None,
    is_favorite: bool = False
) -> PracticeCardFeedback:
    """
    創建練習卡回饋 (API-204.3)
    
    記錄對單個練習卡的星數評分 (`PracticeCardFeedback`)
    
    Args:
        db: 資料庫會話
        session_id: 會話ID
        practice_id: 練習卡ID
        rating: 星數評分 (1-5 顆星)
        feedback_text: 自由文字回饋（可選）
        is_favorite: 是否加入最愛清單（預設 false），可獨立於星數設定
        
    Returns:
        PracticeCardFeedback: 創建的練習卡回饋記錄
    """
    try:
        feedback_repo = PracticeCardFeedbackRepository(db)
        
        # 創建練習卡回饋記錄
        feedback = PracticeCardFeedback(
            session_id=session_id,
            practice_id=practice_id,
            rating=rating,
            feedback_text=feedback_text,
            is_favorite=is_favorite
        )
        
        created_feedback = feedback_repo.create(feedback)
        logger.info(f"成功創建練習卡回饋: session_id={session_id}, practice_id={practice_id}, rating={rating}")
        
        return created_feedback
        
    except Exception as e:
        logger.error(f"創建練習卡回饋時出錯: {e}")
        raise

def toggle_practice_card_favorite(
    db: Session,
    feedback_id: int,
    is_favorite: bool
) -> PracticeCardFeedback:
    """
    切換練習卡最愛狀態 (API-204.5)
    
    更新練習卡最愛標記狀態
    
    Args:
        db: 資料庫會話
        feedback_id: 回饋ID
        is_favorite: 最愛狀態
        
    Returns:
        PracticeCardFeedback: 更新的練習卡回饋記錄
    """
    try:
        feedback_repo = PracticeCardFeedbackRepository(db)
        
        # 更新最愛狀態
        updated_feedback = feedback_repo.update(feedback_id, is_favorite=is_favorite)
        logger.info(f"成功更新練習卡最愛狀態: feedback_id={feedback_id}, is_favorite={is_favorite}")
        
        return updated_feedback
        
    except Exception as e:
        logger.error(f"更新練習卡最愛狀態時出錯: {e}")
        raise

def get_session_feedback_stats(db: Session) -> Dict[str, any]:
    """
    獲取會話回饋統計 (API-207.1 部分)
    
    提供會話層級回饋的統計資訊
    
    Returns:
        Dict: 會話回饋統計
    """
    try:
        feedback_repo = SessionFeedbackRepository(db)
        all_feedback = feedback_repo.get_all()
        
        # 計算評分分布
        rating_distribution = {"not_applicable": 0, "partially_applicable": 0, "applicable": 0}
        feedback_type_distribution = {"immediate": 0, "delayed": 0}
        
        for feedback in all_feedback:
            if feedback.rating in rating_distribution:
                rating_distribution[feedback.rating] += 1
            if feedback.feedback_type in feedback_type_distribution:
                feedback_type_distribution[feedback.feedback_type] += 1
                
        total_count = len(all_feedback)
        feedback_completion_rate = 1.0 if total_count > 0 else 0.0
        
        return {
            "session_feedback_distribution": rating_distribution,
            "immediate_vs_delayed": feedback_type_distribution,
            "feedback_completion_rate": feedback_completion_rate,
            "total_feedback_count": total_count
        }
        
    except Exception as e:
        logger.error(f"獲取會話回饋統計時出錯: {e}")
        return {
            "session_feedback_distribution": {"not_applicable": 0, "partially_applicable": 0, "applicable": 0},
            "immediate_vs_delayed": {"immediate": 0, "delayed": 0},
            "feedback_completion_rate": 0.0,
            "total_feedback_count": 0
        }

def get_practice_card_feedback_stats(db: Session, practice_id: int) -> Dict[str, any]:
    """
    獲取練習卡回饋統計 (API-207.2 部分)
    
    提供練習卡層級回饋的統計資訊
    
    Args:
        db: 資料庫會話
        practice_id: 練習卡ID
        
    Returns:
        Dict: 練習卡回饋統計
    """
    try:
        feedback_repo = PracticeCardFeedbackRepository(db)
        all_feedback = feedback_repo.get_by_practice_card(practice_id)
        
        # 計算星數分布
        rating_distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        favorite_count = 0
        
        for feedback in all_feedback:
            if feedback.rating in rating_distribution:
                rating_distribution[feedback.rating] += 1
            if feedback.is_favorite:
                favorite_count += 1
                
        total_count = len(all_feedback)
        average_rating = sum(f.rating for f in all_feedback) / total_count if total_count > 0 else 0
        favorite_rate = favorite_count / total_count if total_count > 0 else 0
        
        return {
            "rating_distribution": rating_distribution,
            "average_rating": round(average_rating, 2),
            "rating_count": total_count,
            "favorite_count": favorite_count,
            "favorite_rate": round(favorite_rate, 2)
        }
        
    except Exception as e:
        logger.error(f"獲取練習卡回饋統計時出錯: {e}")
        return {
            "rating_distribution": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
            "average_rating": 0.0,
            "rating_count": 0,
            "favorite_count": 0,
            "favorite_rate": 0.0
        }