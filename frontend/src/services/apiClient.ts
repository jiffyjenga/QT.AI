import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

// API base URL from environment variables
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance
const axiosInstance: AxiosInstance = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth token
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling errors
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle 401 Unauthorized errors (token expired or invalid)
    if (error.response && error.response.status === 401) {
      // Clear token and redirect to login
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API client with typed methods
const apiClient = {
  // Generic request method with type parameter
  request: async <T>(config: AxiosRequestConfig): Promise<T> => {
    try {
      const response: AxiosResponse<T> = await axiosInstance(config);
      return response.data;
    } catch (error) {
      console.error('API request error:', error);
      throw error;
    }
  },

  // GET request
  get: async <T>(url: string, config?: AxiosRequestConfig): Promise<T> => {
    return apiClient.request<T>({ ...config, method: 'GET', url });
  },

  // POST request
  post: async <T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
    return apiClient.request<T>({ ...config, method: 'POST', url, data });
  },

  // PUT request
  put: async <T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
    return apiClient.request<T>({ ...config, method: 'PUT', url, data });
  },

  // DELETE request
  delete: async <T>(url: string, config?: AxiosRequestConfig): Promise<T> => {
    return apiClient.request<T>({ ...config, method: 'DELETE', url });
  },
};

export default apiClient;
