/**
 * 使用者輸入介面 (UI-301)
 * 
 * 設計並實作使用者輸入口語問題的介面
 */
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/SkiInputForm.css';

const SkiInputForm = () => {
  const navigate = useNavigate();
  const [inputText, setInputText] = useState('');
  const [selectedOptions, setSelectedOptions] = useState({
    level: '',
    terrain: '',
    style: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    setInputText(e.target.value);
  };

  const handleOptionChange = (category, value) => {
    setSelectedOptions(prev => ({
      ...prev,
      [category]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!inputText.trim()) {
      setError('請描述您的滑行問題');
      return;
    }
    
    setIsLoading(true);
    setError('');
    
    try {
      // 調用後端API獲取滑雪建議
      const response = await fetch('/api/v1/ski-tips', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          input_text: inputText,
          level: selectedOptions.level,
          terrain: selectedOptions.terrain,
          style: selectedOptions.style
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        // 導向結果頁面
        navigate('/results', {
          state: {
            recommendedCards: data.recommended_cards,
            userInput: inputText,
            selectedOptions
          }
        });
      } else {
        throw new Error('獲取建議失敗');
      }
    } catch (err) {
      setError('提交失敗，請稍後再試');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="ski-input-form">
      <div className="page-header">
        <h1>⛷️ 描述您的滑行困難</h1>
        <p>請盡可能詳細地描述您在滑雪時遇到的問題</p>
      </div>
      
      <form onSubmit={handleSubmit} className="input-form">
        <div className="form-group">
          <label htmlFor="problem-description">
            請描述您的問題 *
          </label>
          <textarea
            id="problem-description"
            value={inputText}
            onChange={handleInputChange}
            placeholder="例如：轉彎會後坐、重心不穩、換刃困難等"
            rows={4}
            className={error && !inputText.trim() ? 'error' : ''}
          />
          {error && !inputText.trim() && (
            <span className="error-message">{error}</span>
          )}
        </div>
        
        <div className="optional-section">
          <h2>選填資訊（幫助提供更精準建議）</h2>
          
          <div className="options-row">
            <div className="option-group">
              <label>等級</label>
              <div className="radio-group">
                {['初級', '中級', '高級'].map(level => (
                  <label key={level} className="radio-label">
                    <input
                      type="radio"
                      name="level"
                      value={level}
                      checked={selectedOptions.level === level}
                      onChange={() => handleOptionChange('level', level)}
                    />
                    <span className="radio-custom"></span>
                    {level}
                  </label>
                ))}
              </div>
            </div>
            
            <div className="option-group">
              <label>地形</label>
              <div className="radio-group">
                {['綠線', '藍線', '黑線'].map(terrain => (
                  <label key={terrain} className="radio-label">
                    <input
                      type="radio"
                      name="terrain"
                      value={terrain}
                      checked={selectedOptions.terrain === terrain}
                      onChange={() => handleOptionChange('terrain', terrain)}
                    />
                    <span className="radio-custom"></span>
                    {terrain}
                  </label>
                ))}
              </div>
            </div>
            
            <div className="option-group">
              <label>滑行風格</label>
              <div className="radio-group">
                {['平花', '自由式', 'Park'].map(style => (
                  <label key={style} className="radio-label">
                    <input
                      type="radio"
                      name="style"
                      value={style}
                      checked={selectedOptions.style === style}
                      onChange={() => handleOptionChange('style', style)}
                    />
                    <span className="radio-custom"></span>
                    {style}
                  </label>
                ))}
              </div>
            </div>
          </div>
        </div>
        
        <button 
          type="submit" 
          className="submit-button"
          disabled={isLoading}
        >
          {isLoading ? '處理中...' : '獲取練習建議'}
        </button>
        
        {error && !inputText.trim() && (
          <div className="error-message">{error}</div>
        )}
      </form>
    </div>
  );
};

export default SkiInputForm;