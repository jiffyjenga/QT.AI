import { useEffect, useRef, useState, useCallback } from 'react';

// WebSocket URL from environment variables
const WS_URL = `ws://${import.meta.env.VITE_API_URL?.replace(/^https?:\/\//, '') || 'localhost:8000'}/ws`;

// Message type enum
export enum MessageType {
  MARKET_DATA = 'market_data',
  TRADE_UPDATE = 'trade_update',
  PORTFOLIO_UPDATE = 'portfolio_update',
  STRATEGY_UPDATE = 'strategy_update',
  ERROR = 'error',
}

// WebSocket connection status
export type ConnectionStatus = 'Connecting' | 'Open' | 'Closing' | 'Closed' | 'Error';

// WebSocket hook options
interface WebSocketOptions {
  url?: string;
  reconnectInterval?: number;
  reconnectAttempts?: number;
  onOpen?: (event: Event) => void;
  onClose?: (event: CloseEvent) => void;
  onMessage?: (event: MessageEvent) => void;
  onError?: (event: Event) => void;
}

// WebSocket hook return type
interface WebSocketHook {
  sendMessage: (data: string | object) => void;
  lastMessage: MessageEvent | null;
  connectionStatus: ConnectionStatus;
  reconnect: () => void;
}

/**
 * Custom hook for WebSocket connection
 */
export const useWebSocket = (options: WebSocketOptions = {}): WebSocketHook => {
  const {
    url = WS_URL,
    reconnectInterval = 5000,
    reconnectAttempts = 10,
    onOpen,
    onClose,
    onMessage,
    onError,
  } = options;

  const [lastMessage, setLastMessage] = useState<MessageEvent | null>(null);
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>('Closed');
  const reconnectCount = useRef(0);
  const ws = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<number | null>(null);

  // Get auth token for WebSocket connection
  const getAuthToken = () => {
    return localStorage.getItem('token') || '';
  };

  // Connect to WebSocket
  const connect = useCallback(() => {
    // Close existing connection
    if (ws.current) {
      ws.current.close();
    }

    // Create new WebSocket connection with auth token
    const token = getAuthToken();
    const wsUrl = `${url}${token ? `?token=${token}` : ''}`;
    
    try {
      setConnectionStatus('Connecting');
      ws.current = new WebSocket(wsUrl);

      // Connection opened
      ws.current.onopen = (event: Event) => {
        setConnectionStatus('Open');
        reconnectCount.current = 0;
        if (onOpen) onOpen(event);
      };

      // Connection closed
      ws.current.onclose = (event: CloseEvent) => {
        setConnectionStatus('Closed');
        if (onClose) onClose(event);
        
        // Attempt to reconnect
        if (reconnectCount.current < reconnectAttempts) {
          reconnectCount.current += 1;
          if (reconnectTimeoutRef.current) window.clearTimeout(reconnectTimeoutRef.current);
          reconnectTimeoutRef.current = window.setTimeout(() => {
            connect();
          }, reconnectInterval);
        }
      };

      // Message received
      ws.current.onmessage = (event: MessageEvent) => {
        setLastMessage(event);
        if (onMessage) onMessage(event);
      };

      // Error occurred
      ws.current.onerror = (event: Event) => {
        setConnectionStatus('Error');
        if (onError) onError(event);
        
        // Close connection on error
        if (ws.current) {
          ws.current.close();
        }
      };
    } catch (error) {
      console.error('WebSocket connection error:', error);
      setConnectionStatus('Error');
    }
  }, [url, reconnectInterval, reconnectAttempts, onOpen, onClose, onMessage, onError]);

  // Send message to WebSocket
  const sendMessage = useCallback((data: string | object) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      const message = typeof data === 'string' ? data : JSON.stringify(data);
      ws.current.send(message);
    } else {
      console.error('WebSocket is not connected');
    }
  }, []);

  // Reconnect to WebSocket
  const reconnect = useCallback(() => {
    reconnectCount.current = 0;
    connect();
  }, [connect]);

  // Connect on mount and disconnect on unmount
  useEffect(() => {
    connect();

    return () => {
      if (reconnectTimeoutRef.current) {
        window.clearTimeout(reconnectTimeoutRef.current);
      }
      
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [connect]);

  return {
    sendMessage,
    lastMessage,
    connectionStatus,
    reconnect,
  };
};

/**
 * Hook for market data WebSocket
 */
export const useMarketDataWebSocket = (symbol?: string): WebSocketHook & { marketData: any | null } => {
  const [marketData, setMarketData] = useState<any | null>(null);
  
  const handleMessage = useCallback((event: MessageEvent) => {
    try {
      const data = JSON.parse(event.data);
      
      if (data.type === MessageType.MARKET_DATA) {
        // If symbol is specified, only update for that symbol
        if (!symbol || data.payload.symbol === symbol) {
          setMarketData(data.payload);
        }
      }
    } catch (error) {
      console.error('Error parsing market data:', error);
    }
  }, [symbol]);
  
  const wsHook = useWebSocket({
    onMessage: handleMessage,
  });
  
  // Subscribe to market data on connect
  useEffect(() => {
    if (wsHook.connectionStatus === 'Open') {
      wsHook.sendMessage({
        action: 'subscribe',
        channel: 'market_data',
        symbol: symbol || 'all',
      });
    }
  }, [wsHook.connectionStatus, wsHook.sendMessage, symbol]);
  
  return {
    ...wsHook,
    marketData,
  };
};

/**
 * Hook for trade updates WebSocket
 */
export const useTradeWebSocket = (): WebSocketHook & { tradeUpdate: any | null } => {
  const [tradeUpdate, setTradeUpdate] = useState<any | null>(null);
  
  const handleMessage = useCallback((event: MessageEvent) => {
    try {
      const data = JSON.parse(event.data);
      
      if (data.type === MessageType.TRADE_UPDATE) {
        setTradeUpdate(data.payload);
      }
    } catch (error) {
      console.error('Error parsing trade update:', error);
    }
  }, []);
  
  const wsHook = useWebSocket({
    onMessage: handleMessage,
  });
  
  // Subscribe to trade updates on connect
  useEffect(() => {
    if (wsHook.connectionStatus === 'Open') {
      wsHook.sendMessage({
        action: 'subscribe',
        channel: 'trade_updates',
      });
    }
  }, [wsHook.connectionStatus, wsHook.sendMessage]);
  
  return {
    ...wsHook,
    tradeUpdate,
  };
};

export default useWebSocket;
