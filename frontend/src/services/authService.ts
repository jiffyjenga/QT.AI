import apiClient from './apiClient';

// Types
export interface User {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// Auth service
const authService = {
  // Login user
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    // Convert to form data format for token endpoint
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    
    const response = await apiClient.post<AuthResponse>('/auth/token', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    // Store token in localStorage
    localStorage.setItem('token', response.access_token);
    
    return response;
  },
  
  // Register new user
  register: async (data: RegisterData): Promise<User> => {
    const response = await apiClient.post<User>('/auth/register', data);
    return response;
  },
  
  // Logout user
  logout: (): void => {
    localStorage.removeItem('token');
  },
  
  // Get current user
  getCurrentUser: async (): Promise<User> => {
    const response = await apiClient.get<User>('/users/me');
    return response;
  },
  
  // Check if user is authenticated
  isAuthenticated: (): boolean => {
    return !!localStorage.getItem('token');
  },
};

export default authService;
