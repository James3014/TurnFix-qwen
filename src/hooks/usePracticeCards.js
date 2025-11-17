/**
 * usePracticeCards Hook
 *
 * 管理練習卡的狀態和操作
 * 遵循 Linus 原則：簡單、清晰、無特殊情況
 */
import { useState, useEffect } from 'react';
import { practiceCardsAPI } from '../api/client';

export const usePracticeCards = (autoLoad = true) => {
  const [practiceCards, setPracticeCards] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // 載入所有練習卡
  const loadPracticeCards = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await practiceCardsAPI.getAll();
      setPracticeCards(response.practice_cards || []);
    } catch (err) {
      setError(err.message || '載入練習卡失敗');
      console.error('Load practice cards error:', err);
    } finally {
      setLoading(false);
    }
  };

  // 根據 ID 獲取練習卡
  const getPracticeCard = async (id) => {
    try {
      setLoading(true);
      setError(null);
      const response = await practiceCardsAPI.getById(id);
      return response.practice_card;
    } catch (err) {
      setError(err.message || '載入練習卡失敗');
      console.error('Get practice card error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // 創建練習卡
  const createPracticeCard = async (data) => {
    try {
      setLoading(true);
      setError(null);
      const response = await practiceCardsAPI.create(data);
      await loadPracticeCards(); // 重新載入列表
      return response.practice_card;
    } catch (err) {
      setError(err.message || '創建練習卡失敗');
      console.error('Create practice card error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // 更新練習卡
  const updatePracticeCard = async (id, data) => {
    try {
      setLoading(true);
      setError(null);
      const response = await practiceCardsAPI.update(id, data);
      await loadPracticeCards(); // 重新載入列表
      return response.practice_card;
    } catch (err) {
      setError(err.message || '更新練習卡失敗');
      console.error('Update practice card error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // 刪除練習卡
  const deletePracticeCard = async (id) => {
    try {
      setLoading(true);
      setError(null);
      await practiceCardsAPI.delete(id);
      // 立即更新本地狀態
      setPracticeCards(prev => prev.filter(card => card.id !== id));
    } catch (err) {
      setError(err.message || '刪除練習卡失敗');
      console.error('Delete practice card error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // 自動載入（可選）
  useEffect(() => {
    if (autoLoad) {
      loadPracticeCards();
    }
  }, [autoLoad]);

  return {
    practiceCards,
    loading,
    error,
    loadPracticeCards,
    getPracticeCard,
    createPracticeCard,
    updatePracticeCard,
    deletePracticeCard,
  };
};
