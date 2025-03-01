import React, { useState, useEffect } from 'react';
import Input from '../common/Input';
import Button from '../common/Button';
import Select from '../common/Select';
import { accountAPI } from '../../services/api';

interface ApiKeyManagementProps {
  onApiKeyUpdate: () => void;
}

const ApiKeyManagement: React.FC<ApiKeyManagementProps> = ({ onApiKeyUpdate }) => {
  const [exchange, setExchange] = useState<string>('binance');
  const [apiKey, setApiKey] = useState<string>('');
  const [apiSecret, setApiSecret] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [savedKeys, setSavedKeys] = useState<any[]>([]);

  // Exchange options
  const exchangeOptions = [
    { value: 'binance', label: 'Binance' },
    { value: 'coinbase', label: 'Coinbase Pro' },
    { value: 'kraken', label: 'Kraken' },
    { value: 'kucoin', label: 'KuCoin' },
    { value: 'ftx', label: 'FTX' },
    { value: 'bybit', label: 'Bybit' },
    { value: 'huobi', label: 'Huobi' },
    { value: 'okx', label: 'OKX' },
    { value: 'interactive_brokers', label: 'Interactive Brokers' },
    { value: 'alpaca', label: 'Alpaca' },
    { value: 'td_ameritrade', label: 'TD Ameritrade' },
    { value: 'robinhood', label: 'Robinhood' },
  ];

  // Fetch saved API keys on component mount
  useEffect(() => {
    const fetchApiKeys = async () => {
      try {
        setLoading(true);
        const response = await accountAPI.getApiKeys();
        setSavedKeys(response.data);
        setLoading(false);
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to fetch API keys');
        setLoading(false);
      }
    };

    fetchApiKeys();
  }, []);

  // Handle save API key
  const handleSaveApiKey = async () => {
    // Validate input
    if (!exchange) {
      setError('Please select an exchange');
      return;
    }

    if (!apiKey) {
      setError('API key is required');
      return;
    }

    if (!apiSecret) {
      setError('API secret is required');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      // Call API to save API key
      await accountAPI.saveApiKey(exchange, apiKey, apiSecret);
      
      // Show success message
      setSuccess(`Successfully saved API key for ${exchange}`);
      
      // Reset form
      setApiKey('');
      setApiSecret('');
      
      // Refresh API keys
      const response = await accountAPI.getApiKeys();
      setSavedKeys(response.data);
      
      // Notify parent component
      onApiKeyUpdate();
      
      setLoading(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save API key');
      setLoading(false);
    }
  };

  // Handle delete API key
  const handleDeleteApiKey = async (keyId: string) => {
    try {
      setLoading(true);
      setError(null);
      
      // Call API to delete API key
      await accountAPI.deleteApiKey(keyId);
      
      // Show success message
      setSuccess('Successfully deleted API key');
      
      // Refresh API keys
      const response = await accountAPI.getApiKeys();
      setSavedKeys(response.data);
      
      // Notify parent component
      onApiKeyUpdate();
      
      setLoading(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete API key');
      setLoading(false);
    }
  };

  // Handle test API key
  const handleTestApiKey = async (keyId: string) => {
    try {
      setLoading(true);
      setError(null);
      
      // Call API to test API key
      const response = await accountAPI.testApiKey(keyId);
      
      // Show success message
      setSuccess(response.data.message || 'API key test successful');
      
      setLoading(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'API key test failed');
      setLoading(false);
    }
  };

  return (
    <div>
      <h3 className="text-lg font-medium mb-3">API Key Management</h3>
      <p className="text-gray-600 mb-4">
        Securely store your exchange API keys for automated trading.
      </p>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          <p>{error}</p>
          <button
            className="text-sm underline"
            onClick={() => setError(null)}
          >
            Dismiss
          </button>
        </div>
      )}
      
      {success && (
        <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
          <p>{success}</p>
          <button
            className="text-sm underline"
            onClick={() => setSuccess(null)}
          >
            Dismiss
          </button>
        </div>
      )}
      
      <div className="bg-white border border-gray-200 rounded-md p-4 mb-6">
        <h4 className="text-md font-medium mb-3">Add New API Key</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Select
            id="exchange"
            label="Exchange"
            value={exchange}
            onChange={(e) => setExchange(e.target.value)}
            options={exchangeOptions}
            required
          />
          
          <Input
            id="apiKey"
            label="API Key"
            type="text"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="Enter your API key"
            required
          />
          
          <Input
            id="apiSecret"
            label="API Secret"
            type="password"
            value={apiSecret}
            onChange={(e) => setApiSecret(e.target.value)}
            placeholder="Enter your API secret"
            required
          />
          
          <div className="flex items-end">
            <Button
              onClick={handleSaveApiKey}
              disabled={loading}
              className="w-full"
            >
              {loading ? 'Saving...' : 'Save API Key'}
            </Button>
          </div>
        </div>
      </div>
      
      {/* Saved API Keys */}
      <div className="bg-white border border-gray-200 rounded-md p-4 mb-6">
        <h4 className="text-md font-medium mb-3">Saved API Keys</h4>
        
        {savedKeys.length === 0 ? (
          <p className="text-gray-500 italic">No API keys saved yet</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Exchange
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    API Key (masked)
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Added On
                  </th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {savedKeys.map((key) => (
                  <tr key={key.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {key.exchange}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {key.masked_key}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(key.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <div className="flex space-x-2">
                        <Button
                          onClick={() => handleTestApiKey(key.id)}
                          variant="outline"
                          size="sm"
                          disabled={loading}
                        >
                          Test
                        </Button>
                        <Button
                          onClick={() => handleDeleteApiKey(key.id)}
                          variant="danger"
                          size="sm"
                          disabled={loading}
                        >
                          Delete
                        </Button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
      
      <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4">
        <h4 className="text-sm font-medium text-yellow-800 mb-2">Security Information</h4>
        <p className="text-sm text-yellow-700">
          Your API keys are encrypted and stored securely. We recommend using API keys with read-only or trading-only permissions, and not withdrawal permissions.
          Always follow the exchange's security best practices when creating API keys.
        </p>
      </div>
    </div>
  );
};

export default ApiKeyManagement;
