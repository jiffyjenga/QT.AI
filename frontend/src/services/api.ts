import axios from 'axios';

// Create axios instance with base URL
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Auth API
export const authAPI = {
  login: (email: string, password: string) => 
    api.post('/token', { username: email, password }),
  register: (userData: any) => 
    api.post('/users', userData),
  getCurrentUser: () => 
    api.get('/users/me'),
};

// Setup Wizard API
export const setupAPI = {
  getStatus: () => 
    api.get('/setup/status'),
  setupProfile: (profileData: any) => 
    api.post('/setup/profile', profileData),
  setupSecurity: (securityData: any) => 
    api.post('/setup/security', securityData),
  setupTradingPreferences: (preferencesData: any) => 
    api.post('/setup/trading_preferences', preferencesData),
  setupAccountFunding: (fundingData: any) => 
    api.post('/setup/account_funding', fundingData),
  completeSetup: () => 
    api.post('/setup/complete'),
  resetSetup: () => 
    api.post('/setup/reset'),
};

// Account API
export const accountAPI = {
  getMyAccount: () => 
    api.get('/accounts/me'),
  updateAccount: (accountData: any) => 
    api.put('/accounts/me', accountData),
  depositFunds: (amount: number) => 
    api.post('/accounts/me/deposit', { amount }),
  withdrawFunds: (amount: number) => 
    api.post('/accounts/me/withdraw', { amount }),
  allocateFunds: (amount: number, assetType: string, assetId?: string) => 
    api.post('/accounts/me/allocate', { amount, asset_type: assetType, asset_id: assetId }),
  deallocateFunds: (amount: number, assetType: string, assetId?: string) => 
    api.post('/accounts/me/deallocate', { amount, asset_type: assetType, asset_id: assetId }),
};

export default api;
