/**
 * 練習卡組件 (UI-303)
 * 
 * 設計並實作練習卡展示介面
 */
import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/PracticeCard.css';

const PracticeCard = ({ card, index, onSelect }) => {
  const navigate = useNavigate();

  const handleCardClick = () => {
    if (onSelect) {
      onSelect(card);
    } else {
      // 默認行為：導向詳細頁面
      navigate(`/practice-card/${card.id}`, { state: { card } });
    }
  };

  const renderTips = () => {
    if (!card.tips || card.tips.length === 0) return null;
    
    return (
      <div className="card-section">
        <h3>練習要點</h3>
        <ul>
          {card.tips.map((tip, idx) => (
            <li key={idx}>{tip}</li>
          ))}
        </ul>
      </div>
    );
  };

  const renderSelfCheck = () => {
    if (!card.self_check || card.self_check.length === 0) return null;
    
    return (
      <div className="card-section">
        <h3>自我檢查點</h3>
        <ul>
          {card.self_check.map((check, idx) => (
            <li key={idx}>{check}</li>
          ))}
        </ul>
      </div>
    );
  };

  const renderMetaInfo = () => {
    const metaItems = [];
    
    if (card.level && card.level.length > 0) {
      metaItems.push(`等級: ${card.level.join(', ')}`);
    }
    
    if (card.terrain && card.terrain.length > 0) {
      metaItems.push(`地形: ${card.terrain.join(', ')}`);
    }
    
    return metaItems.length > 0 ? (
      <div className="card-meta">
        {metaItems.map((item, idx) => (
          <span key={idx} className="meta-item">{item}</span>
        ))}
      </div>
    ) : null;
  };

  return (
    <div className="practice-card" onClick={handleCardClick}>
      <div className="card-header">
        <h2 className="card-title">
          {index !== undefined ? `${index + 1}. ` : ''}
          {card.name}
        </h2>
        <span className="card-type">{card.card_type}</span>
      </div>
      
      <div className="card-body">
        <div className="card-section">
          <h3>練習目標</h3>
          <p>{card.goal}</p>
        </div>
        
        {renderTips()}
        
        <div className="card-section">
          <h3>常見錯誤</h3>
          <p>{card.pitfalls}</p>
        </div>
        
        <div className="card-section">
          <h3>建議次數</h3>
          <p>{card.dosage}</p>
        </div>
        
        {renderSelfCheck()}
      </div>
      
      <div className="card-footer">
        {renderMetaInfo()}
      </div>
    </div>
  );
};

export default PracticeCard;