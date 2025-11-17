/**
 * PracticeCardList 組件
 *
 * 顯示練習卡列表並提供編輯/刪除操作
 * 遵循 Linus 原則:簡單、清晰、單一職責
 */
import React from 'react';
import Button from '../common/Button';

const PracticeCardList = ({
  practiceCards,
  onEdit,
  onDelete,
  onAdd
}) => {
  const handleDelete = async (cardId, cardName) => {
    if (!window.confirm(`確定要刪除「${cardName}」嗎?`)) {
      return;
    }
    await onDelete(cardId);
  };

  return (
    <div className="management-page">
      <div className="list-header">
        <h1>練習卡管理</h1>
        <p>管理滑雪練習建議卡庫</p>
        <Button onClick={onAdd}>
          + 新增練習卡
        </Button>
      </div>

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>名稱</th>
              <th>目標</th>
              <th>類型</th>
              <th>適用等級</th>
              <th>適用地形</th>
              <th>要點數量</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            {practiceCards.length === 0 ? (
              <tr>
                <td colSpan="8" style={{ textAlign: 'center', padding: '2rem' }}>
                  暫無練習卡數據
                </td>
              </tr>
            ) : (
              practiceCards.map(card => (
                <tr key={card.id}>
                  <td>{card.id}</td>
                  <td>{card.name}</td>
                  <td>{card.goal?.substring(0, 30)}...</td>
                  <td>{card.card_type}</td>
                  <td>{Array.isArray(card.level) ? card.level.join(', ') : card.level}</td>
                  <td>{Array.isArray(card.terrain) ? card.terrain.join(', ') : card.terrain}</td>
                  <td>{Array.isArray(card.tips) ? card.tips.length : 0}</td>
                  <td>
                    <button
                      className="action-button edit"
                      onClick={() => onEdit(card)}
                    >
                      編輯
                    </button>
                    <button
                      className="action-button delete"
                      onClick={() => handleDelete(card.id, card.name)}
                    >
                      刪除
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default PracticeCardList;
