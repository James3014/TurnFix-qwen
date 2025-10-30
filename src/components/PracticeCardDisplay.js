/**
 * 練習卡展示組件 (UI-303)
 * 
 * 設計並實作練習卡展示介面
 */
import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import '../styles/PracticeCardDisplay.css';

const PracticeCardDisplay = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { recommendedCards, userInput, selectedOptions } = location.state || {};
  
  const [activeCardIndex, setActiveCardIndex] = useState(0);
  const [showFollowup, setShowFollowup] = useState(false);
  const [followupQuestions, setFollowupQuestions] = useState([]);
  const [followupAnswers, setFollowupAnswers] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  if (!recommendedCards || recommendedCards.length === 0) {
    return (
      <div className="practice-card-display">
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

  const renderCardNavigation = () => (
    <div className="card-navigation">
      <button 
        className="nav-button prev"
        onClick={() => setActiveCardIndex(prev => Math.max(0, prev - 1))}
        disabled={activeCardIndex === 0}
      >
        ← 上一張
      </button>
      
      <div className="card-indicators">
        {recommendedCards.map((_, index) => (
          <button
            key={index}
            className={`indicator ${index === activeCardIndex ? 'active' : ''}`}
            onClick={() => setActiveCardIndex(index)}
            aria-label={`第 ${index + 1} 張練習卡`}
          >
            {index + 1}
          </button>
        ))}
      </div>
      
      <button 
        className="nav-button next"
        onClick={() => setActiveCardIndex(prev => Math.min(recommendedCards.length - 1, prev + 1))}
        disabled={activeCardIndex === recommendedCards.length - 1}
      >
        下一張 →
      </button>
    </div>
  );

  const renderActiveCard = () => {
    const card = recommendedCards[activeCardIndex];
    
    return (
      <div className="practice-card active">
        <div className="card-header">
          <h2 className="card-title">
            {activeCardIndex + 1}. {card.name}
          </h2>
          <span className="card-type">{card.card_type}</span>
        </div>
        
        <div className="card-body">
          <div className="card-section">
            <h3>練習目標</h3>
            <p>{card.goal}</p>
          </div>
          
          <div className="card-section">
            <h3>練習要點</h3>
            <ul>
              {card.tips.map((tip, idx) => (
                <li key={idx}>{tip}</li>
              ))}
            </ul>
          </div>
          
          <div className="card-section">
            <h3>常見錯誤</h3>
            <p>{card.pitfalls}</p>
          </div>
          
          <div className="card-section">
            <h3>建議次數</h3>
            <p>{card.dosage}</p>
          </div>
          
          <div className="card-section">
            <h3>自我檢查點</h3>
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
    );
  };

  return (
    <div className="practice-card-display">
      <div className="page-header">
        <h1>🎿 練習卡展示</h1>
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
        {renderCardNavigation()}
        {renderActiveCard()}
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

export default PracticeCardDisplay;