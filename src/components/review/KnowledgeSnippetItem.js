/**
 * 知識片段項組件
 */
import React from 'react';

const KnowledgeSnippetItem = ({ snippet, isSelected, onSelect, onApprove, onReject, onEdit }) => {
  return (
    <div className={`snippet-card ${snippet.review_status}`}>
      <div className="snippet-header">
        <input
          type="checkbox"
          checked={isSelected}
          onChange={() => onSelect(snippet.id)}
        />
        <h3>{snippet.symptom}</h3>
        <span className={`status-badge ${snippet.review_status}`}>
          {snippet.review_status === 'pending' ? '待審核' :
           snippet.review_status === 'approved' ? '已批准' : '已拒絕'}
        </span>
        <span className="confidence-badge">
          置信度: {(snippet.confidence * 100).toFixed(0)}%
        </span>
      </div>

      <div className="snippet-content">
        <div className="field">
          <strong>練習要點:</strong>
          <ul>
            {snippet.practice_tips.map((tip, idx) => (
              <li key={idx}>{tip}</li>
            ))}
          </ul>
        </div>

        <div className="field">
          <strong>常見錯誤:</strong>
          <ul>
            {snippet.pitfalls.map((pitfall, idx) => (
              <li key={idx}>{pitfall}</li>
            ))}
          </ul>
        </div>

        <div className="field">
          <strong>建議劑量:</strong> {snippet.dosage}
        </div>

        <div className="field source-text">
          <strong>原始片段:</strong>
          <p>{snippet.source_snippet}</p>
        </div>
      </div>

      <div className="snippet-actions">
        <button
          className="btn btn-sm btn-edit"
          onClick={() => onEdit(snippet)}
        >
          編輯
        </button>
        <button
          className="btn btn-sm btn-approve"
          onClick={() => onApprove(snippet.id)}
          disabled={snippet.review_status === 'approved'}
        >
          批准
        </button>
        <button
          className="btn btn-sm btn-reject"
          onClick={() => onReject(snippet.id)}
          disabled={snippet.review_status === 'rejected'}
        >
          拒絕
        </button>
      </div>
    </div>
  );
};

export default KnowledgeSnippetItem;
