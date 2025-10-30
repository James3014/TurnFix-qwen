/**
 * 自適應追問介面 (UI-302)
 * 
 * 設計並實作自適應追問介面
 */
import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import '../styles/AdaptiveFollowupInterface.css';

const AdaptiveFollowupInterface = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { followupNeeds, userInput, selectedOptions } = location.state || {};
  
  const [answers, setAnswers] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  if (!followupNeeds || !followupNeeds.questions || followupNeeds.questions.length === 0) {
    return (
      <div className="adaptive-followup-interface">
        <div className="error-message">
          <h2>無追問問題</h2>
          <button onClick={() => navigate(-1)}>返回上一頁</button>
        </div>
      </div>
    );
  }

  const handleAnswerChange = (questionType, value) => {
    setAnswers(prev => ({
      ...prev,
      [questionType]: value
    }));
  };

  const handleSubmit = async () => {
    setIsLoading(true);
    setError('');
    
    try {
      // 處理陣列字段
      const followupData = {
        ...selectedOptions,
        ...answers
      };
      
      // 調用後端API獲取追問結果
      const response = await fetch('/api/v1/followup-needs', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          input_text: userInput,
          level: selectedOptions?.level,
          terrain: selectedOptions?.terrain,
          style: selectedOptions?.style,
          ...answers
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        // 導向更新後的結果頁面
        navigate('/results', {
          state: {
            recommendedCards: data.recommended_cards,
            userInput,
            selectedOptions: { ...selectedOptions, ...answers },
            followupProvided: true
          }
        });
      } else {
        throw new Error('獲取追問結果失敗');
      }
    } catch (err) {
      setError('提交追問失敗，請稍後再試');
    } finally {
      setIsLoading(false);
    }
  };

  const renderQuestionInput = (question, index) => {
    const questionType = question.type || `question-${index}`;
    
    return (
      <div key={index} className="followup-question">
        <label htmlFor={`question-${index}`}>
          {question.question}
        </label>
        <input
          id={`question-${index}`}
          type="text"
          value={answers[questionType] || ''}
          onChange={(e) => handleAnswerChange(questionType, e.target.value)}
          placeholder="請回答..."
        />
      </div>
    );
  };

  return (
    <div className="adaptive-followup-interface">
      <div className="page-header">
        <h1>❓ 自適應追問</h1>
        <p>為了提供更精準的建議，請回答以下問題</p>
      </div>
      
      <div className="confidence-indicator">
        <p>系統對您的問題辨識置信度：{(followupNeeds.confidence * 100).toFixed(0)}%</p>
        <div className="confidence-bar">
          <div 
            className="confidence-fill" 
            style={{ width: `${followupNeeds.confidence * 100}%` }}
          ></div>
        </div>
      </div>
      
      <div className="questions-section">
        <h2>追問問題 (API-203)</h2>
        <form onSubmit={(e) => e.preventDefault()} className="questions-form">
          {followupNeeds.questions.map((question, index) => 
            renderQuestionInput(question, index)
          )}
          
          {error && <div className="error-message">{error}</div>}
          
          <div className="question-actions">
            <button 
              type="button" 
              className="skip-button"
              onClick={() => navigate(-1)}
              disabled={isLoading}
            >
              跳過追問
            </button>
            <button 
              type="submit" 
              className="submit-button"
              onClick={handleSubmit}
              disabled={isLoading}
            >
              {isLoading ? '處理中...' : '提交回答'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AdaptiveFollowupInterface;