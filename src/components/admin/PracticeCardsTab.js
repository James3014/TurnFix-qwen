/**
 * 管理後台 - 練習卡管理標籤
 * 簡潔版本，使用 usePracticeCards hook
 */
import React from 'react';
import { usePracticeCards } from '../../hooks';

const PracticeCardsTab = () => {
  const { practiceCards, loading, error, deletePracticeCard } = usePracticeCards();

  const handleDelete = async (id, name) => {
    if (!window.confirm(`確定要刪除練習卡「${name}」嗎？`)) return;

    try {
      await deletePracticeCard(id);
    } catch (err) {
      alert('刪除失敗：' + err.message);
    }
  };

  if (loading) return <div className="loading">載入中...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="practice-cards-tab">
      <div className="tab-header">
        <h2>練習卡管理</h2>
        <button className="btn-primary">新增練習卡</button>
      </div>

      <div className="data-table">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>練習卡名稱</th>
              <th>目標</th>
              <th>類型</th>
              <th>等級</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            {practiceCards.map(card => (
              <tr key={card.id}>
                <td>{card.id}</td>
                <td>{card.name}</td>
                <td>{card.goal}</td>
                <td>{card.card_type || '-'}</td>
                <td>{card.level?.join(', ') || '-'}</td>
                <td>
                  <button className="btn-edit">編輯</button>
                  <button
                    className="btn-delete"
                    onClick={() => handleDelete(card.id, card.name)}
                  >
                    刪除
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default PracticeCardsTab;
