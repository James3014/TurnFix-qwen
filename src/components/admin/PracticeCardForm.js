/**
 * PracticeCardForm 組件
 *
 * 練習卡創建/編輯表單
 * 遵循 Linus 原則:簡單、清晰、單一職責
 */
import React, { useState, useEffect } from 'react';
import Button from '../common/Button';

const PracticeCardForm = ({
  card,
  onSubmit,
  onCancel,
  loading
}) => {
  const [formData, setFormData] = useState(getInitialFormData());
  const [error, setError] = useState('');

  // 初始化表單數據
  function getInitialFormData(cardData = null) {
    if (cardData) {
      return {
        name: cardData.name || '',
        goal: cardData.goal || '',
        tips: Array.isArray(cardData.tips) ? cardData.tips.join(', ') : '',
        pitfalls: cardData.pitfalls || '',
        dosage: cardData.dosage || '',
        level: Array.isArray(cardData.level) ? cardData.level.join(', ') : '',
        terrain: Array.isArray(cardData.terrain) ? cardData.terrain.join(', ') : '',
        self_check: Array.isArray(cardData.self_check) ? cardData.self_check.join(', ') : '',
        card_type: cardData.card_type || ''
      };
    }
    return {
      name: '',
      goal: '',
      tips: '',
      pitfalls: '',
      dosage: '',
      level: '',
      terrain: '',
      self_check: '',
      card_type: ''
    };
  }

  // 當編輯的卡片變化時,更新表單數據
  useEffect(() => {
    setFormData(getInitialFormData(card));
  }, [card]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // 驗證
    if (!formData.name.trim() || !formData.goal.trim()) {
      setError('練習卡名稱和目標不能為空');
      return;
    }

    // 轉換數據格式
    const cardData = {
      ...formData,
      tips: formData.tips.split(',').map(t => t.trim()).filter(t => t),
      level: formData.level.split(',').map(l => l.trim()).filter(l => l),
      terrain: formData.terrain.split(',').map(t => t.trim()).filter(t => t),
      self_check: formData.self_check.split(',').map(s => s.trim()).filter(s => s)
    };

    try {
      await onSubmit(cardData);
    } catch (err) {
      setError(err.message || '操作失敗');
    }
  };

  return (
    <div className="management-page">
      <div className="page-header">
        <h1>{card ? '編輯練習卡' : '新增練習卡'}</h1>
        <p>創建或修改滑雪練習建議卡</p>
      </div>

      <form onSubmit={handleSubmit} className="management-form">
        <div className="form-content">
          <div className="form-group">
            <label htmlFor="name">練習卡名稱 *</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="例如:J型轉彎練習"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="goal">練習目標 *</label>
            <textarea
              id="goal"
              name="goal"
              value={formData.goal}
              onChange={handleChange}
              placeholder="例如:完成外腳承重再過中立"
              rows={3}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="tips">練習要點 (逗號分隔)</label>
            <input
              type="text"
              id="tips"
              name="tips"
              value={formData.tips}
              onChange={handleChange}
              placeholder="例如:視線外緣, 外腳 70–80%, 中立後換刃"
            />
          </div>

          <div className="form-group">
            <label htmlFor="pitfalls">常見錯誤修正</label>
            <textarea
              id="pitfalls"
              name="pitfalls"
              value={formData.pitfalls}
              onChange={handleChange}
              placeholder="例如:避免提前壓內腳"
              rows={2}
            />
          </div>

          <div className="form-group">
            <label htmlFor="dosage">建議次數/時長</label>
            <input
              type="text"
              id="dosage"
              name="dosage"
              value={formData.dosage}
              onChange={handleChange}
              placeholder="例如:藍線 6 次/趟 ×3 趟"
            />
          </div>

          <div className="form-group">
            <label htmlFor="level">適用等級 (逗號分隔)</label>
            <input
              type="text"
              id="level"
              name="level"
              value={formData.level}
              onChange={handleChange}
              placeholder="例如:初級, 中級"
            />
          </div>

          <div className="form-group">
            <label htmlFor="terrain">適用地形 (逗號分隔)</label>
            <input
              type="text"
              id="terrain"
              name="terrain"
              value={formData.terrain}
              onChange={handleChange}
              placeholder="例如:綠線, 藍線"
            />
          </div>

          <div className="form-group">
            <label htmlFor="self_check">自我檢查點 (逗號分隔)</label>
            <input
              type="text"
              id="self_check"
              name="self_check"
              value={formData.self_check}
              onChange={handleChange}
              placeholder="例如:是否在換刃前感到外腳壓力峰值?"
            />
          </div>

          <div className="form-group">
            <label htmlFor="card_type">練習卡類型</label>
            <select
              id="card_type"
              name="card_type"
              value={formData.card_type}
              onChange={handleChange}
            >
              <option value="">請選擇</option>
              <option value="技術">技術</option>
              <option value="基礎">基礎</option>
              <option value="進階">進階</option>
            </select>
          </div>
        </div>

        {error && <div className="error-message">{error}</div>}

        <div className="form-actions">
          <Button type="button" onClick={onCancel} disabled={loading}>
            取消
          </Button>
          <Button type="submit" disabled={loading}>
            {card ? '更新練習卡' : '創建練習卡'}
          </Button>
        </div>
      </form>
    </div>
  );
};

export default PracticeCardForm;
