import { createContext, useContext, useEffect, useState } from 'react';

// Create Auth Context
const AuthContext = createContext();

// Auth service to manage authentication state
class AuthService {
  constructor() {
    this.currentUser = null;
    this.listeners = [];
    this.init();
  }

  init() {
    // Check for session when service initializes
    this.checkSession();
  }

  async checkSession() {
    try {
      // Construct proper URL for server-side rendering
      const apiUrl = typeof window !== 'undefined'
        ? '/api/auth/get-session'
        : `${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000'}/api/auth/get-session`;

      const response = await fetch(apiUrl);

      // Check if response is JSON before parsing
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        if (response.ok) {
          const data = await response.json();
          if (data.session) {
            this.currentUser = data.session.user;
            this.notifyListeners(this.currentUser);
          }
        }
      } else {
        console.error('Session check returned non-JSON response:', await response.text());
      }
    } catch (error) {
      console.error('Error checking session:', error);
    }
  }

  // Register a listener for auth state changes
  subscribe(listener) {
    this.listeners.push(listener);
    // Return unsubscribe function
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }

  // Notify all listeners of auth state change
  notifyListeners(currentUser) {
    this.listeners.forEach(listener => listener(currentUser));
  }

  // Register a new user (Better Auth handles this via sign-up)
  async register(userData) {
    try {
      let result = null;

      // Try Better Auth registration first
      try {
        // Construct proper URL for server-side rendering
        const apiUrl = typeof window !== 'undefined'
          ? '/api/auth/sign-up'
          : `${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000'}/api/auth/sign-up`;

        const response = await fetch(apiUrl, {
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
          console.error('Non-JSON response received from BetterAuth:', textResponse);
          throw new Error(`Registration failed: Expected JSON but got ${contentType}. Response: ${textResponse.substring(0, 200)}...`);
        }

        result = await response.json();

        if (!response.ok) {
          throw new Error(result.message || 'BetterAuth registration failed');
        }
      } catch (betterAuthError) {
        console.error('BetterAuth registration failed:', betterAuthError);
        // If BetterAuth fails, try direct backend registration as fallback
        const backendResponse = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000'}/api/auth/register`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: userData.email,
            password: userData.password,
          }),
        });

        if (!backendResponse.ok) {
          const errorData = await backendResponse.json();
          throw new Error(errorData.detail || 'Both BetterAuth and backend registration failed');
        }

        result = await backendResponse.json();
      }

      // Update current user after successful registration
      this.currentUser = result.user;
      this.notifyListeners(this.currentUser);

      // After registration, get a JWT token for API calls
      // First try to get session from BetterAuth
      try {
        // Construct proper URL for server-side rendering
        const sessionApiUrl = typeof window !== 'undefined'
          ? '/api/auth/get-session'
          : `${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000'}/api/auth/get-session`;

        const sessionResponse = await fetch(sessionApiUrl);
        if (sessionResponse.ok) {
          const contentType = sessionResponse.headers.get('content-type');
          if (contentType && contentType.includes('application/json')) {
            const sessionData = await sessionResponse.json();
            if (sessionData?.session?.user) {
              // The user is authenticated via BetterAuth
              // Now we need to sync with the backend and get JWT token

              // First, try to get JWT token from backend using email
              try {
                const backendTokenResponse = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000'}/api/auth/token`, {
                  method: 'POST',
                  headers: {
                    'Content-Type': 'application/json',
                  },
                  body: JSON.stringify({
                    email: userData.email,
                  }),
                });

                if (backendTokenResponse.ok) {
                  const backendResult = await backendTokenResponse.json();
                  if (backendResult.access_token) {
                    // Set the JWT token for API requests
                    const { setAuthToken } = await import('./api');
                    setAuthToken(backendResult.access_token);
                  }
                }
              } catch (backendError) {
                console.error('Backend token request after registration failed:', backendError);
              }
            }
          }
        }
      } catch (sessionError) {
        console.error('Session check after registration failed:', sessionError);
      }

      return result;
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  }

  // Login user
  async login(credentials) {
    try {
      // First, try to authenticate with Better Auth
      let betterAuthResult = null;
      try {
        // Construct proper URL for server-side rendering
        const apiUrl = typeof window !== 'undefined'
          ? '/api/auth/sign-in'
          : `${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000'}/api/auth/sign-in`;

        const response = await fetch(apiUrl, {
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
          console.error('Non-JSON response received from BetterAuth:', textResponse);
          throw new Error(`Login failed: Expected JSON but got ${contentType}. Response: ${textResponse.substring(0, 200)}...`);
        }

        betterAuthResult = await response.json();

        if (!response.ok) {
          throw new Error(betterAuthResult.message || 'BetterAuth login failed');
        }
      } catch (betterAuthError) {
        console.error('BetterAuth login failed:', betterAuthError);
        // If BetterAuth fails, try direct backend login as fallback
        const backendResponse = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000'}/api/auth/login`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: credentials.email,
            password: credentials.password,
          }),
        });

        if (!backendResponse.ok) {
          const errorData = await backendResponse.json();
          throw new Error(errorData.detail || 'Both BetterAuth and backend login failed');
        }

        betterAuthResult = await backendResponse.json();
      }

      // Update current user after successful login
      this.currentUser = betterAuthResult.user;
      this.notifyListeners(this.currentUser);

      // Get JWT token from the backend authentication system using email
      const backendResponse = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000'}/api/auth/token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: credentials.email,
        }),
      });

      if (backendResponse.ok) {
        const backendResult = await backendResponse.json();
        if (backendResult.access_token) {
          // Set the JWT token for API requests
          const { setAuthToken } = await import('./api');
          setAuthToken(backendResult.access_token);
        }
      }

      return betterAuthResult;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  }

  // Logout user
  async logout() {
    try {
      let result = {};

      // Try Better Auth sign-out first
      try {
        // Construct proper URL for server-side rendering
        const apiUrl = typeof window !== 'undefined'
          ? '/api/auth/sign-out'
          : `${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000'}/api/auth/sign-out`;

        const response = await fetch(apiUrl, {
          method: 'POST',
        });

        // Check if response is JSON before parsing
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
          result = await response.json();

          if (!response.ok) {
            throw new Error(result.message || 'BetterAuth logout failed');
          }
        } else {
          // If not JSON, try to parse as text and create a basic result
          const textResponse = await response.text();
          result = { success: response.ok, message: textResponse.substring(0, 200) || 'Logged out successfully' };
        }
      } catch (betterAuthError) {
        console.error('BetterAuth logout failed:', betterAuthError);
        // Continue with backend logout even if BetterAuth fails
        result = { success: true, message: 'Logged out successfully' };
      }

      // Clear current user after successful logout
      this.currentUser = null;
      this.notifyListeners(null);

      // Also call backend logout to clear backend session
      try {
        await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000'}/api/auth/logout`, {
          method: 'POST',
        });
      } catch (err) {
        console.error('Backend logout failed:', err);
      }

      // Clear the JWT token
      const { setAuthToken } = await import('./api');
      setAuthToken(null);

      return result;
    } catch (error) {
      console.error('Logout error:', error);
      // Even if backend logout fails, clear local state
      this.currentUser = null;
      this.notifyListeners(null);

      // Clear the JWT token
      const { setAuthToken } = await import('./api');
      setAuthToken(null);

      return { success: true, message: 'Logged out successfully' };
    }
  }

  // Get current user
  getCurrentUser() {
    return this.currentUser;
  }

  // Get current user ID
  getCurrentUserId() {
    return this.currentUser?.id;
  }

  // Check if user is authenticated
  isAuthenticated() {
    return !!this.currentUser;
  }

  // Refresh user token (if needed)
  async refreshToken() {
    await this.checkSession();
    return !!this.currentUser;
  }
}

// Create a singleton instance of the auth service
const authService = new AuthService();

// Export a React hook for using auth state
export const useAuth = () => {
  const [currentUser, setCurrentUser] = useState(authService.getCurrentUser());
  const [loading, setLoading] = useState(!authService.getCurrentUser());

  useEffect(() => {
    // Set initial state
    setCurrentUser(authService.getCurrentUser());
    setLoading(!authService.getCurrentUser());

    // Subscribe to auth state changes
    const unsubscribe = authService.subscribe(setCurrentUser);

    return unsubscribe;
  }, []);

  const value = {
    currentUser,
    loading,
    isAuthenticated: !!currentUser,
    register: authService.register.bind(authService),
    login: authService.login.bind(authService),
    logout: authService.logout.bind(authService),
    refreshToken: authService.refreshToken.bind(authService),
  };

  return value;
};

// Create an AuthProvider component
export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(authService.getCurrentUser());
  const [loading, setLoading] = useState(!authService.getCurrentUser());

  useEffect(() => {
    // Subscribe to auth state changes
    const unsubscribe = authService.subscribe(setCurrentUser);

    return unsubscribe;
  }, []);

  const value = {
    currentUser,
    loading,
    isAuthenticated: !!currentUser,
    register: authService.register.bind(authService),
    login: authService.login.bind(authService),
    logout: authService.logout.bind(authService),
    refreshToken: authService.refreshToken.bind(authService),
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Export the service directly if needed
export default authService;