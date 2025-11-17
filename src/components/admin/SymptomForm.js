/**
 * SymptomForm 組件
 *
 * 症狀創建/編輯表單
 * 遵循 Linus 原則:簡單、清晰、單一職責
 */
import React, { useState, useEffect } from 'react';
import Button from '../common/Button';

const SymptomForm = ({ symptom, onSubmit, onCancel, loading }) => {
  const [formData, setFormData] = useState(getInitialFormData());
  const [error, setError] = useState('');

  function getInitialFormData(symptomData = null) {
    if (symptomData) {
      return {
        name: symptomData.name || '',
        category: symptomData.category || '',
        synonyms: Array.isArray(symptomData.synonyms) ? symptomData.synonyms.join(', ') : '',
        level_scope: Array.isArray(symptomData.level_scope) ? symptomData.level_scope.join(', ') : '',
        terrain_scope: Array.isArray(symptomData.terrain_scope) ? symptomData.terrain_scope.join(', ') : '',
        style_scope: Array.isArray(symptomData.style_scope) ? symptomData.style_scope.join(', ') : ''
      };
    }
    return {
      name: '',
      category: '',
      synonyms: '',
      level_scope: '',
      terrain_scope: '',
      style_scope: ''
    };
  }

  useEffect(() => {
    setFormData(getInitialFormData(symptom));
  }, [symptom]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!formData.name.trim()) {
      setError('症狀名稱不能為空');
      return;
    }

    // 轉換數據格式
    const symptomData = {
      ...formData,
      synonyms: formData.synonyms.split(',').map(s => s.trim()).filter(s => s),
      level_scope: formData.level_scope.split(',').map(l => l.trim()).filter(l => l),
      terrain_scope: formData.terrain_scope.split(',').map(t => t.trim()).filter(t => t),
      style_scope: formData.style_scope.split(',').map(s => s.trim()).filter(s => s)
    };

    try {
      await onSubmit(symptomData);
    } catch (err) {
      setError(err.message || '操作失敗');
    }
  };

  return (
    <div className="management-page">
      <div className="page-header">
        <h1>{symptom ? '編輯症狀' : '新增症狀'}</h1>
        <p>創建或修改滑雪問題症狀</p>
      </div>

      <form onSubmit={handleSubmit} className="management-form">
        <div className="form-content">
          <div className="form-group">
            <label htmlFor="name">症狀名稱 *</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="例如:重心太後"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="category">類別 *</label>
            <select
              id="category"
              name="category"
              value={formData.category}
              onChange={handleChange}
              required
            >
              <option value="">請選擇</option>
              <option value="技術">技術</option>
              <option value="裝備">裝備</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="synonyms">同義詞 (逗號分隔)</label>
            <input
              type="text"
              id="synonyms"
              name="synonyms"
              value={formData.synonyms}
              onChange={handleChange}
              placeholder="例如:後坐, 重心後移"
            />
          </div>

          <div className="form-group">
            <label htmlFor="level_scope">適用等級範圍 (逗號分隔)</label>
            <input
              type="text"
              id="level_scope"
              name="level_scope"
              value={formData.level_scope}
              onChange={handleChange}
              placeholder="例如:初級, 中級"
            />
          </div>

          <div className="form-group">
            <label htmlFor="terrain_scope">適用地形範圍 (逗號分隔)</label>
            <input
              type="text"
              id="terrain_scope"
              name="terrain_scope"
              value={formData.terrain_scope}
              onChange={handleChange}
              placeholder="例如:綠線, 藍線"
            />
          </div>

          <div className="form-group">
            <label htmlFor="style_scope">適用滑行風格 (逗號分隔)</label>
            <input
              type="text"
              id="style_scope"
              name="style_scope"
              value={formData.style_scope}
              onChange={handleChange}
              placeholder="例如:平花"
            />
          </div>
        </div>

        {error && <div className="error-message">{error}</div>}

        <div className="form-actions">
          <Button type="button" onClick={onCancel} disabled={loading}>
            取消
          </Button>
          <Button type="submit" disabled={loading}>
            {symptom ? '更新症狀' : '創建症狀'}
          </Button>
        </div>
      </form>
    </div>
  );
};

export default SymptomForm;
