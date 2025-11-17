/**
 * 練習卡管理組件 (UI-308.2)
 *
 * 重構後:使用自定義 Hook 和拆分的子組件
 * 遵循 Linus 原則:
 * - 單一職責:只負責協調子組件
 * - DRY:使用共享的 Hook 和組件
 * - 簡單:< 100 行
 */
import React, { useState } from 'react';
import { usePracticeCards } from '../hooks/usePracticeCards';
import PracticeCardForm from './admin/PracticeCardForm';
import PracticeCardList from './admin/PracticeCardList';
import '../styles/AdminDashboard.css';

const PracticeCardManagement = () => {
  const [showForm, setShowForm] = useState(false);
  const [editingCard, setEditingCard] = useState(null);

  const {
    practiceCards,
    loading,
    error,
    createPracticeCard,
    updatePracticeCard,
    deletePracticeCard
  } = usePracticeCards();

  const handleAdd = () => {
    setEditingCard(null);
    setShowForm(true);
  };

  const handleEdit = (card) => {
    setEditingCard(card);
    setShowForm(true);
  };

  const handleSubmit = async (cardData) => {
    if (editingCard) {
      await updatePracticeCard(editingCard.id, cardData);
    } else {
      await createPracticeCard(cardData);
    }
    setShowForm(false);
    setEditingCard(null);
  };

  const handleCancel = () => {
    setShowForm(false);
    setEditingCard(null);
  };

  const handleDelete = async (cardId) => {
    await deletePracticeCard(cardId);
  };

  // Loading 狀態
  if (loading && practiceCards.length === 0) {
    return (
      <div className="management-page">
        <div className="loading">載入中...</div>
      </div>
    );
  }

  // Error 狀態
  if (error && practiceCards.length === 0) {
    return (
      <div className="management-page">
        <div className="error-message">{error}</div>
      </div>
    );
  }

  return (
    <div className="practice-card-management">
      {showForm ? (
        <PracticeCardForm
          card={editingCard}
          onSubmit={handleSubmit}
          onCancel={handleCancel}
          loading={loading}
        />
      ) : (
        <PracticeCardList
          practiceCards={practiceCards}
          onEdit={handleEdit}
          onDelete={handleDelete}
          onAdd={handleAdd}
        />
      )}
    </div>
  );
};

export default PracticeCardManagement;
