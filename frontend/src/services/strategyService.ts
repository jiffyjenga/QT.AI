import apiClient from './apiClient';

// Types
export interface Strategy {
  id: number;
  name: string;
  description: string;
  type: string;
  assets: string[];
  parameters: Record<string, any>;
  is_active: boolean;
  user_id: number;
  created_at: string;
  updated_at: string | null;
}

export interface StrategyCreate {
  name: string;
  description: string;
  type: string;
  assets: string[];
  parameters: Record<string, any>;
  is_active: boolean;
}

export interface StrategyUpdate {
  name?: string;
  description?: string;
  type?: string;
  assets?: string[];
  parameters?: Record<string, any>;
  is_active?: boolean;
}

export interface StrategyPerformance {
  strategy_id: number;
  strategy_name: string;
  timeframe: string;
  total_trades: number;
  profitable_trades: number;
  win_rate: number;
  profit_loss: number;
  avg_profit: number;
  trades: any[];
}

// Strategy service
const strategyService = {
  // Get all strategies
  getStrategies: async (): Promise<Strategy[]> => {
    const response = await apiClient.get<Strategy[]>('/strategies');
    return response;
  },
  
  // Get strategy by ID
  getStrategy: async (id: number): Promise<Strategy> => {
    const response = await apiClient.get<Strategy>(`/strategies/${id}`);
    return response;
  },
  
  // Create new strategy
  createStrategy: async (strategy: StrategyCreate): Promise<Strategy> => {
    const response = await apiClient.post<Strategy>('/strategies', strategy);
    return response;
  },
  
  // Update strategy
  updateStrategy: async (id: number, strategy: StrategyUpdate): Promise<Strategy> => {
    const response = await apiClient.put<Strategy>(`/strategies/${id}`, strategy);
    return response;
  },
  
  // Delete strategy
  deleteStrategy: async (id: number): Promise<void> => {
    await apiClient.delete(`/strategies/${id}`);
  },
  
  // Toggle strategy active/inactive
  toggleStrategy: async (id: number): Promise<Strategy> => {
    const response = await apiClient.post<Strategy>(`/strategies/${id}/toggle`);
    return response;
  },
  
  // Get strategy performance
  getStrategyPerformance: async (id: number, timeframe: string = 'all'): Promise<StrategyPerformance> => {
    const response = await apiClient.get<StrategyPerformance>(`/strategies/${id}/performance`, {
      params: { timeframe },
    });
    return response;
  },
};

export default strategyService;
