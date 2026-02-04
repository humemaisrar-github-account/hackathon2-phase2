import axios from 'axios';

// Get the base API URL from environment variables
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

// Store the JWT token
let authToken = null;

// Create an axios instance with base configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Function to set the authentication token
export const setAuthToken = (token) => {
  authToken = token;
  if (token) {
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete apiClient.defaults.headers.common['Authorization'];
  }
};

// Function to get the current token
export const getAuthToken = () => authToken;

// Request interceptor to add authentication token
apiClient.interceptors.request.use(
  async (config) => {
    // If we have an auth token, add it to the request
    if (authToken) {
      config.headers.Authorization = `Bearer ${authToken}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle common error cases
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle specific error responses
    if (error.response?.status === 401) {
      // Token might be expired, redirect to login
      if (typeof window !== 'undefined') {
        // Clear the token
        setAuthToken(null);
        // Redirect to login page
        window.location.href = '/auth/login';
      }
    }

    return Promise.reject(error);
  }
);

// User endpoints
export const userAPI = {
  update: (id, userData) => apiClient.put(`/api/users/${id}`, userData),
};

// Authentication endpoints - these will be handled by Better Auth API routes directly
// So we'll need to extract JWT tokens from the responses
export const authAPI = {
  register: async (userData) => {
    const response = await fetch('/api/auth/sign-up', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: userData.email,
        password: userData.password,
      }),
    });

    // Check if response is JSON before parsing
    const contentType = response.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
      const textResponse = await response.text();
      console.error('Non-JSON response received:', textResponse);
      throw new Error(`Registration failed: Expected JSON but got ${contentType}. Response: ${textResponse.substring(0, 200)}...`);
    }

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Registration failed');
    }

    const result = await response.json();

    // Extract JWT token if provided by BetterAuth
    // For now, we'll assume the existing JWT system from the backend is used
    // This may require adjustment based on actual BetterAuth response

    return result;
  },
  login: async (credentials) => {
    const response = await fetch('/api/auth/sign-in', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: credentials.email,
        password: credentials.password,
      }),
    });

    // Check if response is JSON before parsing
    const contentType = response.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
      const textResponse = await response.text();
      console.error('Non-JSON response received:', textResponse);
      throw new Error(`Login failed: Expected JSON but got ${contentType}. Response: ${textResponse.substring(0, 200)}...`);
    }

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || 'Login failed');
    }

    const result = await response.json();

    // If BetterAuth provides a JWT token in the response, store it
    // Otherwise, we'll need to call a separate endpoint to get the JWT for API calls

    return result;
  },
  logout: async () => {
    const response = await fetch('/api/auth/sign-out', {
      method: 'POST',
    });

    // Check if response is JSON before parsing
    const contentType = response.headers.get('content-type');
    let result = {};
    if (contentType && contentType.includes('application/json')) {
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Logout failed');
      }
      result = await response.json();
    } else {
      // If not JSON, try to parse as text and create a basic result
      const textResponse = await response.text();
      result = { success: response.ok, message: textResponse.substring(0, 200) || 'Logged out successfully' };
    }

    // Clear the stored token
    setAuthToken(null);

    return result;
  },
};

// Todo endpoints - updated to match the API structure
// The userId will be passed from the authenticated user context
export const todoAPI = {
  getAll: (userId, params) => apiClient.get(`/api/${userId}/tasks`, { params }),
  create: (userId, todoData) => apiClient.post(`/api/${userId}/tasks`, todoData),
  update: (userId, id, todoData) => apiClient.put(`/api/${userId}/tasks/${id}`, todoData),
  delete: (userId, id) => apiClient.delete(`/api/${userId}/tasks/${id}`),
  toggleComplete: (userId, id) => apiClient.patch(`/api/${userId}/tasks/${id}/complete`),
};

// Health check endpoint
export const healthAPI = {
  check: () => apiClient.get('/health'),
};

export default apiClient;