/**
 * 練習卡列表組件 (UI-303)
 * 
 * 設計並實作練習卡展示介面
 */
import React from 'react';
import PracticeCard from './PracticeCard';
import '../styles/PracticeCardList.css';

const PracticeCardList = ({ cards, showCountMessage = true, onCardSelect }) => {
  const getCountMessage = () => {
    if (!cards || cards.length === 0) return '';
    
    if (cards.length < 3) {
      return `找到 ${cards.length} 張練習卡，建議至少 3 張`;
    } else if (cards.length > 5) {
      return `共找到 ${cards.length} 張，已顯示排名前 5 張`;
    }
    return `已為您推薦 ${cards.length} 張練習卡`;
  };

  if (!cards || cards.length === 0) {
    return (
      <div className="practice-card-list">
        <div className="no-cards-message">
          <h2>暫無練習建議</h2>
          <p>請稍後再試或提供更多資訊</p>
        </div>
      </div>
    );
  }

  return (
    <div className="practice-card-list">
      {showCountMessage && (
        <div className="count-message">
          {getCountMessage()}
        </div>
      )}
      
      <div className="cards-grid">
        {cards.map((card, index) => (
          <PracticeCard
            key={card.id}
            card={card}
            index={index}
            onSelect={onCardSelect}
          />
        ))}
      </div>
    </div>
  );
};

export default PracticeCardList;