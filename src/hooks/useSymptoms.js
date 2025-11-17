/**
 * useSymptoms Hook
 *
 * 管理症狀的狀態和操作
 * 遵循 Linus 原則：簡單、清晰、無特殊情況
 */
import { useState, useEffect } from 'react';
import { symptomsAPI } from '../api/client';

export const useSymptoms = (autoLoad = true) => {
  const [symptoms, setSymptoms] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // 載入所有症狀
  const loadSymptoms = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await symptomsAPI.getAll();
      setSymptoms(response.symptoms || []);
    } catch (err) {
      setError(err.message || '載入症狀失敗');
      console.error('Load symptoms error:', err);
    } finally {
      setLoading(false);
    }
  };

  // 根據 ID 獲取症狀
  const getSymptom = async (id) => {
    try {
      setLoading(true);
      setError(null);
      const response = await symptomsAPI.getById(id);
      return response.symptom;
    } catch (err) {
      setError(err.message || '載入症狀失敗');
      console.error('Get symptom error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // 創建症狀
  const createSymptom = async (data) => {
    try {
      setLoading(true);
      setError(null);
      const response = await symptomsAPI.create(data);
      await loadSymptoms(); // 重新載入列表
      return response.symptom;
    } catch (err) {
      setError(err.message || '創建症狀失敗');
      console.error('Create symptom error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // 更新症狀
  const updateSymptom = async (id, data) => {
    try {
      setLoading(true);
      setError(null);
      const response = await symptomsAPI.update(id, data);
      await loadSymptoms(); // 重新載入列表
      return response.symptom;
    } catch (err) {
      setError(err.message || '更新症狀失敗');
      console.error('Update symptom error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // 刪除症狀
  const deleteSymptom = async (id) => {
    try {
      setLoading(true);
      setError(null);
      await symptomsAPI.delete(id);
      // 立即更新本地狀態
      setSymptoms(prev => prev.filter(symptom => symptom.id !== id));
    } catch (err) {
      setError(err.message || '刪除症狀失敗');
      console.error('Delete symptom error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // 獲取症狀的練習卡
  const getSymptomPracticeCards = async (symptomId) => {
    try {
      setLoading(true);
      setError(null);
      const response = await symptomsAPI.getPracticeCards(symptomId);
      return response.practice_cards || [];
    } catch (err) {
      setError(err.message || '載入症狀練習卡失敗');
      console.error('Get symptom practice cards error:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // 自動載入（可選）
  useEffect(() => {
    if (autoLoad) {
      loadSymptoms();
    }
  }, [autoLoad]);

  return {
    symptoms,
    loading,
    error,
    loadSymptoms,
    getSymptom,
    createSymptom,
    updateSymptom,
    deleteSymptom,
    getSymptomPracticeCards,
  };
};
