/**
 * TurnFix 前端應用程式入口
 * 
 * 此應用程式提供：
 * 1. 使用者輸入口語問題的介面
 * 2. 顯示症狀辨識結果
 * 3. 顯示練習卡建議
 * 4. 使用者回饋收集
 */
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

console.log('TurnFix 前端應用程式已啟動');