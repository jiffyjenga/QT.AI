import { useState, useEffect } from 'react';
import { authAPI } from '../services/api';

export const useAuth = () => {
  // Auto-authenticate without requiring login
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(true);
  const [user, setUser] = useState<any>({
    id: 'auto-user',
    email: 'auto@qtai.test',
    username: 'auto_user',
    full_name: 'Auto User',
    role: 'user',
    setup_completed: true
  });
  const [loading, setLoading] = useState<boolean>(false);
  const [setupCompleted, setSetupCompleted] = useState<boolean>(true);

  // No need to check authentication on mount since we're auto-authenticated
  useEffect(() => {
    // Set a dummy token to ensure API calls work
    if (!localStorage.getItem('token')) {
      localStorage.setItem('token', 'auto-authenticated-token');
    }
    
    // Nothing else to do here since we're auto-authenticated
  }, []);

  // Login function - always returns true for direct access
  const login = async (email: string, password: string): Promise<boolean> => {
    // No need to make actual API call since we're auto-authenticated
    console.log('Auto-login successful');
    return true;
  };

  // Logout function
  const logout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
    setUser(null);
    setSetupCompleted(false);
  };

  // Register function
  const register = async (userData: any): Promise<boolean> => {
    try {
      await authAPI.register(userData);
      return true;
    } catch (error) {
      console.error('Registration error:', error);
      return false;
    }
  };

  // Complete setup function
  const completeSetup = () => {
    setSetupCompleted(true);
  };

  return {
    isAuthenticated,
    user,
    loading,
    setupCompleted,
    login,
    logout,
    register,
    completeSetup
  };
};
