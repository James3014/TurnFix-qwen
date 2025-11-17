/**
 * PracticeCardFeedbackForm 組件
 *
 * 單個練習卡的回饋表單
 * 遵循 Linus 原則:簡單、清晰、單一職責
 */
import React, { useState } from 'react';
import { feedbackAPI, favoritesAPI } from '../../api/client';

const PracticeCardFeedbackItem = ({ card, sessionId }) => {
  const [formData, setFormData] = useState({
    rating: 0,
    feedback_text: '',
    is_favorite: false
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleRatingChange = (rating) => {
    setFormData(prev => ({ ...prev, rating }));
  };

  const handleTextChange = (text) => {
    setFormData(prev => ({ ...prev, feedback_text: text }));
  };

  const toggleFavorite = async () => {
    const newFavoriteState = !formData.is_favorite;
    setFormData(prev => ({ ...prev, is_favorite: newFavoriteState }));

    try {
      await favoritesAPI.toggle(card.id);
      setSuccess(newFavoriteState ? '已加入最愛清單' : '已從最愛清單移除');
      setTimeout(() => setSuccess(''), 2000);
    } catch (err) {
      setError('更新最愛狀態失敗');
      // 回滾狀態
      setFormData(prev => ({ ...prev, is_favorite: !newFavoriteState }));
      setTimeout(() => setError(''), 3000);
    }
  };

  const handleSubmit = async () => {
    if (!formData.rating) {
      setError('請選擇星數評分');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      await feedbackAPI.submitPracticeCardFeedback({
        session_id: sessionId,
        practice_id: card.id,
        ...formData
      });
      setSuccess(`練習卡「${card.name}」回饋已提交成功!`);
      // 重置表單(保留最愛狀態)
      setFormData(prev => ({
        rating: 0,
        feedback_text: '',
        is_favorite: prev.is_favorite
      }));
    } catch (err) {
      setError(err.message || '提交練習卡回饋失敗,請稍後再試');
    } finally {
      setLoading(false);
    }
  };

  const getRatingDescription = (rating) => {
    const descriptions = {
      1: '不適用 - 練習卡與我的症狀無關或不適合我',
      2: '較不適用 - 有些內容有用,但大部分不適用',
      3: '部分適用 - 有幫助但需要調整或補充',
      4: '適用 - 相當有幫助',
      5: '非常適用 - 完全符合我的需求'
    };
    return descriptions[rating] || '';
  };

  return (
    <div className="practice-card-feedback">
      <div className="card-header">
        <h3>{card.name}</h3>
        <button
          className={`favorite-button ${formData.is_favorite ? 'favorited' : ''}`}
          onClick={toggleFavorite}
          aria-label={formData.is_favorite ? '移除最愛' : '加入最愛'}
        >
          {formData.is_favorite ? '❤️' : '🤍'}
        </button>
      </div>

      <div className="star-rating">
        <p>星數評分:</p>
        <div className="stars">
          {[1, 2, 3, 4, 5].map((star) => (
            <button
              key={star}
              className={`star ${formData.rating >= star ? 'filled' : ''}`}
              onClick={() => handleRatingChange(star)}
              aria-label={`${star} 顆星`}
            >
              {formData.rating >= star ? '★' : '☆'}
            </button>
          ))}
        </div>

        {formData.rating > 0 && (
          <p className="rating-description">
            {getRatingDescription(formData.rating)}
          </p>
        )}
      </div>

      <div className="feedback-form">
        <label htmlFor={`feedback-text-${card.id}`}>自由文字回饋(可選):</label>
        <textarea
          id={`feedback-text-${card.id}`}
          value={formData.feedback_text}
          onChange={(e) => handleTextChange(e.target.value)}
          placeholder="請告訴我們這張練習卡哪些部分有幫助,哪些可以改進..."
          rows={3}
        />
      </div>

      <button
        className="submit-button"
        onClick={handleSubmit}
        disabled={loading}
      >
        {loading ? '提交中...' : '提交練習卡回饋'}
      </button>

      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}
    </div>
  );
};

const PracticeCardFeedbackForm = ({ cards, sessionId }) => {
  return (
    <div className="feedback-tab practice-card-feedback-tab">
      <h2>回饋層二:PracticeCard 層級 - 單個練習卡的品質評價</h2>
      <p>這些練習卡本身對我的實用程度如何?</p>

      <div className="practice-cards-feedback">
        {cards.map((card) => (
          <PracticeCardFeedbackItem
            key={card.id}
            card={card}
            sessionId={sessionId}
          />
        ))}
      </div>
    </div>
  );
};

export default PracticeCardFeedbackForm;
