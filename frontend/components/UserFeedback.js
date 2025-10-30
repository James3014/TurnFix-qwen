/**
 * 使用者回饋組件 (UI-307)
 * 
 * 設計並實作多層回饋介面
 */
import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import '../styles/UserFeedback.css';

const UserFeedback = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { session, recommendedCards } = location.state || {};
  
  const [activeTab, setActiveTab] = useState('session'); // 'session' or 'practice-card'
  const [sessionFeedback, setSessionFeedback] = useState({
    rating: '',
    feedback_text: '',
    feedback_type: 'immediate'
  });
  const [practiceCardFeedback, setPracticeCardFeedback] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  if (!session || !recommendedCards) {
    return (
      <div className="user-feedback">
        <div className="error-message">
          <h2>缺少必要資訊</h2>
          <button onClick={() => navigate(-1)}>返回上一頁</button>
        </div>
      </div>
    );
  }

  const handleSessionFeedbackChange = (field, value) => {
    setSessionFeedback(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handlePracticeCardFeedbackChange = (practiceId, field, value) => {
    setPracticeCardFeedback(prev => ({
      ...prev,
      [practiceId]: {
        ...prev[practiceId],
        [field]: value
      }
    }));
  };

  const submitSessionFeedback = async () => {
    if (!sessionFeedback.rating) {
      setError('請選擇評分');
      return;
    }
    
    setIsLoading(true);
    setError('');
    setSuccess('');
    
    try {
      const response = await fetch('/api/v1/session-feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: session.id,
          rating: sessionFeedback.rating,
          feedback_text: sessionFeedback.feedback_text,
          feedback_type: sessionFeedback.feedback_type
        })
      });
      
      if (response.ok) {
        setSuccess('會話回饋已提交成功！');
        // 重置表單
        setSessionFeedback({
          rating: '',
          feedback_text: '',
          feedback_type: 'immediate'
        });
      } else {
        throw new Error('提交會話回饋失敗');
      }
    } catch (err) {
      setError('提交會話回饋失敗，請稍後再試');
    } finally {
      setIsLoading(false);
    }
  };

  const submitPracticeCardFeedback = async (practiceId) => {
    const feedback = practiceCardFeedback[practiceId];
    if (!feedback || !feedback.rating) {
      setError('請選擇星數評分');
      return;
    }
    
    setIsLoading(true);
    setError('');
    setSuccess('');
    
    try {
      const response = await fetch('/api/v1/practice-card-feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: session.id,
          practice_id: practiceId,
          rating: feedback.rating,
          feedback_text: feedback.feedback_text,
          is_favorite: feedback.is_favorite || false
        })
      });
      
      if (response.ok) {
        setSuccess(`練習卡 ${practiceId} 回饋已提交成功！`);
        // 重置該練習卡的表單
        setPracticeCardFeedback(prev => {
          const newPrev = {...prev};
          delete newPrev[practiceId];
          return newPrev;
        });
      } else {
        throw new Error('提交練習卡回饋失敗');
      }
    } catch (err) {
      setError('提交練習卡回饋失敗，請稍後再試');
    } finally {
      setIsLoading(false);
    }
  };

  const toggleFavorite = async (practiceId) => {
    const feedback = practiceCardFeedback[practiceId];
    const isFavorite = !(feedback && feedback.is_favorite);
    
    setPracticeCardFeedback(prev => ({
      ...prev,
      [practiceId]: {
        ...prev[practiceId],
        is_favorite: isFavorite
      }
    }));
    
    // 這裡應該調用API更新最愛狀態
    try {
      // 模擬API調用
      await new Promise(resolve => setTimeout(resolve, 500));
      setSuccess(isFavorite ? '已加入最愛清單' : '已從最愛清單移除');
    } catch (err) {
      setError('更新最愛狀態失敗');
      // 回滾狀態
      setPracticeCardFeedback(prev => ({
        ...prev,
        [practiceId]: {
          ...prev[practiceId],
          is_favorite: !isFavorite
        }
      }));
    }
  };

  const renderSessionFeedbackTab = () => (
    <div className="feedback-tab session-feedback-tab">
      <h2>回饋層一：Session 層級 - 整個問題推薦流程的效果評價 (API-204.1)</h2>
      <p>這些推薦的練習卡是否幫助改善了我的問題？</p>
      
      <div className="rating-options">
        <div className="rating-option">
          <input
            type="radio"
            id="not_applicable"
            name="session_rating"
            value="not_applicable"
            checked={sessionFeedback.rating === "not_applicable"}
            onChange={(e) => handleSessionFeedbackChange('rating', e.target.value)}
          />
          <label htmlFor="not_applicable" className="rating-label not-applicable">
            ❌ 不適用
          </label>
        </div>
        
        <div className="rating-option">
          <input
            type="radio"
            id="partially_applicable"
            name="session_rating"
            value="partially_applicable"
            checked={sessionFeedback.rating === "partially_applicable"}
            onChange={(e) => handleSessionFeedbackChange('rating', e.target.value)}
          />
          <label htmlFor="partially_applicable" className="rating-label partially-applicable">
            △ 部分適用
          </label>
        </div>
        
        <div className="rating-option">
          <input
            type="radio"
            id="applicable"
            name="session_rating"
            value="applicable"
            checked={sessionFeedback.rating === "applicable"}
            onChange={(e) => handleSessionFeedbackChange('rating', e.target.value)}
          />
          <label htmlFor="applicable" className="rating-label applicable">
            ✓ 適用
          </label>
        </div>
      </div>
      
      <div className="feedback-form">
        <label htmlFor="session-feedback-text">自由文字回饋（可選）：</label>
        <textarea
          id="session-feedback-text"
          value={sessionFeedback.feedback_text}
          onChange={(e) => handleSessionFeedbackChange('feedback_text', e.target.value)}
          placeholder="請告訴我們這些推薦的練習卡哪些部分有幫助，哪些可以改進..."
          rows={4}
        />
      </div>
      
      <div className="feedback-actions">
        <button 
          className="submit-button"
          onClick={submitSessionFeedback}
          disabled={isLoading}
        >
          {isLoading ? '提交中...' : '提交會話回饋'}
        </button>
      </div>
    </div>
  );

  const renderPracticeCardFeedbackTab = () => (
    <div className="feedback-tab practice-card-feedback-tab">
      <h2>回饋層二：PracticeCard 層級 - 單個練習卡的品質評價 (API-204.3)</h2>
      <p>這些練習卡本身對我的實用程度如何？</p>
      
      <div className="practice-cards-feedback">
        {recommendedCards.map((card) => (
          <div key={card.id} className="practice-card-feedback">
            <div className="card-header">
              <h3>{card.name}</h3>
              <button 
                className={`favorite-button ${practiceCardFeedback[card.id]?.is_favorite ? 'favorited' : ''}`}
                onClick={() => toggleFavorite(card.id)}
                aria-label={practiceCardFeedback[card.id]?.is_favorite ? "移除最愛" : "加入最愛"}
              >
                {practiceCardFeedback[card.id]?.is_favorite ? '❤️' : '🤍'}
              </button>
            </div>
            
            <div className="star-rating">
              <p>星數評分：</p>
              <div className="stars">
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    className={`star ${practiceCardFeedback[card.id]?.rating >= star ? 'filled' : ''}`}
                    onClick={() => handlePracticeCardFeedbackChange(card.id, 'rating', star)}
                    aria-label={`${star} 顆星`}
                  >
                    {practiceCardFeedback[card.id]?.rating >= star ? '★' : '☆'}
                  </button>
                ))}
              </div>
              
              {practiceCardFeedback[card.id]?.rating && (
                <p className="rating-description">
                  {practiceCardFeedback[card.id].rating === 1 && "不適用 - 練習卡與我的症狀無關或不適合我"}
                  {practiceCardFeedback[card.id].rating === 2 && "較不適用 - 有些內容有用，但大部分不適用"}
                  {practiceCardFeedback[card.id].rating === 3 && "部分適用 - 有幫助但需要調整或補充"}
                  {practiceCardFeedback[card.id].rating === 4 && "適用 - 相當有幫助"}
                  {practiceCardFeedback[card.id].rating === 5 && "非常適用 - 完全符合我的需求"}
                </p>
              )}
            </div>
            
            <div className="feedback-form">
              <label htmlFor={`feedback-text-${card.id}`}>自由文字回饋（可選）：</label>
              <textarea
                id={`feedback-text-${card.id}`}
                value={practiceCardFeedback[card.id]?.feedback_text || ''}
                onChange={(e) => handlePracticeCardFeedbackChange(card.id, 'feedback_text', e.target.value)}
                placeholder="請告訴我們這張練習卡哪些部分有幫助，哪些可以改進..."
                rows={3}
              />
            </div>
            
            <button 
              className="submit-button"
              onClick={() => submitPracticeCardFeedback(card.id)}
              disabled={isLoading}
            >
              {isLoading ? '提交中...' : '提交練習卡回饋'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="user-feedback">
      <div className="page-header">
        <h1>📝 提供回饋</h1>
        <p>您的意見將幫助我們改善系統</p>
      </div>
      
      <div className="feedback-tabs">
        <button 
          className={`tab-button ${activeTab === 'session' ? 'active' : ''}`}
          onClick={() => setActiveTab('session')}
        >
          會話回饋
        </button>
        <button 
          className={`tab-button ${activeTab === 'practice-card' ? 'active' : ''}`}
          onClick={() => setActiveTab('practice-card')}
        >
          練習卡回饋
        </button>
      </div>
      
      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}
      
      {activeTab === 'session' ? renderSessionFeedbackTab() : renderPracticeCardFeedbackTab()}
      
      <div className="feedback-navigation">
        <button 
          className="back-button"
          onClick={() => navigate(-1)}
        >
          ← 返回上一頁
        </button>
        <button 
          className="continue-button"
          onClick={() => navigate('/')}
        >
          繼續使用系統 →
        </button>
      </div>
    </div>
  );
};

export default UserFeedback;