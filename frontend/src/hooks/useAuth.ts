import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

interface AuthState {
  isAuthenticated: boolean;
  isLoading: boolean;
  user: any | null;
  setupCompleted: boolean;
}

export const useAuth = () => {
  const [authState, setAuthState] = useState<AuthState>({
    isAuthenticated: false,
    isLoading: true,
    user: null,
    setupCompleted: false
  });
  const navigate = useNavigate();

  useEffect(() => {
    // Check if token exists in localStorage
    const token = localStorage.getItem('token');
    
    if (!token) {
      setAuthState({
        isAuthenticated: false,
        isLoading: false,
        user: null,
        setupCompleted: false
      });
      return;
    }

    // In a real implementation, this would validate the token with the backend
    // and fetch the user data
    // For demo purposes, we'll just set isAuthenticated to true
    
    // Mock user data
    const mockUser = {
      id: 'user123',
      email: 'user@example.com',
      username: 'username',
      setup_completed: true
    };
    
    setAuthState({
      isAuthenticated: true,
      isLoading: false,
      user: mockUser,
      setupCompleted: mockUser.setup_completed
    });
  }, []);

  const login = async (email: string, password: string) => {
    try {
      // In a real implementation, this would call the login API
      // const response = await authAPI.login(email, password);
      // localStorage.setItem('token', response.data.access_token);
      
      // For demo purposes, just set a mock token
      localStorage.setItem('token', 'mock_token');
      
      // Mock user data
      const mockUser = {
        id: 'user123',
        email,
        username: email.split('@')[0],
        setup_completed: false
      };
      
      setAuthState({
        isAuthenticated: true,
        isLoading: false,
        user: mockUser,
        setupCompleted: mockUser.setup_completed
      });
      
      // Redirect based on setup completion
      if (mockUser.setup_completed) {
        navigate('/dashboard');
      } else {
        navigate('/setup');
      }
      
      return true;
    } catch (error) {
      console.error('Login failed:', error);
      return false;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setAuthState({
      isAuthenticated: false,
      isLoading: false,
      user: null,
      setupCompleted: false
    });
    navigate('/login');
  };

  const completeSetup = () => {
    if (authState.user) {
      const updatedUser = {
        ...authState.user,
        setup_completed: true
      };
      
      setAuthState({
        ...authState,
        user: updatedUser,
        setupCompleted: true
      });
    }
  };

  return {
    ...authState,
    login,
    logout,
    completeSetup
  };
};
