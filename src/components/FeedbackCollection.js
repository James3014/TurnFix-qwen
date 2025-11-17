/**
 * 回饋收集組件 (UI-304)
 *
 * 重構後:使用拆分的子組件
 * 遵循 Linus 原則:
 * - 單一職責:只負責協調子組件和 tab 切換
 * - DRY:使用共享的組件
 * - 簡單:< 80 行
 */
import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import SessionFeedbackForm from './feedback/SessionFeedbackForm';
import PracticeCardFeedbackForm from './feedback/PracticeCardFeedbackForm';
import '../styles/FeedbackCollection.css';

const FeedbackCollection = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { session, recommendedCards } = location.state || {};
  const [activeTab, setActiveTab] = useState('session');

  // 驗證必要資訊
  if (!session || !recommendedCards) {
    return (
      <div className="feedback-collection">
        <div className="error-message">
          <h2>缺少必要資訊</h2>
          <button onClick={() => navigate(-1)}>返回上一頁</button>
        </div>
      </div>
    );
  }

  const renderTabContent = () => {
    switch (activeTab) {
      case 'session':
        return <SessionFeedbackForm sessionId={session.id} />;
      case 'practice-card':
        return <PracticeCardFeedbackForm cards={recommendedCards} sessionId={session.id} />;
      default:
        return <SessionFeedbackForm sessionId={session.id} />;
    }
  };

  return (
    <div className="feedback-collection">
      <div className="page-header">
        <h1>提供回饋</h1>
        <p>您的意見將幫助我們改善系統</p>
      </div>

      <div className="feedback-content">
        <nav className="feedback-nav">
          <ul>
            <li>
              <button
                className={activeTab === 'session' ? 'active' : ''}
                onClick={() => setActiveTab('session')}
              >
                會話回饋
              </button>
            </li>
            <li>
              <button
                className={activeTab === 'practice-card' ? 'active' : ''}
                onClick={() => setActiveTab('practice-card')}
              >
                練習卡回饋
              </button>
            </li>
          </ul>
        </nav>

        <div className="feedback-main">
          {renderTabContent()}
        </div>
      </div>

      <div className="feedback-navigation">
        <button
          className="back-button"
          onClick={() => navigate(-1)}
        >
          ← 返回上一頁
        </button>
        <button
          className="continue-button"
          onClick={() => navigate('/')}
        >
          繼續使用系統 →
        </button>
      </div>
    </div>
  );
};

export default FeedbackCollection;
