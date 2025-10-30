/**
 * 視頻示範組件
 * 實現 UXP-1815 功能：視頻示範鏈接
 */
import React, { useState, useEffect } from 'react';
// 移除缺失的 CSS 文件引用，避免構建錯誤
// import './VideoDemo.css';

const VideoDemo = ({ practiceCardId }) => {
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showVideos, setShowVideos] = useState(false);

  useEffect(() => {
    if (practiceCardId && showVideos) {
      fetchVideos();
    }
  }, [practiceCardId, showVideos]);

  const fetchVideos = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`/api/v1/video-suggestions/${practiceCardId}`);
      const data = await response.json();

      if (data.status === 'success') {
        setVideos(data.videos);
      } else {
        setError(data.message || '獲取視頻建議失敗');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const toggleVideosVisibility = () => {
    if (!showVideos) {
      setShowVideos(true);
    } else {
      setShowVideos(!showVideos);
    }
  };

  return (
    <div className="video-demo">
      <div className="video-demo-header">
        <button 
          className="video-demo-toggle"
          onClick={toggleVideosVisibility}
        >
          {showVideos ? '隱藏視頻示範' : '📺 查看示範視頻'}
        </button>
      </div>

      {showVideos && (
        <div className="video-demo-content">
          {loading && <div className="loading">正在搜索相關視頻...</div>}
          
          {error && (
            <div className="error">
              {error}
            </div>
          )}

          {!loading && !error && videos.length === 0 && (
            <div className="no-videos">
              暫無相關視頻示範
            </div>
          )}

          {!loading && !error && videos.length > 0 && (
            <div className="video-list">
              {videos.map((video) => (
                <div key={video.id} className="video-item">
                  <a 
                    href={video.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="video-link"
                  >
                    <img 
                      src={video.thumbnail} 
                      alt={video.title} 
                      className="video-thumbnail"
                    />
                    <div className="video-info">
                      <h4>{video.title}</h4>
                      <p>{video.description.substring(0, 100)}...</p>
                    </div>
                  </a>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default VideoDemo;