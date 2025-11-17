/**
 * 映射列表組件
 * 顯示症狀練習卡映射關係列表
 */
import React from 'react';

const MappingList = ({ mappings, onEdit, onDelete }) => {
  // 按症狀分組
  const groupedMappings = mappings.reduce((acc, mapping) => {
    const key = `${mapping.symptom_id}-${mapping.symptom_name}`;
    if (!acc[key]) {
      acc[key] = {
        symptom_id: mapping.symptom_id,
        symptom_name: mapping.symptom_name,
        practices: []
      };
    }
    acc[key].practices.push(mapping);
    return acc;
  }, {});

  return (
    <div className="mapping-list">
      <h2>映射關係列表</h2>

      {Object.values(groupedMappings).length === 0 ? (
        <p className="empty-message">目前沒有任何映射關係</p>
      ) : (
        Object.values(groupedMappings).map((group) => (
          <div key={group.symptom_id} className="mapping-group">
            <h3>{group.symptom_name}</h3>
            <table className="data-table">
              <thead>
                <tr>
                  <th>練習卡名稱</th>
                  <th>排序</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                {group.practices
                  .sort((a, b) => a.order - b.order)
                  .map((mapping) => (
                    <tr key={`${mapping.symptom_id}-${mapping.practice_id}`}>
                      <td>{mapping.practice_name}</td>
                      <td>{mapping.order || '-'}</td>
                      <td className="actions">
                        <button
                          className="btn btn-sm btn-edit"
                          onClick={() => onEdit(mapping)}
                        >
                          編輯
                        </button>
                        <button
                          className="btn btn-sm btn-delete"
                          onClick={() => onDelete(mapping.symptom_id, mapping.practice_id)}
                        >
                          刪除
                        </button>
                      </td>
                    </tr>
                  ))}
              </tbody>
            </table>
          </div>
        ))
      )}
    </div>
  );
};

export default MappingList;
