/**
 * 映射表單組件
 * 處理症狀練習卡映射的創建和編輯
 */
import React from 'react';

const MappingForm = ({
  formData,
  symptoms,
  practiceCards,
  editingMapping,
  onInputChange,
  onSubmit,
  onCancel
}) => {
  return (
    <div className="mapping-form">
      <h2>{editingMapping ? '編輯映射關係' : '新增映射關係'}</h2>

      <form onSubmit={onSubmit} className="form-content">
        <div className="form-group">
          <label htmlFor="symptom_id">症狀 *</label>
          <select
            id="symptom_id"
            name="symptom_id"
            value={formData.symptom_id}
            onChange={onInputChange}
            required
            disabled={!!editingMapping}
          >
            <option value="">請選擇症狀</option>
            {symptoms.map(symptom => (
              <option key={symptom.id} value={symptom.id}>
                {symptom.name} ({symptom.category})
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="practice_id">練習卡 *</label>
          <select
            id="practice_id"
            name="practice_id"
            value={formData.practice_id}
            onChange={onInputChange}
            required
            disabled={!!editingMapping}
          >
            <option value="">請選擇練習卡</option>
            {practiceCards.map(card => (
              <option key={card.id} value={card.id}>
                {card.name} ({card.card_type})
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="order">排序順序</label>
          <input
            type="number"
            id="order"
            name="order"
            value={formData.order}
            onChange={onInputChange}
            min="0"
            placeholder="0"
          />
          <small>數字越小排序越前，0 表示默認排序</small>
        </div>

        <div className="form-actions">
          <button type="submit" className="btn btn-primary">
            {editingMapping ? '更新' : '創建'}
          </button>
          <button
            type="button"
            className="btn btn-secondary"
            onClick={onCancel}
          >
            取消
          </button>
        </div>
      </form>
    </div>
  );
};

export default MappingForm;
