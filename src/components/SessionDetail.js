/**
 * 會話詳細頁面
 * 顯示單次練習會話的完整信息和推薦的練習卡
 */
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import '../styles/SessionDetail.css';

const SessionDetail = () => {
  const { sessionId } = useParams();
  const navigate = useNavigate();
  const [session, setSession] = useState(null);
  const [practiceCards, setPracticeCards] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // 模擬從 API 獲取會話詳細信息
    // 實際實現中應該調用 API: GET /api/sessions/{sessionId}
    const mockSessionData = {
      1: {
        id: 1,
        date: '2025-10-28',
        input_text: '轉彎會後坐',
        level: '初級',
        terrain: '綠線',
        symptom: '重心太後',
        detected_symptoms: ['重心太後', '姿勢不正確'],
        feedback_rating: 'applicable',
        feedback_text: '練習卡很有幫助',
        cards: [
          {
            id: 101,
            name: 'J型轉彎練習',
            card_type: '技術',
            goal: '改善轉彎時的重心位置，避免後坐',
            tips: ['保持膝蓋彎曲', '重心放在前腳', '視線看向轉彎方向'],
            pitfalls: '容易重心過度後移，導致失去控制',
            dosage: '每次練習 10-15 次轉彎'
          },
          {
            id: 102,
            name: '重心轉移練習',
            card_type: '基礎',
            goal: '學習正確的重心轉移技巧',
            tips: ['感受前後腳的壓力變化', '保持上身穩定', '用髖部帶動重心'],
            pitfalls: '不要用肩膀帶動重心',
            dosage: '每次練習 5-10 分鐘'
          },
          {
            id: 103,
            name: '基礎滑行姿勢',
            card_type: '基礎',
            goal: '建立正確的滑行姿勢',
            tips: ['膝蓋微彎', '重心在前', '放鬆上身'],
            pitfalls: '不要僵硬站立',
            dosage: '持續練習直到成為習慣'
          }
        ]
      },
      2: {
        id: 2,
        date: '2025-10-25',
        input_text: '換刃不順',
        level: '中級',
        terrain: '藍線',
        symptom: '換刃困難',
        detected_symptoms: ['換刃困難', '節奏不穩'],
        feedback_rating: 'partially_applicable',
        feedback_text: '',
        cards: [
          {
            id: 201,
            name: '換刃節奏練習',
            card_type: '技術',
            goal: '改善換刃的流暢度和節奏',
            tips: ['保持固定節奏', '完成每個動作', '不要急於換刃'],
            pitfalls: '換刃過快導致失衡',
            dosage: '連續練習 20-30 個轉彎'
          }
        ]
      },
      3: {
        id: 3,
        date: '2025-10-20',
        input_text: '重心不穩',
        level: '初級',
        terrain: '綠線',
        symptom: '重心不穩',
        detected_symptoms: ['重心不穩', '平衡感差'],
        feedback_rating: 'applicable',
        feedback_text: '練習後有明顯改善',
        cards: [
          {
            id: 301,
            name: '平衡感訓練',
            card_type: '基礎',
            goal: '提升整體平衡能力',
            tips: ['單腳平衡練習', '核心肌群使用', '視線穩定'],
            pitfalls: '不要過度緊張',
            dosage: '每天練習 10 分鐘'
          }
        ]
      }
    };

    const sessionData = mockSessionData[sessionId];
    if (sessionData) {
      setSession(sessionData);
      setPracticeCards(sessionData.cards);
    }
    setLoading(false);
  }, [sessionId]);

  const viewCardDetail = (card) => {
    navigate(`/practice-card/${card.id}`, { state: { card } });
  };

  const getFeedbackIcon = (rating) => {
    switch (rating) {
      case 'not_applicable':
        return { icon: '❌', text: '不適用' };
      case 'partially_applicable':
        return { icon: '△', text: '部分適用' };
      case 'applicable':
        return { icon: '✓', text: '適用' };
      default:
        return { icon: '', text: '未評價' };
    }
  };

  if (loading) {
    return (
      <div className="session-detail">
        <div className="loading">載入中...</div>
      </div>
    );
  }

  if (!session) {
    return (
      <div className="session-detail">
        <div className="error-message">
          <h2>找不到此練習記錄</h2>
          <button
            className="back-button"
            onClick={() => navigate('/history')}
          >
            返回練習歷史
          </button>
        </div>
      </div>
    );
  }

  const feedback = getFeedbackIcon(session.feedback_rating);

  return (
    <div className="session-detail">
      <div className="page-header">
        <button
          className="back-button"
          onClick={() => navigate('/history')}
        >
          ← 返回練習歷史
        </button>
        <h1>練習會話詳細</h1>
      </div>

      <div className="session-info-card">
        <div className="info-row">
          <div className="info-item">
            <strong>日期：</strong>
            <span>{session.date}</span>
          </div>
          <div className="info-item">
            <strong>回饋：</strong>
            <span className="feedback-badge">
              {feedback.icon} {feedback.text}
            </span>
          </div>
        </div>

        <div className="info-row">
          <div className="info-item full-width">
            <strong>問題描述：</strong>
            <span>{session.input_text}</span>
          </div>
        </div>

        <div className="info-row">
          <div className="info-item">
            <strong>等級：</strong>
            <span>{session.level}</span>
          </div>
          <div className="info-item">
            <strong>地形：</strong>
            <span>{session.terrain}</span>
          </div>
        </div>

        <div className="info-row">
          <div className="info-item full-width">
            <strong>檢測到的症狀：</strong>
            <div className="symptom-tags">
              {session.detected_symptoms.map((symptom, index) => (
                <span key={index} className="symptom-tag">{symptom}</span>
              ))}
            </div>
          </div>
        </div>

        {session.feedback_text && (
          <div className="info-row">
            <div className="info-item full-width">
              <strong>用戶回饋：</strong>
              <p className="feedback-text">{session.feedback_text}</p>
            </div>
          </div>
        )}
      </div>

      <div className="practice-cards-section">
        <h2>推薦的練習卡 ({practiceCards.length} 張)</h2>
        <div className="practice-cards-grid">
          {practiceCards.map((card, index) => (
            <div key={card.id} className="practice-card">
              <div className="card-number">{index + 1}</div>
              <div className="card-header">
                <h3>{card.name}</h3>
                <span className="card-type-badge">{card.card_type}</span>
              </div>
              <div className="card-content">
                <div className="card-section">
                  <strong>目標：</strong>
                  <p>{card.goal}</p>
                </div>
                <div className="card-section">
                  <strong>要點：</strong>
                  <ul>
                    {card.tips.slice(0, 2).map((tip, idx) => (
                      <li key={idx}>{tip}</li>
                    ))}
                    {card.tips.length > 2 && <li>...</li>}
                  </ul>
                </div>
              </div>
              <button
                className="view-card-btn"
                onClick={() => viewCardDetail(card)}
              >
                查看完整內容
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SessionDetail;
