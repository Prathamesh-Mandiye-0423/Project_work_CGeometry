import axios, { AxiosError } from 'axios';
import type {AxiosInstance} from "axios";
import type {
  ComputeRequest,
  ComputeResponse,
  HealthResponse,
  AlgorithmsResponse,
  VersionResponse,
  APIError,
} from '../types';

// Create axios instance with base configuration
const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'https://project-work-cgeometry-4.onrender.com',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(' API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error: AxiosError) => {
    console.error(' Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(' API Response:', response.status, response.config.url);
    return response;
  },
  (error: AxiosError<APIError>) => {
    console.error(' Response Error:', error.response?.status, error.message);
    return Promise.reject(error);
  }
);

// API Service Methods
export const separatorAPI = {
  /**
   * Compute separators for given points
   */
  computeSeparators: async (data: ComputeRequest): Promise<ComputeResponse> => {
    try {
      const response = await api.post<ComputeResponse>('/api/compute-separators', data);
      return response.data;
    } catch (error) {
      const axiosError = error as AxiosError<APIError>;
      throw new Error(
        axiosError.response?.data?.detail || 'Failed to compute separators'
      );
    }
  },

  /**
   * Get API health status
   */
  getHealth: async (): Promise<HealthResponse> => {
    try {
      const response = await api.get<HealthResponse>('/api/health');
      return response.data;
    } catch (error) {
      throw new Error('Failed to check health status');
    }
  },

  /**
   * Get algorithm information
   */
  getAlgorithms: async (): Promise<AlgorithmsResponse> => {
    try {
      const response = await api.get<AlgorithmsResponse>('/api/algorithms');
      return response.data;
    } catch (error) {
      throw new Error('Failed to fetch algorithm information');
    }
  },

  /**
   * Get API version
   */
  getVersion: async (): Promise<VersionResponse> => {
    try {
      const response = await api.get<VersionResponse>('/api/version');
      return response.data;
    } catch (error) {
      throw new Error('Failed to fetch version');
    }
  },
};

export default api;