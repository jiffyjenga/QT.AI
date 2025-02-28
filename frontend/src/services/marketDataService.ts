import apiClient from './apiClient';

// Types
export interface OHLCVData {
  timestamp: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface MarketSummary {
  symbol: string;
  price: number;
  change24h: number;
  high24h: number;
  low24h: number;
  volume24h: number;
}

export interface OrderBookEntry {
  price: number;
  amount: number;
}

export interface OrderBook {
  symbol: string;
  bids: [number, number][];  // [price, amount]
  asks: [number, number][];  // [price, amount]
  timestamp: number;
}

// Market data service
const marketDataService = {
  // Get OHLCV data
  getOHLCV: async (
    symbol: string,
    timeframe: string = '1h',
    limit: number = 100,
    since?: number
  ): Promise<OHLCVData[]> => {
    const params: Record<string, string | number> = {
      symbol,
      timeframe,
      limit,
    };
    
    if (since) {
      params.since = since;
    }
    
    const response = await apiClient.get<OHLCVData[]>('/market/ohlcv', { params });
    return response;
  },
  
  // Get market summaries
  getMarketSummaries: async (symbols?: string[]): Promise<MarketSummary[]> => {
    const params: Record<string, string> = {};
    
    if (symbols && symbols.length > 0) {
      params.symbols = symbols.join(',');
    }
    
    const response = await apiClient.get<MarketSummary[]>('/market/summaries', { params });
    return response;
  },
  
  // Get ticker for a symbol
  getTicker: async (symbol: string): Promise<any> => {
    const response = await apiClient.get<any>(`/market/ticker/${symbol}`);
    return response;
  },
  
  // Get order book for a symbol
  getOrderBook: async (symbol: string, limit: number = 20): Promise<OrderBook> => {
    const response = await apiClient.get<OrderBook>(`/market/orderbook/${symbol}`, {
      params: { limit },
    });
    return response;
  },
};

export default marketDataService;
