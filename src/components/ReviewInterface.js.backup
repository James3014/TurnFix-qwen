/**
 * 簡易人工審核 Web 介面 (TOOL-104)
 * 
 * 展示待審核的知識片段（症狀與練習建議）
 * 支援修改和確認（允許管理者調整自動抽取的結果）
 * 支援批量操作（批准多個片段、標記為不適用等）
 */
import React, { useState, useEffect } from 'react';
import './ReviewInterface.css';

const ReviewInterface = () => {
  const [knowledgeSnippets, setKnowledgeSnippets] = useState([]);
  const [filteredSnippets, setFilteredSnippets] = useState([]);
  const [selectedSnippets, setSelectedSnippets] = useState(new Set());
  const [filter, setFilter] = useState('all'); // all, pending, approved, rejected
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);

  // 模擬從API獲取待審核項目
  useEffect(() => {
    const fetchKnowledgeSnippets = async () => {
      try {
        // 在實際實現中，這裡會從API獲取數據
        // 模擬數據：
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
            practice_tips: ['控制速度', '保持平衡'],
            pitfalls: ['避免急轉', '不要過度傾斜'],
            dosage: '平緩斜坡8次',
            source_snippet: '轉彎時不穩定主要因為重心控制不佳...',
            review_status: 'pending',
            confidence: 0.68,
            original_text: '轉彎不穩是初學者常見問題...'
          }
        ];
        
        setKnowledgeSnippets(mockData);
        setFilteredSnippets(mockData);
        setLoading(false);
      } catch (error) {
        console.error('獲取知識片段失敗:', error);
        setLoading(false);
      }
    };

    fetchKnowledgeSnippets();
  }, []);

  // 根據篩選條件和搜索詞更新顯示的片段
  useEffect(() => {
    let result = knowledgeSnippets;

    // 應用狀態篩選
    if (filter !== 'all') {
      result = result.filter(snippet => snippet.review_status === filter);
    }

    // 應用搜索篩選
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      result = result.filter(snippet => 
        snippet.symptom.toLowerCase().includes(term) ||
        snippet.source_snippet.toLowerCase().includes(term) ||
        snippet.original_text.toLowerCase().includes(term)
      );
    }

    setFilteredSnippets(result);
  }, [filter, searchTerm, knowledgeSnippets]);

  const toggleSnippetSelection = (id) => {
    const newSelected = new Set(selectedSnippets);
    if (newSelected.has(id)) {
      newSelected.delete(id);
    } else {
      newSelected.add(id);
    }
    setSelectedSnippets(newSelected);
  };

  const toggleSelectAll = () => {
    if (selectedSnippets.size === filteredSnippets.length) {
      setSelectedSnippets(new Set());
    } else {
      setSelectedSnippets(new Set(filteredSnippets.map(s => s.id)));
    }
  };

  const updateSnippetStatus = (id, status) => {
    setKnowledgeSnippets(prev => 
      prev.map(snippet => 
        snippet.id === id 
          ? { ...snippet, review_status: status } 
          : snippet
      )
    );
  };

  const updateSelectedSnippetsStatus = (status) => {
    setKnowledgeSnippets(prev => 
      prev.map(snippet => 
        selectedSnippets.has(snippet.id) 
          ? { ...snippet, review_status: status } 
          : snippet
      )
    );
    setSelectedSnippets(new Set());
  };

  const saveChanges = async () => {
    try {
      // 在實際實現中，這裡會向API發送更新請求
      console.log('保存審核結果到服務器:', knowledgeSnippets);
      alert('審核結果已保存！');
    } catch (error) {
      console.error('保存審核結果失敗:', error);
      alert('保存失敗，請重試');
    }
  };

  if (loading) {
    return <div className="review-interface-loading">載入中...</div>;
  }

  return (
    <div className="review-interface">
      <h1>知識片段人工審核</h1>
      
      <div className="review-controls">
        <div className="search-filter">
          <input
            type="text"
            placeholder="搜索症狀或內容..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
          <select 
            value={filter} 
            onChange={(e) => setFilter(e.target.value)}
            className="filter-select"
          >
            <option value="all">全部狀態</option>
            <option value="pending">待審核</option>
            <option value="approved">已批准</option>
            <option value="rejected">已拒絕</option>
          </select>
        </div>
        
        <div className="batch-actions">
          <button 
            onClick={() => updateSelectedSnippetsStatus('approved')}
            disabled={selectedSnippets.size === 0}
            className="btn-approve"
          >
            批准選中
          </button>
          <button 
            onClick={() => updateSelectedSnippetsStatus('rejected')}
            disabled={selectedSnippets.size === 0}
            className="btn-reject"
          >
            拒絕選中
          </button>
          <button 
            onClick={saveChanges}
            className="btn-save"
          >
            保存更改
          </button>
        </div>
      </div>
      
      <div className="review-stats">
        <span>總數: {knowledgeSnippets.length} | </span>
        <span>待審核: {knowledgeSnippets.filter(s => s.review_status === 'pending').length} | </span>
        <span>已選中: {selectedSnippets.size}</span>
      </div>
      
      <div className="review-list">
        {filteredSnippets.length === 0 ? (
          <div className="no-results">沒有找到符合條件的知識片段</div>
        ) : (
          filteredSnippets.map(snippet => (
            <div 
              key={snippet.id} 
              className={`review-item ${snippet.review_status} ${selectedSnippets.has(snippet.id) ? 'selected' : ''}`}
            >
              <div className="selection-control">
                <input
                  type="checkbox"
                  checked={selectedSnippets.has(snippet.id)}
                  onChange={() => toggleSnippetSelection(snippet.id)}
                />
              </div>
              
              <div className="content">
                <div className="header">
                  <h3>{snippet.symptom}</h3>
                  <div className="meta">
                    <span className="confidence">置信度: {(snippet.confidence * 100).toFixed(1)}%</span>
                    <span className={`status status-${snippet.review_status}`}>
                      {snippet.review_status === 'pending' && '待審核'}
                      {snippet.review_status === 'approved' && '已批准'}
                      {snippet.review_status === 'rejected' && '已拒絕'}
                    </span>
                  </div>
                </div>
                
                <div className="details">
                  <div className="tips-section">
                    <h4>練習要點:</h4>
                    <ul>
                      {snippet.practice_tips.map((tip, idx) => (
                        <li key={idx}>{tip}</li>
                      ))}
                    </ul>
                  </div>
                  
                  <div className="pitfalls-section">
                    <h4>常見錯誤:</h4>
                    <ul>
                      {snippet.pitfalls.map((pitfall, idx) => (
                        <li key={idx}>{pitfall}</li>
                      ))}
                    </ul>
                  </div>
                  
                  <div className="dosage-section">
                    <h4>建議次數:</h4>
                    <p>{snippet.dosage}</p>
                  </div>
                  
                  <div className="source-section">
                    <h4>來源片段:</h4>
                    <p>{snippet.source_snippet}</p>
                  </div>
                </div>
                
                <div className="actions">
                  <button 
                    onClick={() => updateSnippetStatus(snippet.id, 'approved')}
                    className="btn-sm btn-approve"
                  >
                    批准
                  </button>
                  <button 
                    onClick={() => updateSnippetStatus(snippet.id, 'rejected')}
                    className="btn-sm btn-reject"
                  >
                    拒絕
                  </button>
                  <button 
                    onClick={() => updateSnippetStatus(snippet.id, 'pending')}
                    className="btn-sm btn-pending"
                  >
                    重置
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
      
      {filteredSnippets.length > 0 && (
        <div className="select-all-bar">
          <label>
            <input
              type="checkbox"
              checked={selectedSnippets.size === filteredSnippets.length}
              onChange={toggleSelectAll}
            />
            選擇全部顯示項目 ({filteredSnippets.length})
          </label>
        </div>
      )}
    </div>
  );
};

export default ReviewInterface;