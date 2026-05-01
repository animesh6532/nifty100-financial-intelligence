import axios from 'axios';

// Ensure the backend URL is set correctly via env variables
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request Interceptor: Attach JWT or API Keys if present
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    const apiKey = localStorage.getItem('api_key');

    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    } else if (apiKey) {
      // Allow testing partner API easily
      config.headers['X-API-KEY'] = apiKey;
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response Interceptor: Global error handling
api.interceptors.response.use(
  (response) => {
    // If our backend uses a standardized { success, data, message } format:
    if (response.data && response.data.success !== undefined) {
       return response.data;
    }
    return response;
  },
  (error) => {
    // Handle 401 Unauthorized globally
    if (error.response && error.response.status === 401) {
      console.warn("Unauthorized access. Redirecting to login...");
      // Optionally clear tokens and redirect here
    }
    return Promise.reject(error);
  }
);

export default api;
