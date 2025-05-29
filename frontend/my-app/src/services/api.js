import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const chat = {
  sendMessage: (message) => api.post('/api/chat', { message }),
  getMessages: () => api.get('/api/chat/history'),
};

export const logs = {
  getLogs: () => api.get('/api/logs'),
};

export const agents = {
  getStatus: () => api.get('/api/agents/status'),
  startAgent: (agentId) => api.post(`/api/agents/${agentId}/start`),
  stopAgent: (agentId) => api.post(`/api/agents/${agentId}/stop`),
};

export const workflow = {
  getStatus: () => api.get('/api/workflow/status'),
  startWorkflow: (workflowData) => api.post('/api/workflow/start', workflowData),
};

// Add request interceptor for adding auth token if needed
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add response interceptor for handling errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized error (e.g., redirect to login)
      console.error('Unauthorized access - please log in');
    }
    return Promise.reject(error);
  }
);

export default api;
