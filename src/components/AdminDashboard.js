/**
 * 管理後台組件
 *
 * 簡潔版本 - 遵循 Linus 原則：
 * 1. 只做容器，不做邏輯
 * 2. 每個 Tab 是獨立組件
 * 3. 從 499 行減少到 < 100 行
 */
import React, { useState } from 'react';
import OverviewTab from './admin/OverviewTab';
import SymptomsTab from './admin/SymptomsTab';
import PracticeCardsTab from './admin/PracticeCardsTab';
import MappingsTab from './admin/MappingsTab';
import AnalyticsTab from './admin/AnalyticsTab';
import '../styles/AdminDashboard.css';

const AdminDashboard = () => {
  const [activeTab, setActiveTab] = useState('overview');

  // 模擬統計數據 - 實際應從 API 獲取
  const stats = {
    totalSymptoms: 15,
    totalPracticeCards: 42,
    totalSessions: 128,
    totalFeedback: 86,
    avgRating: 4.2,
  };

  const tabs = [
    { id: 'overview', label: '概覽', icon: '📊' },
    { id: 'symptoms', label: '症狀管理', icon: '🩺' },
    { id: 'practice-cards', label: '練習卡管理', icon: '📋' },
    { id: 'mappings', label: '映射管理', icon: '🔗' },
    { id: 'analytics', label: '回饋分析', icon: '📈' },
  ];

  const renderTabContent = () => {
    switch (activeTab) {
      case 'overview':
        return <OverviewTab stats={stats} />;
      case 'symptoms':
        return <SymptomsTab />;
      case 'practice-cards':
        return <PracticeCardsTab />;
      case 'mappings':
        return <MappingsTab />;
      case 'analytics':
        return <AnalyticsTab />;
      default:
        return <OverviewTab stats={stats} />;
    }
  };

  return (
    <div className="admin-dashboard">
      <div className="dashboard-header">
        <h1>管理後台</h1>
      </div>

      <div className="dashboard-tabs">
        {tabs.map(tab => (
          <button
            key={tab.id}
            className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            <span className="tab-icon">{tab.icon}</span>
            <span className="tab-label">{tab.label}</span>
          </button>
        ))}
      </div>

      <div className="dashboard-content">
        {renderTabContent()}
      </div>
    </div>
  );
};

export default AdminDashboard;
