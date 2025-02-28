import apiClient from './apiClient';

// Types
export interface Trade {
  id: number;
  symbol: string;
  type: 'BUY' | 'SELL';
  amount: number;
  price: number;
  value: number;
  fee: number;
  status: string;
  exchange: string;
  order_id: string | null;
  user_id: number;
  strategy_id: number | null;
  created_at: string;
  updated_at: string | null;
}

export interface TradeCreate {
  symbol: string;
  type: 'BUY' | 'SELL';
  amount: number;
  price: number;
  exchange: string;
  strategy_id?: number;
}

export interface TradeHistoryParams {
  limit?: number;
  offset?: number;
  symbol?: string;
  strategy_id?: number;
  type?: 'BUY' | 'SELL';
  status?: string;
  start_date?: string;
  end_date?: string;
}

export interface TradeHistoryResponse {
  trades: Trade[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

// Trade service
const tradeService = {
  // Create new trade
  createTrade: async (trade: TradeCreate): Promise<Trade> => {
    const response = await apiClient.post<Trade>('/trades', trade);
    return response;
  },
  
  // Get trade history
  getTradeHistory: async (params?: TradeHistoryParams): Promise<TradeHistoryResponse> => {
    const response = await apiClient.get<TradeHistoryResponse>('/trades', { params });
    return response;
  },
  
  // Get trade by ID
  getTrade: async (id: number): Promise<Trade> => {
    const response = await apiClient.get<Trade>(`/trades/${id}`);
    return response;
  },
};

export default tradeService;
