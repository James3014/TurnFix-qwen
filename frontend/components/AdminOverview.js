/**
 * 管理後台儀表板組件 (UI-308.0)
 * 
 * 提供管理者後台的統計資訊和快速操作
 */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/AdminDashboard.css';

const AdminOverview = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState({
    totalSymptoms: 0,
    totalPracticeCards: 0,
    totalSessions: 0,
    totalFeedback: 0,
    avgRating: 0
  });
  const [loading, setLoading] = useState(true);

  // 模擬數據 - 實際實現中會從API獲取
  useEffect(() => {
    const mockStats = {
      totalSymptoms: 15,
      totalPracticeCards: 42,
      totalSessions: 128,
      totalFeedback: 86,
      avgRating: 4.2
    };
    
    setStats(mockStats);
    setLoading(false);
  }, []);

  const quickActions = [
    {
      icon: '🩺',
      label: '管理症狀',
      path: '/admin/symptoms',
      description: '新增、編輯、刪除症狀種子'
    },
    {
      icon: '📋',
      label: '管理練習卡',
      path: '/admin/practice-cards',
      description: '新增、編輯、刪除練習建議卡'
    },
    {
      icon: '🔗',
      label: '管理映射關係',
      path: '/admin/mappings',
      description: '維護症狀與練習卡的關聯'
    },
    {
      icon: '📊',
      label: '查看回饋分析',
      path: '/admin/analytics',
      description: '查看用戶回饋統計與分析'
    }
  ];

  if (loading) {
    return (
      <div className="management-page">
        <div className="loading">載入中...</div>
      </div>
    );
  }

  return (
    <div className="management-page admin-overview">
      <div className="dashboard-header">
        <h1>🔧 管理後台儀表板</h1>
        <p>系統概覽與快速操作</p>
      </div>
      
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">🩺</div>
          <div className="stat-content">
            <div className="stat-value">{stats.totalSymptoms}</div>
            <div className="stat-label">總症狀數</div>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">📋</div>
          <div className="stat-content">
            <div className="stat-value">{stats.totalPracticeCards}</div>
            <div className="stat-label">總練習卡數</div>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">👥</div>
          <div className="stat-content">
            <div className="stat-value">{stats.totalSessions}</div>
            <div className="stat-label">總會話數</div>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">⭐</div>
          <div className="stat-content">
            <div className="stat-value">{stats.avgRating.toFixed(1)}</div>
            <div className="stat-label">平均評分</div>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">💬</div>
          <div className="stat-content">
            <div className="stat-value">{stats.totalFeedback}</div>
            <div className="stat-label">總回饋數</div>
          </div>
        </div>
      </div>
      
      <div className="quick-actions">
        <h2>快速操作</h2>
        <div className="actions-grid">
          {quickActions.map((action, index) => (
            <button
              key={index}
              className="action-card"
              onClick={() => navigate(action.path)}
            >
              <div className="action-icon">{action.icon}</div>
              <div className="action-label">{action.label}</div>
              <div className="action-description">{action.description}</div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AdminOverview;