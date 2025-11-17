/**
 * 簡易人工審核 Web 介面 (TOOL-104)
 * 重構：拆分為子組件，提升可維護性
 */
import React, { useState, useMemo } from 'react';
import { useReviewManagement } from '../hooks/useReviewManagement';
import ReviewFilters from './review/ReviewFilters';
import BatchActions from './review/BatchActions';
import KnowledgeSnippetItem from './review/KnowledgeSnippetItem';
import './ReviewInterface.css';

const ReviewInterface = () => {
  const {
    snippets,
    loading,
    approveSnippet,
    rejectSnippet,
    batchApprove,
    batchReject
  } = useReviewManagement();

  const [selectedSnippets, setSelectedSnippets] = useState(new Set());
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  // 篩選和搜索
  const filteredSnippets = useMemo(() => {
    return snippets.filter(snippet => {
      const matchesFilter = filter === 'all' || snippet.review_status === filter;
      const matchesSearch = !searchTerm ||
        snippet.symptom.toLowerCase().includes(searchTerm.toLowerCase()) ||
        snippet.practice_tips.some(tip => tip.toLowerCase().includes(searchTerm.toLowerCase()));
      return matchesFilter && matchesSearch;
    });
  }, [snippets, filter, searchTerm]);

  const handleSelect = (id) => {
    setSelectedSnippets(prev => {
      const newSet = new Set(prev);
      if (newSet.has(id)) {
        newSet.delete(id);
      } else {
        newSet.add(id);
      }
      return newSet;
    });
  };

  const handleSelectAll = () => {
    setSelectedSnippets(new Set(filteredSnippets.map(s => s.id)));
  };

  const handleDeselectAll = () => {
    setSelectedSnippets(new Set());
  };

  const handleBatchApprove = () => {
    if (window.confirm(`確定要批准 ${selectedSnippets.size} 個項目嗎？`)) {
      batchApprove(selectedSnippets);
      setSelectedSnippets(new Set());
    }
  };

  const handleBatchReject = () => {
    if (window.confirm(`確定要拒絕 ${selectedSnippets.size} 個項目嗎？`)) {
      batchReject(selectedSnippets);
      setSelectedSnippets(new Set());
    }
  };

  const handleEdit = (snippet) => {
    // TODO: 實現編輯功能
    console.log('Edit snippet:', snippet);
  };

  if (loading) return <div className="loading">載入中...</div>;

  return (
    <div className="review-interface">
      <h1>知識審核介面</h1>

      <ReviewFilters
        filter={filter}
        searchTerm={searchTerm}
        onFilterChange={setFilter}
        onSearchChange={setSearchTerm}
      />

      <BatchActions
        selectedCount={selectedSnippets.size}
        onBatchApprove={handleBatchApprove}
        onBatchReject={handleBatchReject}
        onSelectAll={handleSelectAll}
        onDeselectAll={handleDeselectAll}
      />

      <div className="snippets-list">
        {filteredSnippets.length === 0 ? (
          <p className="empty-message">沒有符合條件的項目</p>
        ) : (
          filteredSnippets.map(snippet => (
            <KnowledgeSnippetItem
              key={snippet.id}
              snippet={snippet}
              isSelected={selectedSnippets.has(snippet.id)}
              onSelect={handleSelect}
              onApprove={approveSnippet}
              onReject={rejectSnippet}
              onEdit={handleEdit}
            />
          ))
        )}
      </div>

      <div className="review-summary">
        <p>總計: {snippets.length} 項</p>
        <p>待審核: {snippets.filter(s => s.review_status === 'pending').length} 項</p>
        <p>已批准: {snippets.filter(s => s.review_status === 'approved').length} 項</p>
        <p>已拒絕: {snippets.filter(s => s.review_status === 'rejected').length} 項</p>
      </div>
    </div>
  );
};

export default ReviewInterface;
