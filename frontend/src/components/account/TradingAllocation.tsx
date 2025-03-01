import React, { useState } from 'react';
import Input from '../common/Input';
import Select from '../common/Select';
import Button from '../common/Button';
import { accountAPI } from '../../services/api';

interface TradingAllocationProps {
  account: any;
  onAllocationComplete: () => void;
}

const TradingAllocation: React.FC<TradingAllocationProps> = ({ account, onAllocationComplete }) => {
  const [amount, setAmount] = useState<string>('');
  const [assetType, setAssetType] = useState<string>('crypto');
  const [assetId, setAssetId] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // Asset type options
  const assetTypeOptions = [
    { value: 'crypto', label: 'Cryptocurrency' },
    { value: 'stocks', label: 'Stocks' },
    { value: 'forex', label: 'Forex' },
    { value: 'commodities', label: 'Commodities' },
  ];

  // Asset ID options based on asset type
  const getAssetIdOptions = () => {
    switch (assetType) {
      case 'crypto':
        return [
          { value: 'BTC', label: 'Bitcoin (BTC)' },
          { value: 'ETH', label: 'Ethereum (ETH)' },
          { value: 'SOL', label: 'Solana (SOL)' },
          { value: 'ADA', label: 'Cardano (ADA)' },
        ];
      case 'stocks':
        return [
          { value: 'AAPL', label: 'Apple Inc. (AAPL)' },
          { value: 'MSFT', label: 'Microsoft Corp. (MSFT)' },
          { value: 'GOOGL', label: 'Alphabet Inc. (GOOGL)' },
          { value: 'AMZN', label: 'Amazon.com Inc. (AMZN)' },
        ];
      case 'forex':
        return [
          { value: 'EUR/USD', label: 'Euro/US Dollar (EUR/USD)' },
          { value: 'GBP/USD', label: 'British Pound/US Dollar (GBP/USD)' },
          { value: 'USD/JPY', label: 'US Dollar/Japanese Yen (USD/JPY)' },
          { value: 'USD/CHF', label: 'US Dollar/Swiss Franc (USD/CHF)' },
        ];
      case 'commodities':
        return [
          { value: 'GOLD', label: 'Gold (XAU)' },
          { value: 'SILVER', label: 'Silver (XAG)' },
          { value: 'OIL', label: 'Crude Oil (WTI)' },
          { value: 'NATGAS', label: 'Natural Gas' },
        ];
      default:
        return [];
    }
  };

  // Handle amount change
  const handleAmountChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    // Allow only numbers and decimal point
    if (value === '' || /^\d*\.?\d*$/.test(value)) {
      setAmount(value);
    }
  };

  // Handle allocation
  const handleAllocate = async () => {
    // Validate input
    if (!amount || isNaN(parseFloat(amount)) || parseFloat(amount) <= 0) {
      setError('Please enter a valid amount greater than zero');
      return;
    }

    if (!assetType) {
      setError('Please select an asset type');
      return;
    }

    if (!assetId) {
      setError('Please select an asset');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      // Call API to allocate funds
      await accountAPI.allocateFunds(parseFloat(amount), assetType, assetId);
      
      // Show success message
      setSuccess(`Successfully allocated ${amount} ${account.currency} for ${assetType} trading`);
      
      // Reset form
      setAmount('');
      
      // Notify parent component to refresh account data
      onAllocationComplete();
      
      setLoading(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to allocate funds');
      setLoading(false);
    }
  };

  // Handle deallocation
  const handleDeallocate = async () => {
    // Validate input
    if (!amount || isNaN(parseFloat(amount)) || parseFloat(amount) <= 0) {
      setError('Please enter a valid amount greater than zero');
      return;
    }

    if (!assetType) {
      setError('Please select an asset type');
      return;
    }

    if (!assetId) {
      setError('Please select an asset');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      // Call API to deallocate funds
      await accountAPI.deallocateFunds(parseFloat(amount), assetType, assetId);
      
      // Show success message
      setSuccess(`Successfully deallocated ${amount} ${account.currency} from ${assetType} trading`);
      
      // Reset form
      setAmount('');
      
      // Notify parent component to refresh account data
      onAllocationComplete();
      
      setLoading(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to deallocate funds');
      setLoading(false);
    }
  };

  return (
    <div>
      <h3 className="text-lg font-medium mb-3">Trading Allocation</h3>
      <p className="text-gray-600 mb-4">
        Allocate funds for trading across different asset classes.
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
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input
            id="allocationAmount"
            label="Amount"
            type="text"
            value={amount}
            onChange={handleAmountChange}
            placeholder={`Enter amount in ${account?.currency || 'USD'}`}
            required
          />
          
          <Select
            id="assetType"
            label="Asset Type"
            value={assetType}
            onChange={(e) => {
              setAssetType(e.target.value);
              setAssetId(''); // Reset asset ID when asset type changes
            }}
            options={assetTypeOptions}
            required
          />
          
          <Select
            id="assetId"
            label="Asset"
            value={assetId}
            onChange={(e) => setAssetId(e.target.value)}
            options={getAssetIdOptions()}
            required
          />
          
          <div className="flex items-end space-x-2">
            <Button
              onClick={handleAllocate}
              disabled={loading}
              className="flex-1"
            >
              Allocate Funds
            </Button>
            
            <Button
              onClick={handleDeallocate}
              disabled={loading}
              variant="outline"
              className="flex-1"
            >
              Deallocate Funds
            </Button>
          </div>
        </div>
      </div>
      
      <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4">
        <h4 className="text-sm font-medium text-yellow-800 mb-2">Important Information</h4>
        <p className="text-sm text-yellow-700">
          Allocated funds will be used for trading operations in the selected asset class.
          You can deallocate funds at any time to return them to your available balance.
        </p>
      </div>
    </div>
  );
};

export default TradingAllocation;
