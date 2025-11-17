/**
 * SessionFeedbackForm 組件
 *
 * 會話層級的回饋表單
 * 遵循 Linus 原則:簡單、清晰、單一職責
 */
import React, { useState } from 'react';
import { feedbackAPI } from '../../api/client';
import Button from '../common/Button';

const SessionFeedbackForm = ({ sessionId }) => {
  const [formData, setFormData] = useState({
    rating: '',
    feedback_text: '',
    feedback_type: 'immediate'
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async () => {
    if (!formData.rating) {
      setError('請選擇評分');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      await feedbackAPI.submitSessionFeedback({
        session_id: sessionId,
        ...formData
      });
      setSuccess('會話回饋已提交成功!');
      // 重置表單
      setFormData({
        rating: '',
        feedback_text: '',
        feedback_type: 'immediate'
      });
    } catch (err) {
      setError(err.message || '提交會話回饋失敗,請稍後再試');
    } finally {
      setLoading(false);
    }
  };

  const ratingOptions = [
    { value: 'not_applicable', label: '❌ 不適用' },
    { value: 'partially_applicable', label: '△ 部分適用' },
    { value: 'applicable', label: '✓ 適用' }
  ];

  return (
    <div className="feedback-tab session-feedback-tab">
      <h2>回饋層一:Session 層級 - 整個問題推薦流程的效果評價</h2>
      <p>這些推薦的練習卡是否幫助改善了我的問題?</p>

      <div className="rating-options">
        {ratingOptions.map(({ value, label }) => (
          <div key={value} className="rating-option">
            <input
              type="radio"
              id={value}
              name="session_rating"
              value={value}
              checked={formData.rating === value}
              onChange={(e) => handleChange('rating', e.target.value)}
            />
            <label htmlFor={value} className={`rating-label ${value.replace('_', '-')}`}>
              {label}
            </label>
          </div>
        ))}
      </div>

      <div className="feedback-form">
        <label htmlFor="session-feedback-text">自由文字回饋(可選):</label>
        <textarea
          id="session-feedback-text"
          value={formData.feedback_text}
          onChange={(e) => handleChange('feedback_text', e.target.value)}
          placeholder="請告訴我們這些推薦的練習卡哪些部分有幫助,哪些可以改進..."
          rows={4}
        />
      </div>

      <div className="feedback-type">
        <label>回饋類型:</label>
        <div className="radio-group">
          <label className="radio-label">
            <input
              type="radio"
              name="feedback_type"
              value="immediate"
              checked={formData.feedback_type === 'immediate'}
              onChange={(e) => handleChange('feedback_type', e.target.value)}
            />
            <span className="radio-custom"></span>
            即時回饋
          </label>
          <label className="radio-label">
            <input
              type="radio"
              name="feedback_type"
              value="delayed"
              checked={formData.feedback_type === 'delayed'}
              onChange={(e) => handleChange('feedback_type', e.target.value)}
            />
            <span className="radio-custom"></span>
            延遲回饋(練習後評價)
          </label>
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}

      <div className="feedback-actions">
        <Button onClick={handleSubmit} disabled={loading}>
          {loading ? '提交中...' : '提交會話回饋'}
        </Button>
      </div>
    </div>
  );
};

export default SessionFeedbackForm;
