import apiClient from './apiClient';

// Types
export interface RiskSettings {
  id: number;
  max_position_size: number;
  max_daily_loss: number;
  max_drawdown: number;
  stop_loss_percent: number;
  take_profit_percent: number;
  confirm_trades: boolean;
  user_id: number;
  created_at: string;
  updated_at: string | null;
}

export interface RiskSettingsUpdate {
  max_position_size?: number;
  max_daily_loss?: number;
  max_drawdown?: number;
  stop_loss_percent?: number;
  take_profit_percent?: number;
  confirm_trades?: boolean;
}

export interface ApiKey {
  id: number;
  exchange: string;
  api_key: string;
  api_secret: string;
  is_active: boolean;
  user_id: number;
  created_at: string;
  updated_at: string | null;
}

export interface ApiKeyCreate {
  exchange: string;
  api_key: string;
  api_secret: string;
}

// Settings service
const settingsService = {
  // Get risk settings
  getRiskSettings: async (): Promise<RiskSettings> => {
    const response = await apiClient.get<RiskSettings>('/settings/risk');
    return response;
  },
  
  // Update risk settings
  updateRiskSettings: async (settings: RiskSettingsUpdate): Promise<RiskSettings> => {
    const response = await apiClient.put<RiskSettings>('/settings/risk', settings);
    return response;
  },
  
  // Get API keys
  getApiKeys: async (): Promise<ApiKey[]> => {
    const response = await apiClient.get<ApiKey[]>('/settings/api-keys');
    return response;
  },
  
  // Create API key
  createApiKey: async (apiKey: ApiKeyCreate): Promise<ApiKey> => {
    const response = await apiClient.post<ApiKey>('/settings/api-keys', apiKey);
    return response;
  },
  
  // Delete API key
  deleteApiKey: async (id: number): Promise<void> => {
    await apiClient.delete(`/settings/api-keys/${id}`);
  },
};

export default settingsService;
