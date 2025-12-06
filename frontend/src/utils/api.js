import axios from 'axios';

// API base URL - uses environment variable or defaults to localhost
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 second timeout for large file uploads
});

// Response interceptor to ensure data is always parsed
api.interceptors.response.use(
  (response) => {
    // If response.data is a string, try to parse it as JSON
    if (typeof response.data === 'string') {
      try {
        response.data = JSON.parse(response.data);
      } catch (e) {
        // Keep as string if not valid JSON
      }
    }
    return response;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Health check
export const checkHealth = async () => {
  const response = await api.get('/health');
  return response.data;
};

// Upload endpoints
export const uploadFile = async (fileType, file, onProgress) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post(`/upload/${fileType}`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    onUploadProgress: (progressEvent) => {
      if (onProgress) {
        const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
        onProgress(percentCompleted);
      }
    },
  });
  return response.data;
};

export const getUploadStatus = async () => {
  const response = await api.get('/upload/status');
  return response.data;
};

export const deleteFile = async (fileType) => {
  const response = await api.delete(`/upload/${fileType}`);
  return response.data;
};

export const clearAllFiles = async () => {
  const response = await api.delete('/upload/clear');
  return response.data;
};

// Process endpoints
export const runProcessing = async (config = null) => {
  const response = await api.post('/process', config ? { config } : {});
  return response.data;
};

export const getProcessingStatus = async () => {
  const response = await api.get('/process/status');
  return response.data;
};

// Results endpoints
export const getAllResults = async () => {
  const response = await api.get('/results');
  return response.data;
};

export const getOccupancyResults = async () => {
  const response = await api.get('/results/occupancy');
  return response.data;
};

export const getRevenueResults = async () => {
  const response = await api.get('/results/revenue');
  return response.data;
};

export const getSummary = async () => {
  const response = await api.get('/results/summary');
  return response.data;
};

// Download endpoints
export const downloadOccupancy = () => {
  window.open(`${API_BASE_URL}/download/occupancy`, '_blank');
};

export const downloadRevenue = () => {
  window.open(`${API_BASE_URL}/download/revenue`, '_blank');
};

export const downloadAll = () => {
  window.open(`${API_BASE_URL}/download/all`, '_blank');
};

export default api;
