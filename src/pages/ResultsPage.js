/**
 * 結果頁面 (UI-303)
 * 
 * 設計並實作練習卡展示介面
 */
import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import '../styles/ResultsPage.css';

const ResultsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { recommendedCards, userInput, selectedOptions } = location.state || {};
  
  const [showFollowup, setShowFollowup] = useState(false);
  const [followupQuestions, setFollowupQuestions] = useState([]);
  const [followupAnswers, setFollowupAnswers] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  if (!recommendedCards) {
    return (
      <div className="results-page">
        <div className="error-message">
          <h2>未找到練習建議</h2>
          <button onClick={() => navigate('/input')}>重新輸入</button>
        </div>
      </div>
    );
  }

  const handleFollowupSubmit = async () => {
    setIsLoading(true);
    setError('');
    
    try {
      // 這裡應該調用後端API獲取追問結果
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
          ...followupAnswers
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        // 導向更新後的結果頁面
        navigate('/results', {
          state: {
            recommendedCards: data.recommended_cards,
            userInput,
            selectedOptions: { ...selectedOptions, ...followupAnswers },
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

  const handleAnswerChange = (questionType, value) => {
    setFollowupAnswers(prev => ({
      ...prev,
      [questionType]: value
    }));
  };

  const renderFollowupSection = () => {
    if (!showFollowup || followupQuestions.length === 0) {
      return (
        <div className="followup-section">
          <button 
            className="followup-button"
            onClick={() => setShowFollowup(true)}
          >
            需要更多幫助？點擊進行追問
          </button>
        </div>
      );
    }

    return (
      <div className="followup-section expanded">
        <h2>追問問題</h2>
        {followupQuestions.map((question, index) => (
          <div key={index} className="followup-question">
            <label>{question.question}</label>
            <input
              type="text"
              value={followupAnswers[question.type] || ''}
              onChange={(e) => handleAnswerChange(question.type, e.target.value)}
              placeholder="請回答..."
            />
          </div>
        ))}
        <button 
          className="submit-followup"
          onClick={handleFollowupSubmit}
          disabled={isLoading}
        >
          {isLoading ? '處理中...' : '提交追問'}
        </button>
        <button 
          className="cancel-followup"
          onClick={() => setShowFollowup(false)}
        >
          取消
        </button>
        {error && <div className="error-message">{error}</div>}
      </div>
    );
  };

  const renderUserInputSummary = () => {
    if (!userInput && !selectedOptions) return null;
    
    return (
      <div className="user-input-summary">
        <h2>您的問題描述</h2>
        {userInput && <p><strong>問題：</strong>{userInput}</p>}
        {selectedOptions && (
          <div className="options-summary">
            {selectedOptions.level && <span>等級：{selectedOptions.level}</span>}
            {selectedOptions.terrain && <span>地形：{selectedOptions.terrain}</span>}
            {selectedOptions.style && <span>風格：{selectedOptions.style}</span>}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="results-page">
      <div className="page-header">
        <h1>🎿 滑雪練習建議</h1>
        <button 
          className="restart-button"
          onClick={() => navigate('/input')}
        >
          重新診斷
        </button>
      </div>
      
      {renderUserInputSummary()}
      
      <div className="results-section">
        <h2>為您推薦的練習</h2>
        <div className="cards-grid">
          {recommendedCards.map((card, index) => (
            <div key={card.id} className="practice-card">
              <div className="card-header">
                <h3 className="card-title">
                  {index + 1}. {card.name}
                </h3>
                <span className="card-type">{card.card_type}</span>
              </div>
              
              <div className="card-body">
                <div className="card-section">
                  <h4>練習目標</h4>
                  <p>{card.goal}</p>
                </div>
                
                <div className="card-section">
                  <h4>練習要點</h4>
                  <ul>
                    {card.tips.map((tip, idx) => (
                      <li key={idx}>{tip}</li>
                    ))}
                  </ul>
                </div>
                
                <div className="card-section">
                  <h4>常見錯誤</h4>
                  <p>{card.pitfalls}</p>
                </div>
                
                <div className="card-section">
                  <h4>建議次數</h4>
                  <p>{card.dosage}</p>
                </div>
                
                <div className="card-section">
                  <h4>自我檢查點</h4>
                  <ul>
                    {card.self_check.map((check, idx) => (
                      <li key={idx}>{check}</li>
                    ))}
                  </ul>
                </div>
              </div>
              
              <div className="card-footer">
                <div className="card-meta">
                  {card.level && card.level.length > 0 && (
                    <span className="meta-item">等級: {card.level.join(', ')}</span>
                  )}
                  {card.terrain && card.terrain.length > 0 && (
                    <span className="meta-item">地形: {card.terrain.join(', ')}</span>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
      
      {renderFollowupSection()}
      
      <div className="feedback-section">
        <h2>這些練習卡有幫助嗎？</h2>
        <div className="feedback-options">
          <button className="feedback-option negative">
            ❌ 不適用
          </button>
          <button className="feedback-option neutral">
            △ 部分適用
          </button>
          <button className="feedback-option positive">
            ✓ 適用
          </button>
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;