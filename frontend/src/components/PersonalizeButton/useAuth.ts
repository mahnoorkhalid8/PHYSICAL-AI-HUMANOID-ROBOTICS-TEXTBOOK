import { useState, useEffect, useContext, createContext } from 'react';

// Define the user type with background information
interface User {
  id: string;
  email: string;
  name?: string;
  image?: string;
  // Extended fields for personalization
  software_background?: string;
  hardware_background?: string;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  getToken: () => Promise<string | null>;
  refreshToken: () => Promise<string | null>;
}

// Create auth context with default value
const defaultAuthContextValue: AuthContextType = {
  user: null,
  isLoading: true,
  isAuthenticated: false,
  getToken: async () => null,
  refreshToken: async () => null
};

const AuthContext = createContext<AuthContextType>(defaultAuthContextValue);

// Helper function to decode JWT token and check expiration
const isTokenExpired = (token: string): boolean => {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const currentTime = Math.floor(Date.now() / 1000);
    // Check if token expires within 5 minutes (to allow for refresh)
    return payload.exp < currentTime + 5 * 60;
  } catch (error) {
    console.error('Error decoding token:', error);
    return true;
  }
};

// Function to verify token with backend
const verifyTokenWithBackend = async (token: string): Promise<boolean> => {
  try {
    const response = await fetch('/api/auth/verify', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    });

    return response.ok;
  } catch (error) {
    console.error('Error verifying token with backend:', error);
    return false;
  }
};

// Mock auth provider component (to be replaced with real Better Auth implementation)
export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Simulate checking auth status on mount
  useEffect(() => {
    const checkAuth = async () => {
      // Check if user is logged in (in a real app, this would check for valid session/cookie)
      const storedUser = localStorage.getItem('better-auth-user');
      let storedToken = localStorage.getItem('better-auth-token');

      if (storedUser && storedToken) {
        // First check if token is expired
        if (isTokenExpired(storedToken)) {
          storedToken = await refreshToken();
          if (!storedToken) {
            // If refresh failed, clear auth data
            localStorage.removeItem('better-auth-token');
            localStorage.removeItem('better-auth-user');
            setUser(null);
            setIsAuthenticated(false);
            setIsLoading(false);
            return;
          }
        } else {
          // Even if not expired, verify with backend to ensure it hasn't been revoked
          const isValid = await verifyTokenWithBackend(storedToken);
          if (!isValid) {
            // Token is not valid according to backend, clear auth data
            localStorage.removeItem('better-auth-token');
            localStorage.removeItem('better-auth-user');
            setUser(null);
            setIsAuthenticated(false);
            setIsLoading(false);
            return;
          }
        }

        setUser(JSON.parse(storedUser));
        setIsAuthenticated(true);
      } else {
        setUser(null);
        setIsAuthenticated(false);
      }
      setIsLoading(false);
    };

    checkAuth();
  }, []);

  // Get user token, refresh if expired
  const getToken = async (): Promise<string | null> => {
    let token = localStorage.getItem('better-auth-token');

    if (!token) {
      return null;
    }

    // Check if token is expired and refresh if needed
    if (isTokenExpired(token)) {
      token = await refreshToken();
    } else {
      // Even if not expired, verify with backend to ensure it hasn't been revoked
      const isValid = await verifyTokenWithBackend(token);
      if (!isValid) {
        // Token is not valid according to backend, clear auth data and return null
        localStorage.removeItem('better-auth-token');
        localStorage.removeItem('better-auth-user');
        setUser(null);
        setIsAuthenticated(false);
        return null;
      }
    }

    return token;
  };

  // Refresh token by generating a new one
  const refreshToken = async (): Promise<string | null> => {
    try {
      // In a real implementation, this would call an API endpoint to refresh the token
      // For now, we'll use a mock token generation or fetch from a server endpoint
      // that generates fresh tokens with 30-minute expiration

      // Check if we have a valid user to generate a new token for
      const storedUser = localStorage.getItem('better-auth-user');
      if (!storedUser) {
        return null;
      }

      // In a real scenario, this would be an API call to a refresh endpoint
      // For now, we'll return the same token but this is where you'd implement
      // the actual token refresh logic
      console.log('Token refresh needed - in a real app, this would call an API endpoint');

      // For demonstration, let's assume we have a function to get a fresh token
      // This would typically involve calling your backend's token refresh endpoint
      // or calling a function to generate a new token from the server
      const freshToken = await fetchFreshToken();

      if (freshToken) {
        localStorage.setItem('better-auth-token', freshToken);
        return freshToken;
      }

      return null;
    } catch (error) {
      console.error('Error refreshing token:', error);
      return null;
    }
  };

  // Function to fetch a fresh token from the backend
  const fetchFreshToken = async (): Promise<string | null> => {
    // Get the current token to send as authorization for refresh
    const currentToken = localStorage.getItem('better-auth-token');

    if (!currentToken) {
      console.error('No current token available for refresh');
      return null;
    }

    try {
      // For Docusaurus, use relative URLs to work with proxy configuration
      // This allows the request to go through the Docusaurus proxy to the backend
      const refreshUrl = '/api/auth/refresh';

      const response = await fetch(refreshUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${currentToken}`  // Send current token for verification
        }
      });

      if (response.ok) {
        const data = await response.json();
        return data.token;
      } else {
        const errorData = await response.json();
        console.error('Token refresh failed:', errorData.detail || 'Unknown error');

        // If refresh failed due to invalid/expired token, we might need to log the user out
        if (response.status === 401) {
          localStorage.removeItem('better-auth-token');
          localStorage.removeItem('better-auth-user');
        }

        return null;
      }
    } catch (error) {
      console.error('Network error during token refresh:', error);
      return null;
    }
  };

  const authContextValue: AuthContextType = {
    user,
    isLoading,
    isAuthenticated,
    getToken,
    refreshToken
  };

  return (
    <AuthContext.Provider value={authContextValue}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use auth context
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  // Since we provided a default value, context will never be undefined
  return context;
};

// Additional helper functions for authentication
export const useAuthState = () => {
  const { user, isLoading, isAuthenticated } = useAuth();

  return {
    user,
    isLoading,
    isAuthenticated,
    isLoggedIn: isAuthenticated,
    isLoggedOut: !isAuthenticated && !isLoading
  };
};