/**
 * SymptomList 組件
 *
 * 顯示症狀列表並提供編輯/刪除操作
 * 遵循 Linus 原則:簡單、清晰、單一職責
 */
import React from 'react';
import Button from '../common/Button';

const SymptomList = ({ symptoms, onEdit, onDelete, onAdd }) => {
  const handleDelete = async (symptomId, symptomName) => {
    if (!window.confirm(`確定要刪除「${symptomName}」嗎?`)) {
      return;
    }
    await onDelete(symptomId);
  };

  return (
    <div className="management-page">
      <div className="list-header">
        <h1>症狀管理</h1>
        <p>管理滑雪問題症狀庫</p>
        <Button onClick={onAdd}>
          + 新增症狀
        </Button>
      </div>

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>名稱</th>
              <th>類別</th>
              <th>同義詞數量</th>
              <th>等級範圍</th>
              <th>地形範圍</th>
              <th>滑行風格</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            {symptoms.length === 0 ? (
              <tr>
                <td colSpan="8" style={{ textAlign: 'center', padding: '2rem' }}>
                  暫無症狀數據
                </td>
              </tr>
            ) : (
              symptoms.map(symptom => (
                <tr key={symptom.id}>
                  <td>{symptom.id}</td>
                  <td>{symptom.name}</td>
                  <td>{symptom.category}</td>
                  <td>{Array.isArray(symptom.synonyms) ? symptom.synonyms.length : 0}</td>
                  <td>{Array.isArray(symptom.level_scope) ? symptom.level_scope.join(', ') : symptom.level_scope}</td>
                  <td>{Array.isArray(symptom.terrain_scope) ? symptom.terrain_scope.join(', ') : symptom.terrain_scope}</td>
                  <td>{Array.isArray(symptom.style_scope) ? symptom.style_scope.join(', ') : symptom.style_scope}</td>
                  <td>
                    <button
                      className="action-button edit"
                      onClick={() => onEdit(symptom)}
                    >
                      編輯
                    </button>
                    <button
                      className="action-button delete"
                      onClick={() => handleDelete(symptom.id, symptom.name)}
                    >
                      刪除
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default SymptomList;
