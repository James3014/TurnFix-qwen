/**
 * 練習卡詳細頁面 (UI-304)
 * 
 * 設計並實作練習卡詳細頁面
 */
import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import PersonalizedRecommendations from './PersonalizedRecommendations';
import VideoDemo from './VideoDemo';
import VoiceReading from './VoiceReading';
import '../styles/PracticeCardDetail.css';

const PracticeCardDetail = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { card } = location.state || {};
  
  const [checkedItems, setCheckedItems] = useState({});
  const [isFavorite, setIsFavorite] = useState(false);
  const [starRating, setStarRating] = useState(0);
  const [feedbackText, setFeedbackText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [feedbackSubmitted, setFeedbackSubmitted] = useState(false);

  if (!card) {
    return (
      <div className="practice-card-detail">
        <div className="error-message">
          <h2>練習卡不存在</h2>
          <button 
            className="back-button"
            onClick={() => navigate(-1)}
          >
            返回上一頁
          </button>
        </div>
      </div>
    );
  }

  const toggleCheckItem = (itemKey) => {
    setCheckedItems(prev => ({
      ...prev,
      [itemKey]: !prev[itemKey]
    }));
  };

  const toggleFavorite = async () => {
    setIsLoading(true);
    try {
      // 這裡應該發送API請求更新最愛狀態
      // 模擬API調用
      await new Promise(resolve => setTimeout(resolve, 500));
      setIsFavorite(!isFavorite);
    } catch (error) {
      console.error('更新最愛狀態失敗:', error);
      alert('更新最愛狀態失敗，請稍後再試');
    } finally {
      setIsLoading(false);
    }
  };

  const handleStarRating = (rating) => {
    setStarRating(rating);
  };

  const submitFeedback = async () => {
    if (starRating === 0) {
      alert('請先選擇星數評分');
      return;
    }
    
    setIsLoading(true);
    setFeedbackSubmitted(false);
    
    try {
      // 這裡應該發送API請求提交回饋
      // 模擬API調用
      await new Promise(resolve => setTimeout(resolve, 1000));
      setFeedbackSubmitted(true);
      alert('感謝您的回饋！');
    } catch (error) {
      console.error('提交回饋失敗:', error);
      alert('提交回饋失敗，請稍後再試');
    } finally {
      setIsLoading(false);
    }
  };

  const renderTips = () => {
    if (!card.tips || card.tips.length === 0) return null;
    
    return (
      <div className="detail-section">
        <h2>練習要點</h2>
        <ul className="checklist">
          {card.tips.map((tip, index) => (
            <li key={index} className="checklist-item">
              <label className="checklist-label">
                <input
                  type="checkbox"
                  checked={!!checkedItems[`tip-${index}`]}
                  onChange={() => toggleCheckItem(`tip-${index}`)}
                />
                <span className="checkmark"></span>
                {tip}
              </label>
            </li>
          ))}
        </ul>
      </div>
    );
  };

  const renderSelfCheck = () => {
    if (!card.self_check || card.self_check.length === 0) return null;
    
    return (
      <div className="detail-section">
        <h2>自我檢查點</h2>
        <ul className="checklist orange">
          {card.self_check.map((check, index) => (
            <li key={index} className="checklist-item">
              <label className="checklist-label">
                <input
                  type="checkbox"
                  checked={!!checkedItems[`self-check-${index}`]}
                  onChange={() => toggleCheckItem(`self-check-${index}`)}
                />
                <span className="checkmark orange"></span>
                {check}
              </label>
            </li>
          ))}
        </ul>
      </div>
    );
  };

  return (
    <div className="practice-card-detail">
      <div className="card-header">
        <button 
          className="back-button"
          onClick={() => navigate(-1)}
        >
          ← 返回
        </button>
        <div className="card-title-section">
          <h1>{card.name}</h1>
          <span className="card-type">{card.card_type}</span>
        </div>
        <button 
          className={`favorite-button ${isFavorite ? 'favorited' : ''}`}
          onClick={toggleFavorite}
          aria-label={isFavorite ? "移除最愛" : "加入最愛"}
          disabled={isLoading}
        >
          {isLoading ? '🔄' : (isFavorite ? '❤️' : '🤍')}
        </button>
      </div>
      
      <div className="card-content">
        <div className="detail-section">
          <h2>練習目標</h2>
          <p>{card.goal}</p>
        </div>
        
        {renderTips()}
        
        <div className="detail-section">
          <h2>常見錯誤</h2>
          <p>{card.pitfalls}</p>
        </div>
        
        <div className="detail-section">
          <h2>建議次數</h2>
          <p>{card.dosage}</p>
        </div>
        
        {renderSelfCheck()}
        
        {/* 語音朗讀功能 - UXP-1816 */}
        <div className="voice-reading-section">
          <VoiceReading 
            text={`練習卡名稱：${card.name}。練習目標：${card.goal}。${card.tips && card.tips.length > 0 ? `練習要點：${card.tips.join('，')}。` : ''}${card.pitfalls ? `常見錯誤：${card.pitfalls}。` : ''}${card.dosage ? `建議次數：${card.dosage}。` : ''}${card.self_check && card.self_check.length > 0 ? `自我檢查點：${card.self_check.join('，')}。` : ''}`} 
            language="zh-TW" 
          />
        </div>
      </div>
      
      <div className="feedback-section">
        <h2>評價這張練習卡 (API-204.3)</h2>
        
        <div className="star-rating">
          <p>星數評分：</p>
          <div className="stars">
            {[1, 2, 3, 4, 5].map(star => (
              <button
                key={star}
                className={`star ${star <= starRating ? 'filled' : ''}`}
                onClick={() => handleStarRating(star)}
                aria-label={`${star} 顆星`}
                disabled={isLoading}
              >
                {star <= starRating ? '★' : '☆'}
              </button>
            ))}
          </div>
          {starRating > 0 && (
            <p className="rating-description">
              {starRating === 1 && "不適用 - 練習卡與我的症狀無關或不適合我"}
              {starRating === 2 && "較不適用 - 有些內容有用，但大部分不適用"}
              {starRating === 3 && "部分適用 - 有幫助但需要調整或補充"}
              {starRating === 4 && "適用 - 相當有幫助"}
              {starRating === 5 && "非常適用 - 完全符合我的需求"}
            </p>
          )}
        </div>
        
        <div className="feedback-form">
          <label htmlFor="feedback-text">自由文字回饋（可選）：</label>
          <textarea
            id="feedback-text"
            value={feedbackText}
            onChange={(e) => setFeedbackText(e.target.value)}
            placeholder="請告訴我們這張練習卡哪些部分有幫助，哪些可以改進..."
            rows={4}
            disabled={isLoading}
          />
        </div>
        
        <button 
          className="submit-feedback"
          onClick={submitFeedback}
          disabled={isLoading || feedbackSubmitted}
        >
          {isLoading ? '提交中...' : (feedbackSubmitted ? '已提交' : '提交回饋')}
        </button>
        
        {feedbackSubmitted && (
          <div className="feedback-success">
            <p>✅ 感謝您的回饋！</p>
          </div>
        )}
      </div>
      
      {/* 個人化推薦組件 - UXP-1814 */}
      <div className="personalized-recommendations-section">
        <PersonalizedRecommendations 
          practiceId={card.id} 
          sessionId={123} // 在實際應用中應從上下文獲取
        />
      </div>
    </div>
  );
};

export default PracticeCardDetail;