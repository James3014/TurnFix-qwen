/**
 * 管理後台 - 症狀管理標籤
 * 簡潔版本，使用 useSymptoms hook
 */
import React from 'react';
import { useSymptoms } from '../../hooks';

const SymptomsTab = () => {
  const { symptoms, loading, error, deleteSymptom } = useSymptoms();

  const handleDelete = async (id, name) => {
    if (!window.confirm(`確定要刪除症狀「${name}」嗎？`)) return;

    try {
      await deleteSymptom(id);
    } catch (err) {
      alert('刪除失敗：' + err.message);
    }
  };

  if (loading) return <div className="loading">載入中...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="symptoms-tab">
      <div className="tab-header">
        <h2>症狀管理</h2>
        <button className="btn-primary">新增症狀</button>
      </div>

      <div className="data-table">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>症狀名稱</th>
              <th>分類</th>
              <th>同義詞</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            {symptoms.map(symptom => (
              <tr key={symptom.id}>
                <td>{symptom.id}</td>
                <td>{symptom.name}</td>
                <td>{symptom.category}</td>
                <td>{symptom.synonyms?.join(', ') || '-'}</td>
                <td>
                  <button className="btn-edit">編輯</button>
                  <button
                    className="btn-delete"
                    onClick={() => handleDelete(symptom.id, symptom.name)}
                  >
                    刪除
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default SymptomsTab;
