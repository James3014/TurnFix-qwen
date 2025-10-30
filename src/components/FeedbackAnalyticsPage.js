/**
 * 回饋分析頁面組件 (UI-307)
 * 
 * 實作回饋分析界面
 */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/FeedbackAnalyticsPage.css';

const FeedbackAnalyticsPage = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('overview');
  const [analyticsData, setAnalyticsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // 模擬數據 - 實際實現中會從API獲取
  useEffect(() => {
    const mockAnalyticsData = {
      session_feedback_distribution: {
        not_applicable: 12,
        partially_applicable: 45,
        applicable: 78
      },
      immediate_vs_delayed: {
        immediate: 80,
        delayed: 55
      },
      feedback_completion_rate: 0.68,
      total_feedback_count: 135,
      rating_distribution: {
        1: 10,
        2: 15,
        3: 45,
        4: 78,
        5: 52
      },
      average_rating: 3.8,
      rating_count: 200,
      favorite_count: 156,
      favorite_rate: 0.32
    };
    
    setAnalyticsData(mockAnalyticsData);
    setLoading(false);
  }, []);

  const renderOverviewTab = () => (
    <div className="overview-tab">
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">📊</div>
          <div className="stat-content">
            <div className="stat-value">{analyticsData?.total_feedback_count || 0}</div>
            <div className="stat-label">總回饋數</div>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">⭐</div>
          <div className="stat-content">
            <div className="stat-value">{analyticsData?.average_rating?.toFixed(1) || 0}</div>
            <div className="stat-label">平均星數</div>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">✅</div>
          <div className="stat-content">
            <div className="stat-value">{analyticsData?.session_feedback_distribution?.applicable || 0}</div>
            <div className="stat-label">适用回饋</div>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">❤️</div>
          <div className="stat-content">
            <div className="stat-value">{analyticsData?.favorite_count || 0}</div>
            <div className="stat-label">最愛數</div>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">📈</div>
          <div className="stat-content">
            <div className="stat-value">{(analyticsData?.feedback_completion_rate * 100).toFixed(0) || 0}%</div>
            <div className="stat-label">完成率</div>
          </div>
        </div>
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
                  style={{height: `${(analyticsData?.session_feedback_distribution?.not_applicable || 0) / 135 * 100}%`}}
                ></div>
                <div className="bar-label">❌ 不適用 ({analyticsData?.session_feedback_distribution?.not_applicable || 0})</div>
              </div>
              <div className="bar">
                <div 
                  className="bar-fill" 
                  style={{height: `${(analyticsData?.session_feedback_distribution?.partially_applicable || 0) / 135 * 100}%`}}
                ></div>
                <div className="bar-label">△ 部分適用 ({analyticsData?.session_feedback_distribution?.partially_applicable || 0})</div>
              </div>
              <div className="bar">
                <div 
                  className="bar-fill" 
                  style={{height: `${(analyticsData?.session_feedback_distribution?.applicable || 0) / 135 * 100}%`}}
                ></div>
                <div className="bar-label">✓ 適用 ({analyticsData?.session_feedback_distribution?.applicable || 0})</div>
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
                    style={{width: `${(analyticsData?.rating_distribution?.[star] || 0) / 200 * 100}%`}}
                  ></div>
                  <div className="star-count">({analyticsData?.rating_distribution?.[star] || 0})</div>
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
                  style={{height: `${(analyticsData?.immediate_vs_delayed?.immediate || 0) / 135 * 100}%`}}
                ></div>
                <div className="bar-label">即時 ({analyticsData?.immediate_vs_delayed?.immediate || 0})</div>
              </div>
              <div className="bar">
                <div 
                  className="bar-fill delayed" 
                  style={{height: `${(analyticsData?.immediate_vs_delayed?.delayed || 0) / 135 * 100}%`}}
                ></div>
                <div className="bar-label">延遲 ({analyticsData?.immediate_vs_delayed?.delayed || 0})</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderPracticeCardTab = () => (
    <div className="practice-card-tab">
      <div className="tab-header">
        <h2>練習卡回饋分析 (API-207.2)</h2>
        <p>深入分析單張練習卡的回饋表現</p>
      </div>
      
      <div className="search-section">
        <input 
          type="text" 
          placeholder="搜尋練習卡..." 
          className="search-input"
        />
        <button className="search-button">🔍 搜尋</button>
      </div>
      
      <div className="card-analysis-grid">
        <div className="analysis-card">
          <h3>J型轉彎練習</h3>
          <div className="card-stats">
            <div className="stat">
              <span className="label">平均星數:</span>
              <span className="value">4.2 ★</span>
            </div>
            <div className="stat">
              <span className="label">評分數量:</span>
              <span className="value">45</span>
            </div>
            <div className="stat">
              <span className="label">最愛數:</span>
              <span className="value">28</span>
            </div>
            <div className="stat">
              <span className="label">最愛率:</span>
              <span className="value">62%</span>
            </div>
          </div>
          <div className="rating-distribution">
            <h4>星數分布</h4>
            <div className="distribution-bars">
              {[1, 2, 3, 4, 5].map(star => (
                <div key={star} className="star-row">
                  <span className="star-label">{star}★</span>
                  <div className="progress-bar">
                    <div 
                      className="progress-fill" 
                      style={{width: `${star * 20}%`}}
                    ></div>
                  </div>
                  <span className="count">({star * 9})</span>
                </div>
              ))}
            </div>
          </div>
        </div>
        
        <div className="analysis-card">
          <h3>重心轉移練習</h3>
          <div className="card-stats">
            <div className="stat">
              <span className="label">平均星數:</span>
              <span className="value">3.8 ★</span>
            </div>
            <div className="stat">
              <span className="label">評分數量:</span>
              <span className="value">32</span>
            </div>
            <div className="stat">
              <span className="label">最愛數:</span>
              <span className="value">15</span>
            </div>
            <div className="stat">
              <span className="label">最愛率:</span>
              <span className="value">47%</span>
            </div>
          </div>
          <div className="rating-distribution">
            <h4>星數分布</h4>
            <div className="distribution-bars">
              {[1, 2, 3, 4, 5].map(star => (
                <div key={star} className="star-row">
                  <span className="star-label">{star}★</span>
                  <div className="progress-bar">
                    <div 
                      className="progress-fill" 
                      style={{width: `${star * 15}%`}}
                    ></div>
                  </div>
                  <span className="count">({star * 6})</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderSymptomTab = () => (
    <div className="symptom-tab">
      <div className="tab-header">
        <h2>症狀回饋分析 (API-207.3)</h2>
        <p>了解症狀推薦的有效性</p>
      </div>
      
      <div className="symptom-analysis-grid">
        <div className="analysis-card">
          <h3>重心太後</h3>
          <div className="card-stats">
            <div className="stat">
              <span className="label">會話數:</span>
              <span className="value">65</span>
            </div>
            <div className="stat">
              <span className="label">適用數:</span>
              <span className="value">48</span>
            </div>
            <div className="stat">
              <span className="label">適用率:</span>
              <span className="value">74%</span>
            </div>
          </div>
          <div className="related-cards">
            <h4>相關練習卡</h4>
            <ul>
              <li>J型轉彎練習 (4.2★, 62% 最愛率)</li>
              <li>重心轉移練習 (3.8★, 47% 最愛率)</li>
              <li>基礎滑行練習 (4.0★, 55% 最愛率)</li>
            </ul>
          </div>
          <div className="performance-indicators">
            <h4>表現指標</h4>
            <div className="indicator high">高效卡片: J型轉彎練習</div>
            <div className="indicator low">問題卡片: 重心轉移練習</div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderUserPreferenceTab = () => (
    <div className="user-preference-tab">
      <div className="tab-header">
        <h2>用戶偏好分析 (API-207.4)</h2>
        <p>了解用戶的練習習慣</p>
      </div>
      
      <div className="preference-sections">
        <div className="preference-card">
          <h3>最高評分練習卡</h3>
          <ol>
            <li>J型轉彎練習 (4.2★)</li>
            <li>基礎滑行練習 (4.0★)</li>
            <li>重心轉移練習 (3.8★)</li>
            <li>換刃練習 (3.7★)</li>
            <li>煞車練習 (3.6★)</li>
          </ol>
        </div>
        
        <div className="preference-card">
          <h3>最常被加入最愛的卡片</h3>
          <ol>
            <li>J型轉彎練習 (62% 最愛率)</li>
            <li>基礎滑行練習 (55% 最愛率)</li>
            <li>換刃練習 (48% 最愛率)</li>
            <li>重心轉移練習 (47% 最愛率)</li>
            <li>煞車練習 (42% 最愛率)</li>
          </ol>
        </div>
        
        <div className="preference-card">
          <h3>用戶段落分析</h3>
          <div className="segment-analysis">
            <div className="segment">
              <h4>初級用戶</h4>
              <p>平均評分: 3.6★</p>
              <p>最愛率: 28%</p>
              <p>偏好: 基礎滑行練習</p>
            </div>
            <div className="segment">
              <h4>中級用戶</h4>
              <p>平均評分: 3.9★</p>
              <p>最愛率: 35%</p>
              <p>偏好: J型轉彎練習</p>
            </div>
            <div className="segment">
              <h4>高級用戶</h4>
              <p>平均評分: 4.1★</p>
              <p>最愛率: 42%</p>
              <p>偏好: 重心轉移練習</p>
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
      case 'practice-card':
        return renderPracticeCardTab();
      case 'symptom':
        return renderSymptomTab();
      case 'user-preference':
        return renderUserPreferenceTab();
      default:
        return renderOverviewTab();
    }
  };

  if (loading) {
    return (
      <div className="feedback-analytics-page">
        <div className="loading">載入中...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="feedback-analytics-page">
        <div className="error-message">{error}</div>
      </div>
    );
  }

  return (
    <div className="feedback-analytics-page">
      <div className="page-header">
        <h1>📊 回饋分析</h1>
        <p>深入了解用戶反饋，優化系統推薦效果</p>
      </div>
      
      <div className="analytics-content">
        <nav className="analytics-nav">
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
                className={activeTab === 'practice-card' ? 'active' : ''}
                onClick={() => setActiveTab('practice-card')}
              >
                📋 練習卡分析
              </button>
            </li>
            <li>
              <button 
                className={activeTab === 'symptom' ? 'active' : ''}
                onClick={() => setActiveTab('symptom')}
              >
                🩺 症狀分析
              </button>
            </li>
            <li>
              <button 
                className={activeTab === 'user-preference' ? 'active' : ''}
                onClick={() => setActiveTab('user-preference')}
              >
                👥 用戶偏好
              </button>
            </li>
          </ul>
        </nav>
        
        <div className="analytics-main">
          {renderTabContent()}
        </div>
      </div>
    </div>
  );
};

export default FeedbackAnalyticsPage;