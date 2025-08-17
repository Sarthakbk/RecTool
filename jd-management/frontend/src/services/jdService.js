import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

const jdService = {
  // Job Description CRUD operations
  getAllJobs: async () => {
    const response = await api.get('/api/jd');
    return response.data;
  },

  getJobById: async (id) => {
    const response = await api.get(`/api/jd/${id}`);
    return response.data;
  },

  createJob: async (jobData) => {
    const response = await api.post('/api/jd', jobData);
    return response.data;
  },

  updateJob: async (id, jobData) => {
    const response = await api.put(`/api/jd/${id}`, jobData);
    return response.data;
  },

  deleteJob: async (id) => {
    const response = await api.delete(`/api/jd/${id}`);
    return response.data;
  },

  updateAging: async () => {
    const response = await api.post('/api/jd/update-aging');
    return response.data;
  },

  // Reference data endpoints
  getCategories: async () => {
    const response = await api.get('/api/categories');
    return response.data;
  },

  getModes: async () => {
    const response = await api.get('/api/modes');
    return response.data;
  },

  getStatuses: async () => {
    const response = await api.get('/api/statuses');
    return response.data;
  },

  getUsers: async () => {
    const response = await api.get('/api/users');
    return response.data;
  },

  getCurrencies: async () => {
    const response = await api.get('/api/currencies');
    return response.data;
  },

  // Health check
  healthCheck: async () => {
    const response = await api.get('/health');
    return response.data;
  },

  // JD Scanning and Analysis
  scanJobDescription: async (jdText) => {
    const response = await api.post('/api/jd/scan', { jd_text: jdText });
    return response.data;
  },

  // Utility methods
  formatSkills: (skills) => {
    if (!skills) return 'N/A';
    try {
      const skillsArray = typeof skills === 'string' ? JSON.parse(skills) : skills;
      return Array.isArray(skillsArray) ? skillsArray.join(', ') : 'N/A';
    } catch {
      return skills || 'N/A';
    }
  },

  formatKeywords: (keywords) => {
    if (!keywords) return 'N/A';
    try {
      const keywordsArray = typeof keywords === 'string' ? JSON.parse(keywords) : keywords;
      return Array.isArray(keywordsArray) ? keywordsArray.join(', ') : 'N/A';
    } catch {
      return keywords || 'N/A';
    }
  },

  // Validation methods
  validateJobData: (data) => {
    const errors = [];
    
    if (!data.jd_title?.trim()) {
      errors.push('Job Title is required');
    }
    
    if (!data.jd_customer_id) {
      errors.push('Customer ID is required');
    }
    
    if (!data.jd_consumer?.trim()) {
      errors.push('Consumer is required');
    }
    
    if (!data.jd_original?.trim()) {
      errors.push('Original Job Description is required');
    }
    
    if (!data.jd_skillset?.length) {
      errors.push('At least one skill is required');
    }
    
    if (!data.jd_mode) {
      errors.push('Job Mode is required');
    }
    
    if (!data.jd_tenure || data.jd_tenure < 1) {
      errors.push('Valid Tenure is required');
    }
    
    if (!data.jd_op_exp_min || data.jd_op_exp_min < 0) {
      errors.push('Valid Minimum Experience is required');
    }
    
    if (!data.jd_op_exp_max || data.jd_op_exp_max < data.jd_op_exp_min) {
      errors.push('Valid Maximum Experience is required and must be greater than minimum');
    }
    
    if (!data.jd_op_budget_min || data.jd_op_budget_min < 0) {
      errors.push('Valid Minimum Budget is required');
    }
    
    if (!data.jd_op_budget_max || data.jd_op_budget_max < data.jd_op_budget_min) {
      errors.push('Valid Maximum Budget is required and must be greater than minimum');
    }
    
    if (!data.jd_created_by) {
      errors.push('Created By is required');
    }
    
    return {
      isValid: errors.length === 0,
      errors
    };
  }
};

export default jdService; 