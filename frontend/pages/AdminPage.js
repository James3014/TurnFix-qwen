/**
 * 管理員頁面組件
 */
import React, { useState, useEffect } from 'react';
import '../styles/AdminPage.css';
import api from '../api/api';

const AdminPage = () => {
  const [adminData, setAdminData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAdminData();
  }, []);

  const fetchAdminData = async () => {
    try {
      const response = await api.getAdminData();
      setAdminData(response.data);
      setLoading(false);
    } catch (err) {
      setError('獲取管理數據失敗');
      setLoading(false);
      console.error('Error fetching admin data:', err);
    }
  };

  if (loading) {
    return <div className="admin-page">載入中...</div>;
  }

  if (error) {
    return <div className="admin-page error">{error}</div>;
  }

  return (
    <div className="admin-page">
      <h2>管理後台</h2>
      
      <div className="admin-dashboard">
        <div className="dashboard-stats">
          <div className="stat-card">
            <h3>總會話數</h3>
            <p>{adminData?.total_sessions || 0}</p>
          </div>
          <div className="stat-card">
            <h3>總反饋數</h3>
            <p>{adminData?.total_feedbacks || 0}</p>
          </div>
          <div className="stat-card">
            <h3>平均評分</h3>
            <p>{adminData?.average_rating ? adminData.average_rating.toFixed(2) : 'N/A'}</p>
          </div>
        </div>
        
        <div className="admin-sections">
          <div className="admin-section">
            <h3>症狀管理</h3>
            <p>管理滑雪問題症狀庫</p>
            <button className="admin-btn">查看症狀</button>
          </div>
          
          <div className="admin-section">
            <h3>練習卡管理</h3>
            <p>管理練習建議卡片</p>
            <button className="admin-btn">查看練習卡</button>
          </div>
          
          <div className="admin-section">
            <h3>反饋分析</h3>
            <p>查看用戶反饋統計</p>
            <button className="admin-btn">查看分析</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminPage;