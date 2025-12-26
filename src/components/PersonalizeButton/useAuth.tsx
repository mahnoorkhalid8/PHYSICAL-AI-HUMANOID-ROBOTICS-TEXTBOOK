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
}

// Create auth context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Mock auth provider component (to be replaced with real Better Auth implementation)
export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Simulate checking auth status on mount
  useEffect(() => {
    const checkAuth = () => {
      // Check if user is logged in (in a real app, this would check for valid session/cookie)
      const storedUser = localStorage.getItem('better-auth-user');
      const storedToken = localStorage.getItem('better-auth-token');

      if (storedUser && storedToken) {
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

  // Get user token
  const getToken = async (): Promise<string | null> => {
    // In a real implementation, this would get the JWT token from Better Auth
    const token = localStorage.getItem('better-auth-token');

    // Basic validation of token format (JWT tokens have 3 parts separated by dots)
    if (token && typeof token === 'string') {
      const parts = token.split('.');
      if (parts.length === 3) {
        // Token has correct JWT format, return it
        return token;
      } else {
        // Token is malformed, clear it from storage
        localStorage.removeItem('better-auth-token');
        return null;
      }
    }

    return token;
  };

  const authContextValue: AuthContextType = {
    user,
    isLoading,
    isAuthenticated,
    getToken
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
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
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