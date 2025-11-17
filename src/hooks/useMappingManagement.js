/**
 * 映射管理自定義 Hook
 * 處理症狀練習卡映射的數據邏輯
 */
import { useState, useEffect } from 'react';

export const useMappingManagement = () => {
  const [mappings, setMappings] = useState([]);
  const [symptoms, setSymptoms] = useState([]);
  const [practiceCards, setPracticeCards] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      // 模擬數據 - 實際從 API 加載
      setMappings([
        { symptom_id: 1, symptom_name: "重心太後", practice_id: 101, practice_name: "J型轉彎練習", order: 1 },
        { symptom_id: 1, symptom_name: "重心太後", practice_id: 102, practice_name: "重心轉移練習", order: 2 },
        { symptom_id: 2, symptom_name: "重心不穩", practice_id: 201, practice_name: "基礎滑行練習", order: 1 }
      ]);

      setSymptoms([
        { id: 1, name: "重心太後", category: "技術" },
        { id: 2, name: "重心不穩", category: "技術" },
        { id: 3, name: "換刃困難", category: "技術" }
      ]);

      setPracticeCards([
        { id: 101, name: "J型轉彎練習", card_type: "技術" },
        { id: 102, name: "重心轉移練習", card_type: "基礎" },
        { id: 201, name: "基礎滑行練習", card_type: "基礎" }
      ]);
    } catch (err) {
      setError('加載數據失敗');
    } finally {
      setLoading(false);
    }
  };

  const createMapping = async (data) => {
    const response = await fetch('/api/v1/admin/symptom-practice-mappings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    if (response.ok) {
      const newMapping = await response.json();
      setMappings(prev => [...prev, newMapping.mapping]);
    } else {
      throw new Error('創建映射失敗');
    }
  };

  const updateMapping = async (oldMapping, data) => {
    const response = await fetch(
      `/api/v1/admin/symptom-practice-mappings/${oldMapping.symptom_id}/${oldMapping.practice_id}`,
      {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      }
    );

    if (response.ok) {
      const updated = await response.json();
      setMappings(prev => prev.map(m =>
        m.symptom_id === oldMapping.symptom_id && m.practice_id === oldMapping.practice_id
          ? updated.mapping
          : m
      ));
    } else {
      throw new Error('更新映射失敗');
    }
  };

  const deleteMapping = async (symptomId, practiceId) => {
    const response = await fetch(
      `/api/v1/admin/symptom-practice-mappings/${symptomId}/${practiceId}`,
      { method: 'DELETE' }
    );

    if (response.ok) {
      setMappings(prev => prev.filter(m =>
        !(m.symptom_id === symptomId && m.practice_id === practiceId)
      ));
    } else {
      throw new Error('刪除映射失敗');
    }
  };

  return {
    mappings,
    symptoms,
    practiceCards,
    loading,
    error,
    setError,
    createMapping,
    updateMapping,
    deleteMapping
  };
};
