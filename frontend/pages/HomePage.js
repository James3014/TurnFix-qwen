/**
 * 首頁組件
 */
import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/HomePage.css';

const HomePage = () => {
  return (
    <div className="home-page">
      <section className="hero-section">
        <h2>改善你的滑雪技術</h2>
        <p>描述你的滑行困難，獲得個性化練習建議</p>
        <Link to="/input" className="cta-button">
          開始診斷
        </Link>
      </section>
      
      <section className="features-section">
        <div className="feature-card">
          <h3>症狀識別</h3>
          <p>AI自動識別您的滑行問題</p>
        </div>
        <div className="feature-card">
          <h3>個性化建議</h3>
          <p>根據您的等級和地形提供練習卡</p>
        </div>
        <div className="feature-card">
          <h3>進度追蹤</h3>
          <p>記錄練習進度和改善情況</p>
        </div>
      </section>
      
      <section className="how-it-works">
        <h2>如何使用</h2>
        <div className="steps">
          <div className="step">
            <span className="step-number">1</span>
            <p>描述您的滑行問題</p>
          </div>
          <div className="step">
            <span className="step-number">2</span>
            <p>系統診斷並提供練習建議</p>
          </div>
          <div className="step">
            <span className="step-number">3</span>
            <p>練習並反饋結果</p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;