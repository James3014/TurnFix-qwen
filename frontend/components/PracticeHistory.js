/**
 * 練習歷史頁面 (UI-305)
 * 
 * 設計並實作練習歷史頁面
 */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/PracticeHistory.css';

const PracticeHistory = () => {
  const navigate = useNavigate();
  const [sessions, setSessions] = useState([]);
  const [filteredSessions, setFilteredSessions] = useState([]);
  const [filters, setFilters] = useState({
    dateRange: 'all',
    level: '',
    terrain: '',
    symptom: ''
  });
  const [loading, setLoading] = useState(true);

  // 模擬數據 - 實際實現中會從API獲取
  useEffect(() => {
    const mockSessions = [
      {
        id: 1,
        date: '2025-10-28',
        input_text: '轉彎會後坐',
        level: '初級',
        terrain: '綠線',
        symptom: '重心太後',
        card_count: 3,
        feedback_rating: 'applicable'
      },
      {
        id: 2,
        date: '2025-10-25',
        input_text: '換刃不順',
        level: '中級',
        terrain: '藍線',
        symptom: '換刃困難',
        card_count: 4,
        feedback_rating: 'partially_applicable'
      },
      {
        id: 3,
        date: '2025-10-20',
        input_text: '重心不穩',
        level: '初級',
        terrain: '綠線',
        symptom: '重心不穩',
        card_count: 5,
        feedback_rating: 'applicable'
      }
    ];
    
    setSessions(mockSessions);
    setFilteredSessions(mockSessions);
    setLoading(false);
  }, []);

  const handleFilterChange = (filterName, value) => {
    const newFilters = { ...filters, [filterName]: value };
    setFilters(newFilters);
    
    // 應用篩選
    let filtered = [...sessions];
    
    if (newFilters.level) {
      filtered = filtered.filter(session => session.level === newFilters.level);
    }
    
    if (newFilters.terrain) {
      filtered = filtered.filter(session => session.terrain === newFilters.terrain);
    }
    
    if (newFilters.symptom) {
      filtered = filtered.filter(session => session.symptom.includes(newFilters.symptom));
    }
    
    // 日期篩選
    if (newFilters.dateRange !== 'all') {
      const now = new Date();
      const cutoffDate = new Date(now);
      
      switch (newFilters.dateRange) {
        case '7days':
          cutoffDate.setDate(now.getDate() - 7);
          break;
        case '30days':
          cutoffDate.setDate(now.getDate() - 30);
          break;
        case '90days':
          cutoffDate.setDate(now.getDate() - 90);
          break;
        default:
          break;
      }
      
      filtered = filtered.filter(session => new Date(session.date) >= cutoffDate);
    }
    
    setFilteredSessions(filtered);
  };

  const viewSessionDetails = (sessionId) => {
    // 導向會話詳細頁面
    navigate(`/history/${sessionId}`);
  };

  const getFeedbackIcon = (rating) => {
    switch (rating) {
      case 'not_applicable':
        return '❌';
      case 'partially_applicable':
        return '△';
      case 'applicable':
        return '✓';
      default:
        return '';
    }
  };

  if (loading) {
    return (
      <div className="practice-history">
        <div className="loading">載入中...</div>
      </div>
    );
  }

  return (
    <div className="practice-history">
      <div className="page-header">
        <h1>練習歷史</h1>
      </div>
      
      <div className="filters-section">
        <h2>篩選條件</h2>
        <div className="filters">
          <div className="filter-group">
            <label htmlFor="date-range">日期範圍：</label>
            <select
              id="date-range"
              value={filters.dateRange}
              onChange={(e) => handleFilterChange('dateRange', e.target.value)}
            >
              <option value="all">全部</option>
              <option value="7days">最近 7 天</option>
              <option value="30days">最近 30 天</option>
              <option value="90days">最近 90 天</option>
            </select>
          </div>
          
          <div className="filter-group">
            <label htmlFor="level-filter">等級：</label>
            <select
              id="level-filter"
              value={filters.level}
              onChange={(e) => handleFilterChange('level', e.target.value)}
            >
              <option value="">全部</option>
              <option value="初級">初級</option>
              <option value="中級">中級</option>
              <option value="高級">高級</option>
            </select>
          </div>
          
          <div className="filter-group">
            <label htmlFor="terrain-filter">地形：</label>
            <select
              id="terrain-filter"
              value={filters.terrain}
              onChange={(e) => handleFilterChange('terrain', e.target.value)}
            >
              <option value="">全部</option>
              <option value="綠線">綠線</option>
              <option value="藍線">藍線</option>
              <option value="黑線">黑線</option>
              <option value="雙黑線">雙黑線</option>
            </select>
          </div>
          
          <div className="filter-group">
            <label htmlFor="symptom-filter">症狀：</label>
            <input
              id="symptom-filter"
              type="text"
              placeholder="搜尋症狀..."
              value={filters.symptom}
              onChange={(e) => handleFilterChange('symptom', e.target.value)}
            />
          </div>
        </div>
      </div>
      
      <div className="sessions-section">
        <h2>歷史記錄 ({filteredSessions.length} 筆)</h2>
        
        {filteredSessions.length === 0 ? (
          <div className="no-sessions">
            <p>沒有找到符合條件的練習記錄</p>
          </div>
        ) : (
          <div className="sessions-list">
            {filteredSessions.map(session => (
              <div key={session.id} className="session-card">
                <div className="session-header">
                  <div className="session-date">{session.date}</div>
                  <div className="session-rating">
                    {getFeedbackIcon(session.feedback_rating)}
                  </div>
                </div>
                
                <div className="session-content">
                  <div className="session-info">
                    <div className="info-item">
                      <strong>問題：</strong>
                      <span>{session.input_text}</span>
                    </div>
                    <div className="info-item">
                      <strong>症狀：</strong>
                      <span>{session.symptom}</span>
                    </div>
                    <div className="info-item">
                      <strong>條件：</strong>
                      <span>{session.level} / {session.terrain}</span>
                    </div>
                  </div>
                  
                  <div className="session-stats">
                    <div className="stat-item">
                      <strong>推薦卡片：</strong>
                      <span>{session.card_count} 張</span>
                    </div>
                  </div>
                </div>
                
                <div className="session-actions">
                  <button 
                    className="view-details-btn"
                    onClick={() => viewSessionDetails(session.id)}
                  >
                    查看詳細
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default PracticeHistory;