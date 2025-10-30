/**
 * 語音朗讀組件
 * 實現 UXP-1816 功能：語音朗讀
 */
import React, { useState, useEffect, useRef } from 'react';
import './VoiceReading.css';

const VoiceReading = ({ text, language = 'zh-TW' }) => {
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [voices, setVoices] = useState([]);
  const [selectedVoice, setSelectedVoice] = useState(null);
  const [isHovered, setIsHovered] = useState(false);
  const utteranceRef = useRef(null);

  // 獲取可用的語音
  useEffect(() => {
    const loadVoices = () => {
      const availableVoices = window.speechSynthesis.getVoices();
      setVoices(availableVoices);
      
      // 根據語言選擇合適的語音
      const preferredVoice = availableVoices.find(voice => 
        voice.lang.includes(language.split('-')[0])
      ) || availableVoices[0];
      
      setSelectedVoice(preferredVoice);
    };

    // 初始加載
    loadVoices();
    
    // 有些瀏覽器需要等待語音列表加載完成
    window.speechSynthesis.onvoiceschanged = loadVoices;

    // 清理函數
    return () => {
      window.speechSynthesis.onvoiceschanged = null;
    };
  }, [language]);

  const toggleSpeech = () => {
    if (isSpeaking) {
      // 停止朗讀
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
    } else {
      // 開始朗讀
      if (text) {
        // 如果有之前的朗讀實例，先取消
        if (utteranceRef.current) {
          window.speechSynthesis.cancel();
        }
        
        // 創建新的朗讀實例
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.voice = selectedVoice || null;
        utterance.lang = language;
        utterance.rate = 1.0; // 調整語速
        utterance.pitch = 1.0; // 調整音調
        utterance.volume = 1.0; // 調整音量
        
        // 設置事件監聽器
        utterance.onstart = () => setIsSpeaking(true);
        utterance.onend = () => setIsSpeaking(false);
        utterance.onerror = () => setIsSpeaking(false);
        
        // 保存引用以便後續取消
        utteranceRef.current = utterance;
        
        // 開始朗讀
        window.speechSynthesis.speak(utterance);
      }
    }
  };

  const getButtonText = () => {
    if (isSpeaking) {
      return '🔊 停止朗讀';
    }
    return '🔊 朗讀練習卡';
  };

  return (
    <div 
      className="voice-reading"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <button
        className={`voice-reading-btn ${isSpeaking ? 'speaking' : ''} ${isHovered ? 'hovered' : ''}`}
        onClick={toggleSpeech}
        aria-label={isSpeaking ? "停止語音朗讀" : "開始語音朗讀"}
        title={isSpeaking ? "點擊停止朗讀" : "點擊開始朗讀練習卡內容"}
      >
        {getButtonText()}
      </button>
      
      {isSpeaking && (
        <div className="speaking-indicator">
          <span className="pulse"></span> 正在朗讀中...
        </div>
      )}
      
      {/* 語音設置選項 - 可以選擇語音和調整參數 */}
      {isHovered && (
        <div className="voice-settings">
          <label htmlFor="voice-select">選擇語音: </label>
          <select
            id="voice-select"
            value={selectedVoice?.name || ''}
            onChange={(e) => {
              const voice = voices.find(v => v.name === e.target.value);
              setSelectedVoice(voice);
            }}
          >
            {voices.map((voice, index) => (
              <option key={index} value={voice.name}>
                {voice.name} ({voice.lang})
              </option>
            ))}
          </select>
        </div>
      )}
    </div>
  );
};

export default VoiceReading;