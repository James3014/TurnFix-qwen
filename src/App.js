/**
 * TurnFix 前端應用程式主組件
 */
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './styles/App.css';
import Navigation from './components/Navigation';
import HomePage from './components/HomePage';
import SkiInputForm from './components/SkiInputForm';
import ResultsPage from './components/ResultsPage';
import PracticeCardDetail from './components/PracticeCardDetail';
import PracticeHistory from './components/PracticeHistory';
import SessionDetail from './components/SessionDetail';
import FavoritePracticeCards from './components/FavoritePracticeCards';
import SettingsPage from './components/SettingsPage';
import AdminDashboard from './components/AdminDashboard';
import AdminOverview from './components/AdminOverview';
import SymptomManagement from './components/SymptomManagement';
import PracticeCardManagement from './components/PracticeCardManagement';
import SymptomPracticeMappingManagement from './components/SymptomPracticeMappingManagement';
import FeedbackAnalytics from './components/FeedbackAnalytics';
import FollowupQuestions from './components/FollowupQuestions';
import FeedbackCollection from './components/FeedbackCollection';

function App() {
  return (
    <Router>
      <div className="App">
        <Navigation />
        
        <main className="app-main">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/input" element={<SkiInputForm />} />
            <Route path="/results" element={<ResultsPage />} />
            <Route path="/practice-card/:id" element={<PracticeCardDetail />} />
            <Route path="/history" element={<PracticeHistory />} />
            <Route path="/history/:sessionId" element={<SessionDetail />} />
            <Route path="/favorites" element={<FavoritePracticeCards />} />
            <Route path="/settings" element={<SettingsPage />} />
            
            {/* 自適應追問路由 */}
            <Route path="/followup" element={<FollowupQuestions />} />
            
            {/* 使用者回饋路由 */}
            <Route path="/feedback" element={<FeedbackCollection />} />
            
            {/* 管理者後台路由 */}
            <Route path="/admin" element={<AdminDashboard />}>
              <Route index element={<AdminOverview />} />
              <Route path="symptoms" element={<SymptomManagement />} />
              <Route path="practice-cards" element={<PracticeCardManagement />} />
              <Route path="mappings" element={<SymptomPracticeMappingManagement />} />
              <Route path="analytics" element={<FeedbackAnalytics />} />
            </Route>
          </Routes>
        </main>
        
        <footer className="app-footer">
          <p>© 2025 TurnFix - 滑雪症狀診斷與練習建議系統</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;