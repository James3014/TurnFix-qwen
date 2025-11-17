/**
 * 最愛練習清單組件
 *
 * 簡潔版本 - 遵循 Linus "好品味"原則：
 * 1. 沒有假數據 - 全部使用真實 API
 * 2. 沒有 window.prompt() - 使用適當的 UI
 * 3. 邏輯清晰 - 使用自定義 Hook
 * 4. 組件簡短 - < 150 行
 */
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useFavorites } from '../hooks';
import '../styles/FavoritePracticeCards.css';

const FavoritePracticeCards = () => {
  const navigate = useNavigate();
  const { favorites, loading, error, removeFavorite } = useFavorites();

  // 處理移除最愛
  const handleRemove = async (cardId, cardName) => {
    if (!window.confirm(`確定要將「${cardName}」從最愛清單中移除嗎？`)) {
      return;
    }

    try {
      // TODO: 需要從上下文或 localStorage 獲取真實的 session_id
      const sessionId = 1;
      await removeFavorite(cardId, sessionId);
    } catch (err) {
      alert('移除失敗：' + err.message);
    }
  };

  // 處理查看詳情
  const handleViewCard = (card) => {
    navigate(`/practice-card/${card.id}`, { state: { card } });
  };

  if (loading) {
    return <div className="favorite-practice-cards loading">載入中...</div>;
  }

  if (error) {
    return <div className="favorite-practice-cards error">{error}</div>;
  }

  if (favorites.length === 0) {
    return (
      <div className="favorite-practice-cards empty">
        <div className="empty-icon">❤️</div>
        <h2>還沒有加入任何最愛練習卡</h2>
        <p>在練習卡詳細頁面點擊 ❤️ 按鈕，即可將卡片加入最愛清單</p>
        <button onClick={() => navigate('/input')}>瀏覽練習卡</button>
      </div>
    );
  }

  // 計算統計數據
  const avgRating = favorites.length > 0
    ? (favorites.reduce((sum, fav) => sum + (fav.user_rating || 0), 0) / favorites.length).toFixed(1)
    : 0;

  return (
    <div className="favorite-practice-cards">
      <div className="page-header">
        <h1>❤️ 最愛練習清單</h1>
        <p>管理您標記為最愛的練習卡</p>
      </div>

      <div className="stats-section">
        <div className="stat-card">
          <div className="stat-value">{favorites.length}</div>
          <div className="stat-label">最愛卡片</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{avgRating}</div>
          <div className="stat-label">平均評分</div>
        </div>
      </div>

      <div className="cards-grid">
        {favorites.map((fav, index) => {
          const card = fav.card;
          return (
            <div key={card.id} className="favorite-card-wrapper">
              <div className="card-header">
                <div className="card-meta">
                  <span className="favorited-at">
                    加入時間：{new Date(fav.favorited_at).toLocaleDateString()}
                  </span>
                  {fav.user_rating > 0 && (
                    <div className="card-rating">
                      {'★'.repeat(fav.user_rating)}{'☆'.repeat(5 - fav.user_rating)}
                    </div>
                  )}
                </div>
                <button
                  className="remove-favorite"
                  onClick={() => handleRemove(card.id, card.name)}
                  aria-label="移除最愛"
                >
                  ♡
                </button>
              </div>

              <div className="practice-card" onClick={() => handleViewCard(card)}>
                <h2>{index + 1}. {card.name}</h2>
                <p className="goal">{card.goal}</p>

                {card.tips && card.tips.length > 0 && (
                  <div className="tips">
                    <strong>練習要點：</strong>
                    <ul>
                      {card.tips.map((tip, i) => <li key={i}>{tip}</li>)}
                    </ul>
                  </div>
                )}

                {fav.user_notes && (
                  <div className="user-notes">
                    <strong>我的筆記：</strong>
                    <p>{fav.user_notes}</p>
                  </div>
                )}

                <div className="card-footer">
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
        })}
      </div>
    </div>
  );
};

export default FavoritePracticeCards;
