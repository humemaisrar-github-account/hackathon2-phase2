/**
 * Example API client demonstrating all required functionality for the Todo application
 */

// Base URL for the API
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000';

/**
 * Helper function to make authenticated requests
 */
async function makeAuthenticatedRequest(endpoint, options = {}, token) {
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`,
    ...options.headers,
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || errorData.message || 'Request failed');
  }

  return response.json();
}

/**
 * Authentication functions
 */

// Sign up a new user
export async function signUp(email, password) {
  const response = await fetch('/api/auth/sign-up', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.message || 'Sign up failed');
  }

  const result = await response.json();

  // After signing up with BetterAuth, get the JWT token from the backend
  const backendAuthResponse = await fetch(`${API_BASE_URL}/api/auth/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  if (backendAuthResponse.ok) {
    const backendResult = await backendAuthResponse.json();
    return {
      ...result,
      accessToken: backendResult.access_token, // Include backend JWT token
    };
  }

  return result;
}

// Sign in a user
export async function signIn(email, password) {
  const response = await fetch('/api/auth/sign-in', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.message || 'Sign in failed');
  }

  const result = await response.json();

  // After signing in with BetterAuth, get the JWT token from the backend
  const backendAuthResponse = await fetch(`${API_BASE_URL}/api/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  if (backendAuthResponse.ok) {
    const backendResult = await backendAuthResponse.json();
    return {
      ...result,
      accessToken: backendResult.access_token, // Include backend JWT token
    };
  }

  return result;
}

/**
 * Todo API functions
 */

// Get all tasks for a user
export async function getTasks(userId, token) {
  return makeAuthenticatedRequest(`/api/${userId}/tasks`, {}, token);
}

// Create a new task
export async function createTask(userId, title, description, token) {
  return makeAuthenticatedRequest(`/api/${userId}/tasks`, {
    method: 'POST',
    body: JSON.stringify({ title, description }),
  }, token);
}

// Update a task
export async function updateTask(userId, taskId, title, description, token) {
  return makeAuthenticatedRequest(`/api/${userId}/tasks/${taskId}`, {
    method: 'PUT',
    body: JSON.stringify({ title, description }),
  }, token);
}

// Delete a task
export async function deleteTask(userId, taskId, token) {
  return makeAuthenticatedRequest(`/api/${userId}/tasks/${taskId}`, {
    method: 'DELETE',
  }, token);
}

// Toggle completion status of a task
export async function toggleComplete(userId, taskId, token) {
  return makeAuthenticatedRequest(`/api/${userId}/tasks/${taskId}/complete`, {
    method: 'PATCH',
  }, token);
}