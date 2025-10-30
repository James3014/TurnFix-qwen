/**
 * 最愛練習清單組件 (UI-309)
 * 
 * 設計並實作最愛練習清單介面
 */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/FavoritePracticeCards.css';

const FavoritePracticeCards = () => {
  const navigate = useNavigate();
  const [favoriteCards, setFavoriteCards] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // 模擬數據 - 實際實現中會從API獲取
  useEffect(() => {
    const mockFavorites = [
      {
        id: 101,
        name: "J型轉彎練習",
        goal: "完成外腳承重再過中立",
        tips: ["視線外緣", "外腳 70–80%", "中立後換刃"],
        pitfalls: "避免提前壓內腳",
        dosage: "藍線 6 次/趟 ×3 趟",
        level: ["初級", "中級"],
        terrain: ["綠線", "藍線"],
        self_check: ["是否在換刃前感到外腳壓力峰值？"],
        card_type: "技術",
        rating: 5,
        last_practiced: "2025-10-28",
        notes: "這個練習對改善後坐問題很有幫助"
      },
      {
        id: 102,
        name: "重心轉移練習",
        goal: "改善重心控制",
        tips: ["身體前傾", "膝蓋彎曲", "重心保持在腳掌中心"],
        pitfalls: "避免重心過後或過前",
        dosage: "平地 10 次 ×3 組",
        level: ["初級", "中級"],
        terrain: ["綠線"],
        self_check: ["重心是否能穩定在腳掌中心？"],
        card_type: "基礎",
        rating: 4,
        last_practiced: "2025-10-25",
        notes: "對初學者很實用"
      },
      {
        id: 201,
        name: "基礎滑行練習",
        goal: "提升基本滑行穩定性",
        tips: ["膝蓋微彎", "重心稍前", "保持平衡"],
        pitfalls: "避免僵直站立",
        dosage: "平地 5 分鐘",
        level: ["初級"],
        terrain: ["綠線"],
        self_check: ["滑行時是否感到穩定？"],
        card_type: "基礎",
        rating: 4,
        last_practiced: "2025-10-20",
        notes: "每次滑行前都會做"
      }
    ];
    
    setFavoriteCards(mockFavorites);
    setLoading(false);
  }, []);

  const handleRemoveFavorite = (cardId) => {
    // 這裡應該發送API請求移除最愛標記
    setFavoriteCards(prev => prev.filter(card => card.id !== cardId));
  };

  const handleViewCard = (card) => {
    // 導向練習卡詳細頁面
    navigate(`/practice-card/${card.id}`, { state: { card } });
  };

  const handleEditNotes = (cardId, newNotes) => {
    // 更新筆記
    setFavoriteCards(prev => 
      prev.map(card => 
        card.id === cardId ? { ...card, notes: newNotes } : card
      )
    );
  };

  if (loading) {
    return (
      <div className="favorite-practice-cards">
        <div className="loading">載入中...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="favorite-practice-cards">
        <div className="error-message">{error}</div>
      </div>
    );
  }

  return (
    <div className="favorite-practice-cards">
      <div className="page-header">
        <h1>❤️ 最愛練習清單</h1>
        <p>管理您標記為最愛的練習卡</p>
      </div>
      
      {favoriteCards.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">❤️</div>
          <h2>還沒有加入任何最愛練習卡</h2>
          <p>在練習卡詳細頁面點擊 ❤️ 按鈕，即可將卡片加入最愛清單</p>
          <button 
            className="browse-button"
            onClick={() => navigate('/input')}
          >
            瀏覽練習卡
          </button>
        </div>
      ) : (
        <div className="favorites-content">
          <div className="stats-section">
            <div className="stat-card">
              <div className="stat-value">{favoriteCards.length}</div>
              <div className="stat-label">最愛卡片</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">
                {Math.round(favoriteCards.reduce((sum, card) => sum + card.rating, 0) / favoriteCards.length * 10) / 10}
              </div>
              <div className="stat-label">平均評分</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">
                {new Set(favoriteCards.flatMap(card => card.level)).size}
              </div>
              <div className="stat-label">等級覆蓋</div>
            </div>
          </div>
          
          <div className="cards-grid">
            {favoriteCards.map((card, index) => (
              <div key={card.id} className="favorite-card-wrapper">
                <div className="card-header">
                  <div className="card-meta">
                    <span className="last-practiced">
                      最近練習：{card.last_practiced}
                    </span>
                    <div className="card-rating">
                      {'★'.repeat(card.rating) + '☆'.repeat(5 - card.rating)}
                    </div>
                  </div>
                  <button 
                    className="remove-favorite"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleRemoveFavorite(card.id);
                    }}
                    aria-label="移除最愛"
                  >
                    ♡
                  </button>
                </div>
                
                <div 
                  className="practice-card"
                  onClick={() => handleViewCard(card)}
                >
                  <div className="card-title-section">
                    <h2 className="card-title">
                      {index + 1}. {card.name}
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
                
                <div className="card-notes">
                  <div className="notes-header">
                    <h4>練習筆記</h4>
                    <button 
                      className="edit-notes"
                      onClick={() => {
                        const newNotes = prompt('編輯練習筆記：', card.notes || '');
                        if (newNotes !== null) {
                          handleEditNotes(card.id, newNotes);
                        }
                      }}
                    >
                      編輯
                    </button>
                  </div>
                  <p>{card.notes || '還沒有添加筆記'}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default FavoritePracticeCards;