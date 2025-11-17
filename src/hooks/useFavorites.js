/**
 * useFavorites Hook
 *
 * 管理最愛練習卡的狀態和操作
 * 遵循 Linus 原則：簡單、清晰、無特殊情況
 */
import { useState, useEffect } from 'react';
import { favoritesAPI } from '../api/client';

export const useFavorites = () => {
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // 載入最愛清單
  const loadFavorites = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await favoritesAPI.getAll();
      setFavorites(response.favorite_cards || []);
    } catch (err) {
      setError(err.message || '載入最愛清單失敗');
      console.error('Load favorites error:', err);
    } finally {
      setLoading(false);
    }
  };

  // 切換最愛狀態
  const toggleFavorite = async (cardId, isFavorite, sessionId) => {
    try {
      await favoritesAPI.toggle(cardId, {
        is_favorite: isFavorite,
        session_id: sessionId,
      });
      await loadFavorites(); // 重新載入
    } catch (err) {
      setError(err.message || '更新最愛狀態失敗');
      console.error('Toggle favorite error:', err);
      throw err;
    }
  };

  // 移除最愛
  const removeFavorite = async (cardId, sessionId) => {
    try {
      await favoritesAPI.remove(cardId, { session_id: sessionId });
      // 立即更新本地狀態，不需要重新請求 API
      setFavorites(prev => prev.filter(fav => fav.card.id !== cardId));
    } catch (err) {
      setError(err.message || '移除最愛失敗');
      console.error('Remove favorite error:', err);
      throw err;
    }
  };

  // 初始載入
  useEffect(() => {
    loadFavorites();
  }, []);

  return {
    favorites,
    loading,
    error,
    toggleFavorite,
    removeFavorite,
    reload: loadFavorites,
  };
};
