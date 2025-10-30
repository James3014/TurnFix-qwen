/**
 * 個人化推薦組件
 * 實現 UXP-1814 功能：個人化推薦演化
 */
import React, { useState, useEffect } from 'react';
import './PersonalizedRecommendations.css';

const PersonalizedRecommendations = ({ practiceId, sessionId }) => {
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (practiceId && sessionId) {
      fetchRecommendations();
    }
  }, [practiceId, sessionId]);

  const fetchRecommendations = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(
        `/api/v1/personalization/recommendations/${practiceId}?session_id=${sessionId}`
      );
      
      if (!response.ok) {
        throw new Error('獲取個人化推薦失敗');
      }
      
      const data = await response.json();
      setRecommendations(data.recommendations);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="personalized-recommendations-loading">正在分析您的偏好...</div>;
  }

  if (error) {
    return <div className="personalized-recommendations-error">無法顯示個人化推薦: {error}</div>;
  }

  if (!recommendations || recommendations.recommendations.length === 0) {
    return null;
  }

  return (
    <div className="personalized-recommendations">
      <h3>個人化推薦</h3>
      <p className="recommendation-message">{recommendations.message}</p>
      
      <div className="recommendations-list">
        {recommendations.recommendations.map((rec, index) => (
          <div key={index} className="recommendation-item">
            <div className="recommendation-info">
              <h4>{rec.name}</h4>
              <p>{rec.goal}</p>
              {rec.similar_to_previous && (
                <span className="tag similar">與您目前練習相似</span>
              )}
              {rec.based_on_preference && (
                <span className="tag preference">符合您的偏好</span>
              )}
            </div>
            <button 
              className="recommendation-btn"
              onClick={() => window.location.href = `/practice-card/${rec.id}`}
            >
              查看練習卡
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PersonalizedRecommendations;