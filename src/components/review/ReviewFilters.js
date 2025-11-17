/**
 * 審核篩選和搜索組件
 */
import React from 'react';

const ReviewFilters = ({ filter, searchTerm, onFilterChange, onSearchChange }) => {
  return (
    <div className="review-filters">
      <div className="filter-buttons">
        <button
          className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
          onClick={() => onFilterChange('all')}
        >
          全部
        </button>
        <button
          className={`filter-btn ${filter === 'pending' ? 'active' : ''}`}
          onClick={() => onFilterChange('pending')}
        >
          待審核
        </button>
        <button
          className={`filter-btn ${filter === 'approved' ? 'active' : ''}`}
          onClick={() => onFilterChange('approved')}
        >
          已批准
        </button>
        <button
          className={`filter-btn ${filter === 'rejected' ? 'active' : ''}`}
          onClick={() => onFilterChange('rejected')}
        >
          已拒絕
        </button>
      </div>

      <input
        type="text"
        className="search-input"
        placeholder="搜索症狀或練習..."
        value={searchTerm}
        onChange={(e) => onSearchChange(e.target.value)}
      />
    </div>
  );
};

export default ReviewFilters;
