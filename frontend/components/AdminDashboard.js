/**
 * 管理者後台組件 (UI-308)
 * 
 * 設計並實作管理者後台介面
 */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/AdminDashboard.css';

const AdminDashboard = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('overview');
  const [stats, setStats] = useState({
    totalSymptoms: 0,
    totalPracticeCards: 0,
    totalSessions: 0,
    totalFeedback: 0,
    avgRating: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

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

  const renderOverviewTab = () => (
    <div className="overview-tab">
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
            <div className="stat-label">平均星數</div>
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
          <button 
            className="action-card"
            onClick={() => navigate('/admin/symptoms')}
          >
            <div className="action-icon">🩺</div>
            <div className="action-label">管理症狀</div>
          </button>
          
          <button 
            className="action-card"
            onClick={() => navigate('/admin/practice-cards')}
          >
            <div className="action-icon">📋</div>
            <div className="action-label">管理練習卡</div>
          </button>
          
          <button 
            className="action-card"
            onClick={() => navigate('/admin/mappings')}
          >
            <div className="action-icon">🔗</div>
            <div className="action-label">管理映射關係</div>
          </button>
          
          <button 
            className="action-card"
            onClick={() => navigate('/admin/analytics')}
          >
            <div className="action-icon">📊</div>
            <div className="action-label">查看回饋分析</div>
          </button>
        </div>
      </div>
    </div>
  );

  const renderSymptomsTab = () => (
    <div className="symptoms-tab">
      <div className="tab-header">
        <h2>🩺 症狀管理 (API-205.1)</h2>
        <p>提供 CRUD 接口用於管理症狀種子</p>
        <button 
          className="add-button"
          onClick={() => navigate('/admin/symptoms/new')}
        >
          + 新增症狀
        </button>
      </div>
      
      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>名稱</th>
              <th>類別</th>
              <th>同義詞數量</th>
              <th>關聯練習卡</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>1</td>
              <td>重心太後</td>
              <td>技術</td>
              <td>3</td>
              <td>5</td>
              <td>
                <button className="action-button edit">編輯</button>
                <button className="action-button delete">刪除</button>
              </td>
            </tr>
            <tr>
              <td>2</td>
              <td>重心不穩</td>
              <td>技術</td>
              <td>2</td>
              <td>4</td>
              <td>
                <button className="action-button edit">編輯</button>
                <button className="action-button delete">刪除</button>
              </td>
            </tr>
            <tr>
              <td>3</td>
              <td>換刃困難</td>
              <td>技術</td>
              <td>4</td>
              <td>3</td>
              <td>
                <button className="action-button edit">編輯</button>
                <button className="action-button delete">刪除</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );

  const renderPracticeCardsTab = () => (
    <div className="practice-cards-tab">
      <div className="tab-header">
        <h2>📋 練習卡管理 (API-205.2)</h2>
        <p>提供 CRUD 接口用於管理練習卡</p>
        <button 
          className="add-button"
          onClick={() => navigate('/admin/practice-cards/new')}
        >
          + 新增練習卡
        </button>
      </div>
      
      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>名稱</th>
              <th>類型</th>
              <th>適用等級</th>
              <th>適用地形</th>
              <th>關聯症狀</th>
              <th>平均評分</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>101</td>
              <td>J型轉彎練習</td>
              <td>技術</td>
              <td>初級, 中級</td>
              <td>綠線, 藍線</td>
              <td>2</td>
              <td>4.5</td>
              <td>
                <button className="action-button edit">編輯</button>
                <button className="action-button delete">刪除</button>
              </td>
            </tr>
            <tr>
              <td>102</td>
              <td>重心轉移練習</td>
              <td>基礎</td>
              <td>初級, 中級</td>
              <td>綠線</td>
              <td>1</td>
              <td>4.2</td>
              <td>
                <button className="action-button edit">編輯</button>
                <button className="action-button delete">刪除</button>
              </td>
            </tr>
            <tr>
              <td>201</td>
              <td>基礎滑行練習</td>
              <td>基礎</td>
              <td>初級</td>
              <td>綠線</td>
              <td>3</td>
              <td>4.0</td>
              <td>
                <button className="action-button edit">編輯</button>
                <button className="action-button delete">刪除</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );

  const renderMappingsTab = () => (
    <div className="mappings-tab">
      <div className="tab-header">
        <h2>🔗 症狀↔練習卡映射管理 (API-205.3)</h2>
        <p>提供接口管理症狀↔練習卡的關聯</p>
        <button 
          className="add-button"
          onClick={() => navigate('/admin/mappings/new')}
        >
          + 新增映射
        </button>
      </div>
      
      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>症狀ID</th>
              <th>症狀名稱</th>
              <th>練習卡ID</th>
              <th>練習卡名稱</th>
              <th>排序</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>1</td>
              <td>重心太後</td>
              <td>101</td>
              <td>J型轉彎練習</td>
              <td>1</td>
              <td>
                <button className="action-button edit">編輯</button>
                <button className="action-button delete">刪除</button>
              </td>
            </tr>
            <tr>
              <td>1</td>
              <td>重心太後</td>
              <td>102</td>
              <td>重心轉移練習</td>
              <td>2</td>
              <td>
                <button className="action-button edit">編輯</button>
                <button className="action-button delete">刪除</button>
              </td>
            </tr>
            <tr>
              <td>2</td>
              <td>重心不穩</td>
              <td>201</td>
              <td>基礎滑行練習</td>
              <td>1</td>
              <td>
                <button className="action-button edit">編輯</button>
                <button className="action-button delete">刪除</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );

  const renderFeedbackTab = () => (
    <div className="feedback-tab">
      <div className="tab-header">
        <h2>📊 回饋分析 (API-207)</h2>
        <p>查看用戶反饋統計與分析</p>
      </div>
      
      <div className="analytics-sections">
        <div className="analytics-card">
          <h3>會話層級回饋分布 (API-207.1)</h3>
          <div className="chart-placeholder">
            <p>📊 會話層級回饋分布圖表</p>
            <div className="distribution-bars">
              <div className="bar">
                <div 
                  className="bar-fill" 
                  style={{height: `${(stats.totalFeedback * 0.3) / stats.totalFeedback * 100}%`}}
                ></div>
                <div className="bar-label">❌ 不適用 ({Math.floor(stats.totalFeedback * 0.3)})</div>
              </div>
              <div className="bar">
                <div 
                  className="bar-fill" 
                  style={{height: `${(stats.totalFeedback * 0.4) / stats.totalFeedback * 100}%`}}
                ></div>
                <div className="bar-label">△ 部分適用 ({Math.floor(stats.totalFeedback * 0.4)})</div>
              </div>
              <div className="bar">
                <div 
                  className="bar-fill" 
                  style={{height: `${(stats.totalFeedback * 0.3) / stats.totalFeedback * 100}%`}}
                ></div>
                <div className="bar-label">✓ 適用 ({Math.floor(stats.totalFeedback * 0.3)})</div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="analytics-card">
          <h3>練習卡層級星數分布 (API-207.2)</h3>
          <div className="chart-placeholder">
            <p>⭐ 練習卡層級星數分布圖表</p>
            <div className="star-distribution">
              {[1, 2, 3, 4, 5].map(star => (
                <div key={star} className="star-bar">
                  <div className="star-label">{star}★</div>
                  <div 
                    className="star-fill" 
                    style={{width: `${star * 20}%`}}
                  ></div>
                  <div className="star-count">({star * 9})</div>
                </div>
              ))}
            </div>
          </div>
        </div>
        
        <div className="analytics-card">
          <h3>即時 vs 延遲回饋 (API-207.1)</h3>
          <div className="chart-placeholder">
            <p>⏱️ 即時與延遲回饋比較</p>
            <div className="comparison-bars">
              <div className="bar">
                <div 
                  className="bar-fill immediate" 
                  style={{height: `${(stats.totalFeedback * 0.6) / stats.totalFeedback * 100}%`}}
                ></div>
                <div className="bar-label">即時 ({Math.floor(stats.totalFeedback * 0.6)})</div>
              </div>
              <div className="bar">
                <div 
                  className="bar-fill delayed" 
                  style={{height: `${(stats.totalFeedback * 0.4) / stats.totalFeedback * 100}%`}}
                ></div>
                <div className="bar-label">延遲 ({Math.floor(stats.totalFeedback * 0.4)})</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderTabContent = () => {
    switch (activeTab) {
      case 'overview':
        return renderOverviewTab();
      case 'symptoms':
        return renderSymptomsTab();
      case 'practice-cards':
        return renderPracticeCardsTab();
      case 'mappings':
        return renderMappingsTab();
      case 'feedback':
        return renderFeedbackTab();
      default:
        return renderOverviewTab();
    }
  };

  if (loading) {
    return (
      <div className="admin-dashboard">
        <div className="loading">載入中...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="admin-dashboard">
        <div className="error-message">{error}</div>
      </div>
    );
  }

  return (
    <div className="admin-dashboard">
      <div className="page-header">
        <h1>🔧 管理後台</h1>
        <p>系統管理與數據分析</p>
      </div>
      
      <div className="admin-content">
        <nav className="admin-nav">
          <ul>
            <li>
              <button 
                className={activeTab === 'overview' ? 'active' : ''}
                onClick={() => setActiveTab('overview')}
              >
                📊 儀表板
              </button>
            </li>
            <li>
              <button 
                className={activeTab === 'symptoms' ? 'active' : ''}
                onClick={() => navigate('/admin/symptoms')}
              >
                🩺 症狀管理
              </button>
            </li>
            <li>
              <button 
                className={activeTab === 'practice-cards' ? 'active' : ''}
                onClick={() => navigate('/admin/practice-cards')}
              >
                📋 練習卡管理
              </button>
            </li>
            <li>
              <button 
                className={activeTab === 'mappings' ? 'active' : ''}
                onClick={() => navigate('/admin/mappings')}
              >
                🔗 映射管理
              </button>
            </li>
            <li>
              <button 
                className={activeTab === 'feedback' ? 'active' : ''}
                onClick={() => navigate('/admin/analytics')}
              >
                📊 回饋分析
              </button>
            </li>
          </ul>
        </nav>
        
        <div className="admin-main">
          {renderTabContent()}
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;