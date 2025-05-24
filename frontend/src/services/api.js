/**
 * API service for communicating with the backend
 */
import axios from 'axios';

// Base API URL - use relative URL for same-origin API
const API_URL = '';

// Create axios instance with common config
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

/**
 * Upload a codebase file
 * 
 * @param {File} file - The file to upload
 * @returns {Promise} API response with codebase ID
 */
export const uploadCodebase = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  return apiClient.post('/api/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
};

/**
 * Clone a GitHub repository
 * 
 * @param {string} repoUrl - Repository URL
 * @param {string} branch - Branch to clone (optional)
 * @returns {Promise} API response with codebase ID
 */
export const cloneRepository = (repoUrl, branch = 'main') => {
  return apiClient.post('/api/clone', {
    repo_url: repoUrl,
    branch
  });
};

/**
 * Get insights for a codebase
 * 
 * @param {string} codebaseId - Codebase ID
 * @param {string} role - User role
 * @param {string} specificFocus - Optional specific focus area
 * @returns {Promise} API response with insights data
 */
export const getInsights = (codebaseId, role, specificFocus = null) => {
  return apiClient.post('/api/insights', {
    codebase_id: codebaseId,
    role: role,
    specific_focus: specificFocus
  });
};

/**
 * Get available roles
 * 
 * @returns {Promise} API response with available roles
 */
export const getRoles = () => {
  return apiClient.get('/api/roles');
};

/**
 * Check codebase processing status
 * 
 * @param {string} codebaseId - Codebase ID
 * @returns {Promise} API response with processing status
 */
export const getCodebaseStatus = (codebaseId) => {
  return apiClient.get(`/api/status/${codebaseId}`);
};

export default {
  uploadCodebase,
  cloneRepository,
  getInsights,
  getRoles,
  getCodebaseStatus
};