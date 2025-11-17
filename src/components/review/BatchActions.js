/**
 * 批量操作工具欄組件
 */
import React from 'react';

const BatchActions = ({ selectedCount, onBatchApprove, onBatchReject, onSelectAll, onDeselectAll }) => {
  return (
    <div className="batch-actions">
      <span className="selection-info">已選擇 {selectedCount} 項</span>

      <div className="action-buttons">
        <button
          className="btn btn-sm"
          onClick={onSelectAll}
        >
          全選
        </button>
        <button
          className="btn btn-sm"
          onClick={onDeselectAll}
        >
          取消選擇
        </button>
        <button
          className="btn btn-sm btn-approve"
          onClick={onBatchApprove}
          disabled={selectedCount === 0}
        >
          批量批准
        </button>
        <button
          className="btn btn-sm btn-reject"
          onClick={onBatchReject}
          disabled={selectedCount === 0}
        >
          批量拒絕
        </button>
      </div>
    </div>
  );
};

export default BatchActions;
