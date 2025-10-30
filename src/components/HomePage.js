/**
 * 首頁組件 (UI-300)
 * 
 * 設計並實作首頁與導航架構
 */
import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/HomePage.css';

const HomePage = () => {
  const navigate = useNavigate();

  const handleStartDiagnosis = () => {
    navigate('/input');
  };

  return (
    <div className="home-page">
      <div className="hero-section">
        <h1>⛷️ TurnFix</h1>
        <p>滑行技巧問題診斷與練習建議系統</p>
        <button className="cta-button" onClick={handleStartDiagnosis}>
          開始診斷
        </button>
      </div>
      
      <div className="features-section">
        <div className="feature-card">
          <div className="feature-icon">🩺</div>
          <h2>症狀辨識</h2>
          <p>精準識別您的滑行困難點，提供專業分析</p>
        </div>
        
        <div className="feature-card">
          <div className="feature-icon">📋</div>
          <h2>練習建議</h2>
          <p>根據您的問題推薦最適合的練習方案</p>
        </div>
        
        <div className="feature-card">
          <div className="feature-icon">🔄</div>
          <h2>追問機制</h2>
          <p>自動追問相關問題以提供更準確的建議</p>
        </div>
      </div>
      
      <div className="how-it-works">
        <h2>如何使用</h2>
        <div className="steps">
          <div className="step">
            <div className="step-number">1</div>
            <h3>描述問題</h3>
            <p>詳細描述您在滑行時遇到的困難</p>
          </div>
          <div className="step">
            <div className="step-number">2</div>
            <h3>回答追問</h3>
            <p>系統會自動追問相關問題以精準定位問題</p>
          </div>
          <div className="step">
            <div className="step-number">3</div>
            <h3>獲取建議</h3>
            <p>獲得針對性的練習建議以改善問題</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;