/**
 * 導航組件 (UI-300)
 * 
 * 設計並實作首頁與導航架構
 */
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import '../styles/Navigation.css';

const Navigation = () => {
  const location = useLocation();
  
  const navItems = [
    { path: '/', label: '首頁', exact: true },
    { path: '/input', label: '我的問題' },
    { path: '/history', label: '練習歷史' },
    { path: '/favorites', label: '最愛練習' },
    { path: '/settings', label: '設定' },
    { path: '/admin', label: '管理後台' }
  ];

  const isActive = (path, exact = false) => {
    if (exact) {
      return location.pathname === path;
    }
    return location.pathname.startsWith(path);
  };

  return (
    <nav className="navigation">
      <div className="nav-container">
        <div className="nav-brand">
          <Link to="/">TurnFix</Link>
        </div>
        
        <ul className="nav-menu">
          {navItems.map((item) => (
            <li key={item.path} className="nav-item">
              <Link 
                to={item.path} 
                className={`nav-link ${isActive(item.path, item.exact) ? 'active' : ''}`}
              >
                {item.label}
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );
};

export default Navigation;