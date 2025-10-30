/**
 * 反饋頁面組件
 */
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../styles/FeedbackPage.css';
import api from '../api/api';

const FeedbackPage = () => {
  const [sessionFeedback, setSessionFeedback] = useState({
    rating: '',
    feedback_text: ''
  });
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleSessionFeedbackChange = (e) => {
    const { name, value } = e.target;
    setSessionFeedback(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      // 提交反饋到後端
      await api.submitFeedback(sessionFeedback);
      setIsSubmitted(true);
    } catch (error) {
      console.error('提交反饋失敗:', error);
      alert('提交失敗，請稍後再試');
    }
  };

  if (isSubmitted) {
    return (
      <div className="feedback-confirmation">
        <h2>感謝您的反饋！</h2>
        <p>您的意見將幫助我們改善系統。</p>
        <Link to="/" className="btn primary">返回首頁</Link>
      </div>
    );
  }

  return (
    <div className="feedback-page">
      <h2>提供反饋</h2>
      
      <form onSubmit={handleSubmit} className="feedback-form">
        <div className="feedback-section">
          <h3>整體建議評價</h3>
          <p>這些練習卡對您有幫助嗎？</p>
          
          <div className="rating-options">
            <label className="rating-option">
              <input
                type="radio"
                name="rating"
                value="not_applicable"
                checked={sessionFeedback.rating === "not_applicable"}
                onChange={handleSessionFeedbackChange}
              />
              <span className="rating-label">❌ 不適用</span>
            </label>
            
            <label className="rating-option">
              <input
                type="radio"
                name="rating"
                value="partially_applicable"
                checked={sessionFeedback.rating === "partially_applicable"}
                onChange={handleSessionFeedbackChange}
              />
              <span className="rating-label">△ 部分適用</span>
            </label>
            
            <label className="rating-option">
              <input
                type="radio"
                name="rating"
                value="applicable"
                checked={sessionFeedback.rating === "applicable"}
                onChange={handleSessionFeedbackChange}
              />
              <span className="rating-label">✓ 適用</span>
            </label>
          </div>
        </div>
        
        <div className="feedback-section">
          <h3>詳細反饋</h3>
          <textarea
            name="feedback_text"
            value={sessionFeedback.feedback_text}
            onChange={handleSessionFeedbackChange}
            placeholder="請告訴我們這些練習卡哪些部分有幫助，哪些可以改進..."
            rows={5}
          />
        </div>
        
        <div className="feedback-actions">
          <Link to="/" className="btn secondary">返回首頁</Link>
          <button type="submit" className="btn primary">提交反饋</button>
        </div>
      </form>
    </div>
  );
};

export default FeedbackPage;