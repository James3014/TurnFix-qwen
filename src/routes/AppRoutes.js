/**
 * 應用程式路由配置 (UI-300)
 * 
 * 設計並實作應用程式路由
 */
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from '../components/HomePage';
import InputPage from '../components/InputPage';
import ResultsPage from '../components/ResultsPage';
import FeedbackCollection from '../components/FeedbackCollection';
import AdminDashboard from '../components/AdminDashboard';
import SymptomManagement from '../components/SymptomManagement';
import PracticeCardManagement from '../components/PracticeCardManagement';
import SymptomPracticeMappingManagement from '../components/SymptomPracticeMappingManagement';
import FeedbackAnalytics from '../components/FeedbackAnalytics';
import FavoritePracticeCards from '../components/FavoritePracticeCards';
import '../styles/AppRoutes.css';

const AppRoutes = () => {
  return (
    <Routes>
      {/* 首頁路由 (UI-300) */}
      <Route path="/" element={<HomePage />} />
      
      {/* 使用者輸入路由 (UI-301) */}
      <Route path="/input" element={<InputPage />} />
      
      {/* 練習卡展示路由 (UI-303) */}
      <Route path="/results" element={<ResultsPage />} />
      
      {/* 使用者回饋路由 (UI-304) */}
      <Route path="/feedback" element={<FeedbackCollection />} />
      
      {/* 最愛練習清單路由 (UI-309) */}
      <Route path="/favorites" element={<FavoritePracticeCards />} />
      
      {/* 管理者後台路由 (UI-308) */}
      <Route path="/admin/*" element={<AdminDashboard />} />
      
      {/* 症狀管理路由 (UI-308.1) */}
      <Route path="/admin/symptoms" element={<SymptomManagement />} />
      
      {/* 練習卡管理路由 (UI-308.2) */}
      <Route path="/admin/practice-cards" element={<PracticeCardManagement />} />
      
      {/* 症狀練習卡映射管理路由 (UI-308.3) */}
      <Route path="/admin/mappings" element={<SymptomPracticeMappingManagement />} />
      
      {/* 回饋分析路由 (UI-307) */}
      <Route path="/admin/analytics" element={<FeedbackAnalytics />} />
    </Routes>
  );
};

export default AppRoutes;