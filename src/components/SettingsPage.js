/**
 * 設定頁面 (UI-306)
 * 
 * 設計並實作設定頁面
 */
import React, { useState, useEffect } from 'react';
import '../styles/SettingsPage.css';

const SettingsPage = () => {
  const [settings, setSettings] = useState({
    defaultLevel: '',
    defaultTerrain: '',
    defaultStyle: '',
    theme: 'light',
    notifications: true,
    reminderTime: '12:00',
    reminderFrequency: 'daily'
  });
  const [isSaving, setIsSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);

  // 模擬從本地存儲或API加載設定
  useEffect(() => {
    const savedSettings = localStorage.getItem('userSettings');
    if (savedSettings) {
      try {
        setSettings(JSON.parse(savedSettings));
      } catch (e) {
        console.error('載入設定失敗:', e);
      }
    }
  }, []);

  const handleSettingChange = (key, value) => {
    setSettings(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleSave = () => {
    setIsSaving(true);
    setSaveSuccess(false);
    
    // 模擬保存到本地存儲或API
    try {
      localStorage.setItem('userSettings', JSON.stringify(settings));
      setSaveSuccess(true);
      
      // 3秒後隱藏成功消息
      setTimeout(() => {
        setSaveSuccess(false);
      }, 3000);
    } catch (e) {
      console.error('保存設定失敗:', e);
      alert('保存設定失敗，請稍後再試');
    } finally {
      setIsSaving(false);
    }
  };

  const handleReset = () => {
    if (window.confirm('確定要重置所有設定嗎？')) {
      const defaultSettings = {
        defaultLevel: '',
        defaultTerrain: '',
        defaultStyle: '',
        theme: 'light',
        notifications: true,
        reminderTime: '12:00',
        reminderFrequency: 'daily'
      };
      setSettings(defaultSettings);
      localStorage.removeItem('userSettings');
      setSaveSuccess(true);
      setTimeout(() => {
        setSaveSuccess(false);
      }, 3000);
    }
  };

  return (
    <div className="settings-page">
      <div className="page-header">
        <h1>⚙️ 設定</h1>
      </div>
      
      <div className="settings-content">
        <form className="settings-form" onSubmit={(e) => e.preventDefault()}>
          <div className="settings-section">
            <h2>預設偏好</h2>
            <p>設定預設的滑行條件，加快建議生成速度</p>
            
            <div className="setting-group">
              <label htmlFor="defaultLevel">預設等級：</label>
              <select
                id="defaultLevel"
                value={settings.defaultLevel}
                onChange={(e) => handleSettingChange('defaultLevel', e.target.value)}
              >
                <option value="">請選擇</option>
                <option value="初級">初級</option>
                <option value="中級">中級</option>
                <option value="高級">高級</option>
              </select>
            </div>
            
            <div className="setting-group">
              <label htmlFor="defaultTerrain">預設地形：</label>
              <select
                id="defaultTerrain"
                value={settings.defaultTerrain}
                onChange={(e) => handleSettingChange('defaultTerrain', e.target.value)}
              >
                <option value="">請選擇</option>
                <option value="綠線">綠線</option>
                <option value="藍線">藍線</option>
                <option value="黑線">黑線</option>
                <option value="雙黑線">雙黑線</option>
                <option value="野雪">野雪</option>
              </select>
            </div>
            
            <div className="setting-group">
              <label htmlFor="defaultStyle">預設滑行風格：</label>
              <select
                id="defaultStyle"
                value={settings.defaultStyle}
                onChange={(e) => handleSettingChange('defaultStyle', e.target.value)}
              >
                <option value="">請選擇</option>
                <option value="平花">平花</option>
                <option value="回轉">回轉</option>
                <option value="野雪">野雪</option>
                <option value="競速">競速</option>
              </select>
            </div>
          </div>
          
          <div className="settings-section">
            <h2>外觀</h2>
            <p>自訂應用程式的外觀和行為</p>
            
            <div className="setting-group">
              <label htmlFor="theme">主題：</label>
              <select
                id="theme"
                value={settings.theme}
                onChange={(e) => handleSettingChange('theme', e.target.value)}
              >
                <option value="light">淺色主題</option>
                <option value="dark">深色主題</option>
              </select>
            </div>
          </div>
          
          <div className="settings-section">
            <h2>通知</h2>
            <p>設定接收通知和提醒</p>
            
            <div className="setting-group checkbox-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={settings.notifications}
                  onChange={(e) => handleSettingChange('notifications', e.target.checked)}
                />
                <span className="checkmark"></span>
                啟用練習提醒
              </label>
            </div>
            
            {settings.notifications && (
              <>
                <div className="setting-group">
                  <label htmlFor="reminderTime">提醒時間：</label>
                  <input
                    type="time"
                    id="reminderTime"
                    value={settings.reminderTime}
                    onChange={(e) => handleSettingChange('reminderTime', e.target.value)}
                  />
                </div>
                
                <div className="setting-group">
                  <label htmlFor="reminderFrequency">提醒頻率：</label>
                  <select
                    id="reminderFrequency"
                    value={settings.reminderFrequency}
                    onChange={(e) => handleSettingChange('reminderFrequency', e.target.value)}
                  >
                    <option value="daily">每天</option>
                    <option value="weekly">每週</option>
                    <option value="monthly">每月</option>
                  </select>
                </div>
              </>
            )}
          </div>
          
          <div className="settings-actions">
            <button 
              type="button" 
              className="reset-button"
              onClick={handleReset}
            >
              重置設定
            </button>
            <button 
              type="button" 
              className="save-button"
              onClick={handleSave}
              disabled={isSaving}
            >
              {isSaving ? '保存中...' : '保存設定'}
            </button>
          </div>
          
          {saveSuccess && (
            <div className="save-success">
              設定已保存！
            </div>
          )}
        </form>
      </div>
    </div>
  );
};

export default SettingsPage;