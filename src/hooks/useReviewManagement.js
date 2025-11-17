/**
 * 審核管理自定義 Hook
 */
import { useState, useEffect } from 'react';

export const useReviewManagement = () => {
  const [snippets, setSnippets] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSnippets();
  }, []);

  const fetchSnippets = async () => {
    // 模擬數據
    const mockData = [
      {
        id: 1,
        symptom: '重心太後',
        practice_tips: ['保持上身直立', '重心向前移'],
        pitfalls: ['避免後坐', '不要過度彎曲膝蓋'],
        dosage: '藍線6次/趟×3趟',
        source_snippet: '當重心太後時，會導致後坐，建議保持上身直立，重心向前移...',
        review_status: 'pending',
        confidence: 0.85,
        original_text: '重心太後是一個常見問題，會影響滑行控制...'
      },
      {
        id: 2,
        symptom: '無法換刃',
        practice_tips: ['增加壓力轉移', '提前準備換刃動作'],
        pitfalls: ['避免突然換刃', '不要過度用力'],
        dosage: '綠線5次/趟×2趟',
        source_snippet: '很多學員無法順利換刃，這通常是由於壓力轉移不夠...',
        review_status: 'pending',
        confidence: 0.72,
        original_text: '無法換刃是進階滑行的障礙，需要加強壓力轉移...'
      },
      {
        id: 3,
        symptom: '轉彎不穩',
        practice_tips: ['加強核心穩定', '注意視線方向'],
        pitfalls: ['避免低頭看腳', '不要身體僵硬'],
        dosage: '藍線4次/趟×3趟',
        source_snippet: '轉彎不穩通常源於核心力量不足或視線錯誤...',
        review_status: 'approved',
        confidence: 0.9,
        original_text: '轉彎時保持穩定需要良好的核心控制...'
      }
    ];

    setSnippets(mockData);
    setLoading(false);
  };

  const approveSnippet = (id) => {
    setSnippets(prev => prev.map(s =>
      s.id === id ? { ...s, review_status: 'approved' } : s
    ));
  };

  const rejectSnippet = (id) => {
    setSnippets(prev => prev.map(s =>
      s.id === id ? { ...s, review_status: 'rejected' } : s
    ));
  };

  const batchApprove = (ids) => {
    setSnippets(prev => prev.map(s =>
      ids.has(s.id) ? { ...s, review_status: 'approved' } : s
    ));
  };

  const batchReject = (ids) => {
    setSnippets(prev => prev.map(s =>
      ids.has(s.id) ? { ...s, review_status: 'rejected' } : s
    ));
  };

  return {
    snippets,
    loading,
    approveSnippet,
    rejectSnippet,
    batchApprove,
    batchReject
  };
};
