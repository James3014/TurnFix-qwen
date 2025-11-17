/**
 * TurnFix API 客戶端
 *
 * 完整對應後端所有 API 端點
 * 遵循 Linus 原則：簡潔、清晰、無廢話
 */
import axios from 'axios';

// 基礎配置
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 請求攔截器
api.interceptors.request.use(
  (config) => {
    // 未來可以在這裡添加認證 token
    return config;
  },
  (error) => Promise.reject(error)
);

// 響應攔截器 - 統一錯誤處理
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error.response?.data || error);
  }
);

// ============================================================
// 滑雪建議相關 API
// ============================================================
export const skiTipsAPI = {
  /**
   * 獲取滑雪技巧建議
   * @param {Object} params - { input_text, level?, terrain?, style? }
   */
  getRecommendations: (params) =>
    api.post('/ski-tips', null, { params }),

  /**
   * 獲取自適應追問需求
   * @param {Object} data - { input_text, level?, terrain?, style? }
   */
  getFollowupNeeds: (data) =>
    api.post('/followup-needs', data),
};

// ============================================================
// 症狀管理 API
// ============================================================
export const symptomsAPI = {
  /**
   * 獲取所有症狀
   */
  getAll: () =>
    api.get('/admin/symptoms'),

  /**
   * 根據 ID 獲取症狀
   * @param {number} id
   */
  getById: (id) =>
    api.get(`/symptoms/${id}`),

  /**
   * 創建新症狀
   * @param {Object} data - { name, category, synonyms, level_scope, terrain_scope, style_scope }
   */
  create: (data) =>
    api.post('/symptoms', data),

  /**
   * 更新症狀
   * @param {number} id
   * @param {Object} data - 要更新的字段
   */
  update: (id, data) =>
    api.put(`/symptoms/${id}`, data),

  /**
   * 刪除症狀
   * @param {number} id
   */
  delete: (id) =>
    api.delete(`/symptoms/${id}`),

  /**
   * 獲取指定症狀的所有練習卡
   * @param {number} symptomId
   */
  getPracticeCards: (symptomId) =>
    api.get(`/symptoms/${symptomId}/practice-cards`),
};

// ============================================================
// 練習卡管理 API
// ============================================================
export const practiceCardsAPI = {
  /**
   * 獲取所有練習卡
   */
  getAll: () =>
    api.get('/admin/practice-cards'),

  /**
   * 根據 ID 獲取練習卡
   * @param {number} id
   */
  getById: (id) =>
    api.get(`/practice-cards/${id}`),

  /**
   * 創建新練習卡
   * @param {Object} data - { name, goal, tips, pitfalls, dosage, level, terrain, self_check, card_type }
   */
  create: (data) =>
    api.post('/practice-cards', data),

  /**
   * 更新練習卡
   * @param {number} id
   * @param {Object} data - 要更新的字段
   */
  update: (id, data) =>
    api.put(`/practice-cards/${id}`, data),

  /**
   * 刪除練習卡
   * @param {number} id
   */
  delete: (id) =>
    api.delete(`/practice-cards/${id}`),
};

// ============================================================
// 症狀練習卡映射 API
// ============================================================
export const mappingsAPI = {
  /**
   * 創建症狀練習卡映射
   * @param {Object} data - { symptom_id, practice_id, order }
   */
  create: (data) =>
    api.post('/symptom-practice-mappings', data),

  /**
   * 刪除症狀練習卡映射
   * @param {number} symptomId
   * @param {number} practiceId
   */
  delete: (symptomId, practiceId) =>
    api.delete(`/admin/symptom-practice-mappings/${symptomId}/${practiceId}`),
};

// ============================================================
// 回饋系統 API
// ============================================================
export const feedbackAPI = {
  /**
   * 提交會話回饋
   * @param {Object} data - { session_id, rating, feedback_text?, feedback_type }
   */
  submitSession: (data) =>
    api.post('/session-feedback', data),

  /**
   * 提交練習卡回饋
   * @param {Object} data - { session_id, practice_id, rating, feedback_text?, is_favorite }
   */
  submitPracticeCard: (data) =>
    api.post('/practice-card-feedback', data),

  /**
   * 切換練習卡最愛狀態
   * @param {number} feedbackId
   * @param {boolean} isFavorite
   */
  toggleFavorite: (feedbackId, isFavorite) =>
    api.put(`/practice-card-feedback/${feedbackId}/favorite`, { is_favorite: isFavorite }),
};

// ============================================================
// 最愛練習卡 API
// ============================================================
export const favoritesAPI = {
  /**
   * 獲取用戶所有最愛練習卡
   */
  getAll: () =>
    api.get('/user/favorite-cards'),

  /**
   * 更新練習卡的最愛狀態
   * @param {number} cardId
   * @param {Object} data - { is_favorite, session_id }
   */
  toggle: (cardId, data) =>
    api.post(`/user/favorite-cards/${cardId}`, data),

  /**
   * 移除最愛標記
   * @param {number} cardId
   * @param {Object} data - { session_id }
   */
  remove: (cardId, data) =>
    api.delete(`/user/favorite-cards/${cardId}`, { data }),
};

// ============================================================
// 管理後台 - 回饋分析 API
// ============================================================
export const adminAnalyticsAPI = {
  /**
   * 獲取回饋系統整體統計
   */
  getSummary: () =>
    api.get('/summary'),

  /**
   * 獲取指定練習卡的回饋統計
   * @param {number} practiceCardId
   */
  getPracticeCardStats: (practiceCardId) =>
    api.get(`/practice-cards/${practiceCardId}`),

  /**
   * 獲取指定症狀的回饋統計
   * @param {number} symptomId
   */
  getSymptomStats: (symptomId) =>
    api.get(`/symptoms/${symptomId}`),

  /**
   * 獲取用戶偏好分析
   */
  getUserPreferences: () =>
    api.get('/user-preferences'),
};

// ============================================================
// 個人化推薦 API
// ============================================================
export const personalizationAPI = {
  /**
   * 獲取用戶偏好設置
   */
  getUserPreferences: () =>
    api.get('/personalization/user-preferences'),

  /**
   * 獲取指定練習卡的個人化推薦
   * @param {number} practiceId
   */
  getRecommendations: (practiceId) =>
    api.get(`/personalization/recommendations/${practiceId}`),
};

// ============================================================
// 知識庫管理 API
// ============================================================
export const knowledgeAPI = {
  /**
   * 上傳知識
   * @param {Object} data - 知識數據
   */
  upload: (data) =>
    api.post('/knowledge/upload', data),

  /**
   * 獲取待審核的知識列表
   */
  listPendingReview: () =>
    api.get('/knowledge/list-pending-review'),

  /**
   * 批准知識
   * @param {number} knowledgeId
   */
  approve: (knowledgeId) =>
    api.post(`/knowledge/approve/${knowledgeId}`),

  /**
   * 拒絕知識
   * @param {number} knowledgeId
   */
  reject: (knowledgeId) =>
    api.post(`/knowledge/reject/${knowledgeId}`),

  /**
   * 匯出知識庫
   */
  export: () =>
    api.get('/knowledge/export'),
};

// ============================================================
// 健康檢查
// ============================================================
export const healthAPI = {
  check: () => api.get('/health'),
};

// 默認導出所有 API
export default {
  skiTips: skiTipsAPI,
  symptoms: symptomsAPI,
  practiceCards: practiceCardsAPI,
  mappings: mappingsAPI,
  feedback: feedbackAPI,
  favorites: favoritesAPI,
  adminAnalytics: adminAnalyticsAPI,
  personalization: personalizationAPI,
  knowledge: knowledgeAPI,
  health: healthAPI,
};
