/**
 * API 串接工具
 */
import axios from 'axios';

// 基礎配置
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000, // 10秒超時
  headers: {
    'Content-Type': 'application/json',
  },
});

// 請求攔截器
api.interceptors.request.use(
  (config) => {
    // 可以在這裡添加認證 token
    // const token = localStorage.getItem('token');
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 響應攔截器
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// API 方法
const getRecommendations = (data) => {
  return api.post('/ski-tips', data);
};

const submitFeedback = (data) => {
  return api.post('/feedback', data);
};

const getAdminData = () => {
  return api.get('/admin/dashboard');
};

export default {
  getRecommendations,
  submitFeedback,
  getAdminData,
};