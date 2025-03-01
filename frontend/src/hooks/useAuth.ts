import { useState, useEffect } from 'react';
import { authAPI } from '../services/api';

export const useAuth = () => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [setupCompleted, setSetupCompleted] = useState<boolean>(false);

  // Check if user is authenticated on mount
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('token');
      
      if (token) {
        try {
          const response = await authAPI.getCurrentUser();
          setUser(response.data);
          setIsAuthenticated(true);
          setSetupCompleted(response.data.setup_completed || false);
        } catch (error) {
          console.error('Error checking authentication:', error);
          localStorage.removeItem('token');
          setIsAuthenticated(false);
          setUser(null);
        }
      }
      
      setLoading(false);
    };
    
    checkAuth();
  }, []);

  // Login function
  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      const response = await authAPI.login(email, password);
      
      // Store token in localStorage
      localStorage.setItem('token', response.data.access_token);
      
      // Get user data
      const userResponse = await authAPI.getCurrentUser();
      setUser(userResponse.data);
      setIsAuthenticated(true);
      setSetupCompleted(userResponse.data.setup_completed || false);
      
      return true;
    } catch (error) {
      console.error('Login error:', error);
      return false;
    }
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
