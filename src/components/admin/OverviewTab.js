/**
 * 管理後台 - 概覽標籤
 * 簡潔版本，遵循 Linus 原則
 */
import React from 'react';

const OverviewTab = ({ stats }) => {
  return (
    <div className="overview-tab">
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">🩺</div>
          <div className="stat-content">
            <div className="stat-value">{stats.totalSymptoms || 0}</div>
            <div className="stat-label">總症狀數</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📋</div>
          <div className="stat-content">
            <div className="stat-value">{stats.totalPracticeCards || 0}</div>
            <div className="stat-label">總練習卡數</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">👥</div>
          <div className="stat-content">
            <div className="stat-value">{stats.totalSessions || 0}</div>
            <div className="stat-label">總會話數</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">⭐</div>
          <div className="stat-content">
            <div className="stat-value">{(stats.avgRating || 0).toFixed(1)}</div>
            <div className="stat-label">平均星數</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">💬</div>
          <div className="stat-content">
            <div className="stat-value">{stats.totalFeedback || 0}</div>
            <div className="stat-label">總回饋數</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OverviewTab;
