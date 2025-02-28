import React, { useEffect, useState } from 'react';
import Layout from '../../components/layout/Layout';
import marketDataService, { MarketSummary } from '../../services/marketDataService';
import strategyService, { Strategy } from '../../services/strategyService';
import tradeService, { Trade } from '../../services/tradeService';
import { useWebSocket, useMarketDataWebSocket } from '../../services/websocketClient';

const Dashboard: React.FC = () => {
  const [marketSummaries, setMarketSummaries] = useState<MarketSummary[]>([]);
  const [strategies, setStrategies] = useState<Strategy[]>([]);
  const [recentTrades, setRecentTrades] = useState<Trade[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // WebSocket for real-time updates
  const { lastMessage } = useWebSocket();
  const { marketData } = useMarketDataWebSocket();
  
  // Fetch initial data
  useEffect(() => {
    const fetchDashboardData = async () => {
      setIsLoading(true);
      setError(null);
      
      try {
        // Fetch market summaries
        const summaries = await marketDataService.getMarketSummaries();
        setMarketSummaries(summaries);
        
        // Fetch active strategies
        const strategiesData = await strategyService.getStrategies();
        setStrategies(strategiesData);
        
        // Fetch recent trades
        const tradesData = await tradeService.getTradeHistory({ limit: 5 });
        setRecentTrades(tradesData.trades);
      } catch (err: any) {
        console.error('Error fetching dashboard data:', err);
        setError('Failed to load dashboard data. Please try again.');
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchDashboardData();
  }, []);
  
  // Handle WebSocket messages
  useEffect(() => {
    if (lastMessage) {
      try {
        const data = JSON.parse(lastMessage.data);
        
        // Update market data
        if (data.type === 'market_data') {
          setMarketSummaries(prevSummaries => {
            const index = prevSummaries.findIndex(s => s.symbol === data.payload.symbol);
            if (index !== -1) {
              const newSummaries = [...prevSummaries];
              newSummaries[index] = { ...data.payload };
              return newSummaries;
            }
            return prevSummaries;
          });
        }
        
        // Update trades
        if (data.type === 'trade_update') {
          setRecentTrades(prevTrades => {
            // Add new trade to the beginning and limit to 5
            return [data.payload, ...prevTrades].slice(0, 5);
          });
        }
        
        // Update strategy status
        if (data.type === 'strategy_update') {
          setStrategies(prevStrategies => {
            const index = prevStrategies.findIndex(s => s.id === data.payload.id);
            if (index !== -1) {
              const newStrategies = [...prevStrategies];
              newStrategies[index] = { ...data.payload };
              return newStrategies;
            }
            return prevStrategies;
          });
        }
      } catch (err) {
        console.error('Error processing WebSocket message:', err);
      }
    }
  }, [lastMessage]);
  
  // Update market data from WebSocket hook
  useEffect(() => {
    if (marketData) {
      setMarketSummaries(prevSummaries => {
        const index = prevSummaries.findIndex(s => s.symbol === marketData.symbol);
        if (index !== -1) {
          const newSummaries = [...prevSummaries];
          newSummaries[index] = { ...marketData };
          return newSummaries;
        }
        return prevSummaries;
      });
    }
  }, [marketData]);
  
  // Format price change
  const formatPriceChange = (change: number) => {
    const isPositive = change >= 0;
    return (
      <span className={`${isPositive ? 'text-green-500' : 'text-red-500'}`}>
        {isPositive ? '+' : ''}{change.toFixed(2)}%
      </span>
    );
  };
  
  // Loading state
  if (isLoading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-full">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
        </div>
      </Layout>
    );
  }
  
  return (
    <Layout>
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-white">Dashboard</h1>
        <p className="text-gray-400 mt-1">
          Overview of your trading activity and market data
        </p>
      </div>
      
      {error && (
        <div className="mb-6 p-4 bg-red-900/20 border border-red-500 text-red-200 rounded-md">
          {error}
        </div>
      )}
      
      {/* Market Summary */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold text-white mb-4">Market Summary</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {marketSummaries.slice(0, 4).map((summary) => (
            <div key={summary.symbol} className="bg-gray-800 rounded-lg p-4">
              <div className="flex justify-between items-center mb-2">
                <h3 className="text-lg font-medium text-white">{summary.symbol}</h3>
                {formatPriceChange(summary.change24h)}
              </div>
              <div className="text-2xl font-bold text-white mb-2">
                ${summary.price.toFixed(2)}
              </div>
              <div className="flex justify-between text-sm text-gray-400">
                <span>Vol: ${summary.volume24h.toLocaleString()}</span>
                <span>H: ${summary.high24h.toFixed(2)}</span>
                <span>L: ${summary.low24h.toFixed(2)}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
      
      {/* Active Strategies */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold text-white mb-4">Active Strategies</h2>
        <div className="bg-gray-800 rounded-lg overflow-hidden">
          {strategies.filter(s => s.is_active).length > 0 ? (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-700">
                <thead className="bg-gray-700">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Name</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Type</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Assets</th>
                    <th className="px-6 py-3 text-center text-xs font-medium text-gray-300 uppercase tracking-wider">Status</th>
                  </tr>
                </thead>
                <tbody className="bg-gray-800 divide-y divide-gray-700">
                  {strategies.filter(s => s.is_active).map((strategy) => (
                    <tr key={strategy.id} className="hover:bg-gray-700">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-white">{strategy.name}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{strategy.type}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{strategy.assets.join(', ')}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-center">
                        <span className="px-2 py-1 rounded-full text-xs bg-green-900/20 text-green-400">
                          Active
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="p-6 text-center text-gray-400">
              No active strategies. Go to the Strategies page to activate or create a strategy.
            </div>
          )}
        </div>
      </div>
      
      {/* Recent Trades */}
      <div>
        <h2 className="text-xl font-semibold text-white mb-4">Recent Trades</h2>
        <div className="bg-gray-800 rounded-lg overflow-hidden">
          {recentTrades.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-700">
                <thead className="bg-gray-700">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Time</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Symbol</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Type</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-300 uppercase tracking-wider">Amount</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-300 uppercase tracking-wider">Price</th>
                    <th className="px-6 py-3 text-center text-xs font-medium text-gray-300 uppercase tracking-wider">Status</th>
                  </tr>
                </thead>
                <tbody className="bg-gray-800 divide-y divide-gray-700">
                  {recentTrades.map((trade) => (
                    <tr key={trade.id} className="hover:bg-gray-700">
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                        {new Date(trade.created_at).toLocaleString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-white">{trade.symbol}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        <span className={`${trade.type === 'BUY' ? 'text-green-500' : 'text-red-500'}`}>
                          {trade.type}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-300">{trade.amount.toFixed(6)}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-300">${trade.price.toFixed(2)}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-center">
                        <span className={`px-2 py-1 rounded-full text-xs ${
                          trade.status === 'COMPLETED' 
                            ? 'bg-green-900/20 text-green-400' 
                            : trade.status === 'PENDING' 
                              ? 'bg-yellow-900/20 text-yellow-400' 
                              : 'bg-red-900/20 text-red-400'
                        }`}>
                          {trade.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="p-6 text-center text-gray-400">
              No recent trades. Trades will appear here once your strategies start trading.
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
};

export default Dashboard;
