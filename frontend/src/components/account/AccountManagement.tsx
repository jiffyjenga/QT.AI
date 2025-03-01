import React, { useState, useEffect } from 'react';
import { accountAPI } from '../../services/api';
import Button from '../common/Button';
import Input from '../common/Input';
import AccountOverview from './AccountOverview';
import TransactionHistory from './TransactionHistory';
import TradingAllocation from './TradingAllocation';

interface AccountManagementProps {
  // Props can be added as needed
}

const AccountManagement: React.FC<AccountManagementProps> = () => {
  const [account, setAccount] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [depositAmount, setDepositAmount] = useState<string>('');
  const [withdrawAmount, setWithdrawAmount] = useState<string>('');
  const [depositError, setDepositError] = useState<string | null>(null);
  const [withdrawError, setWithdrawError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [depositSuccess, setDepositSuccess] = useState<string | null>(null);
  const [withdrawSuccess, setWithdrawSuccess] = useState<string | null>(null);

  // Fetch account data
  const fetchAccountData = async () => {
    try {
      setLoading(true);
      const response = await accountAPI.getMyAccount();
      setAccount(response.data);
      setLoading(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch account data');
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAccountData();
  }, []);

  // Handle deposit
  const handleDeposit = async () => {
    // Validate input
    if (!depositAmount || isNaN(parseFloat(depositAmount)) || parseFloat(depositAmount) <= 0) {
      setDepositError('Please enter a valid amount greater than zero');
      return;
    }

    try {
      setLoading(true);
      const response = await accountAPI.depositFunds(parseFloat(depositAmount));
      setAccount(response.data);
      setDepositAmount('');
      setDepositError(null);
      setDepositSuccess(`Successfully deposited ${parseFloat(depositAmount)} ${account.currency}`);
      setLoading(false);
    } catch (err: any) {
      setDepositError(err.response?.data?.detail || 'Failed to deposit funds');
      setLoading(false);
    }
  };

  // Handle withdrawal
  const handleWithdraw = async () => {
    // Validate input
    if (!withdrawAmount || isNaN(parseFloat(withdrawAmount)) || parseFloat(withdrawAmount) <= 0) {
      setWithdrawError('Please enter a valid amount greater than zero');
      return;
    }

    try {
      setLoading(true);
      const response = await accountAPI.withdrawFunds(parseFloat(withdrawAmount));
      setAccount(response.data);
      setWithdrawAmount('');
      setWithdrawError(null);
      setWithdrawSuccess(`Successfully withdrew ${parseFloat(withdrawAmount)} ${account.currency}`);
      setLoading(false);
    } catch (err: any) {
      setWithdrawError(err.response?.data?.detail || 'Failed to withdraw funds');
      setLoading(false);
    }
  };

  // Handle amount change with validation
  const handleAmountChange = (setter: React.Dispatch<React.SetStateAction<string>>, value: string) => {
    // Allow only numbers and decimal point
    if (value === '' || /^\d*\.?\d*$/.test(value)) {
      setter(value);
    }
  };

  // Render tab content
  const renderTabContent = () => {
    switch (activeTab) {
      case 'overview':
        return (
          <div className="space-y-8">
            <AccountOverview account={account} loading={loading} />
            
            {/* Deposit and Withdraw */}
            <div>
              <h3 className="text-lg font-medium mb-3">Manage Funds</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Deposit */}
                <div className="border border-gray-200 rounded-md p-4">
                  <h4 className="text-md font-medium mb-2">Deposit Funds</h4>
                  {depositSuccess && (
                    <div className="bg-green-100 border border-green-400 text-green-700 px-3 py-2 rounded mb-3 text-sm">
                      <p>{depositSuccess}</p>
                      <button
                        className="text-xs underline"
                        onClick={() => setDepositSuccess(null)}
                      >
                        Dismiss
                      </button>
                    </div>
                  )}
                  <div className="flex space-x-2">
                    <Input
                      id="depositAmount"
                      label=""
                      type="text"
                      value={depositAmount}
                      onChange={(e) => handleAmountChange(setDepositAmount, e.target.value)}
                      placeholder="Enter amount"
                      error={depositError || ''}
                      className="mb-0"
                    />
                    <Button
                      onClick={handleDeposit}
                      disabled={loading}
                      className="mt-auto"
                    >
                      Deposit
                    </Button>
                  </div>
                </div>
                
                {/* Withdraw */}
                <div className="border border-gray-200 rounded-md p-4">
                  <h4 className="text-md font-medium mb-2">Withdraw Funds</h4>
                  {withdrawSuccess && (
                    <div className="bg-green-100 border border-green-400 text-green-700 px-3 py-2 rounded mb-3 text-sm">
                      <p>{withdrawSuccess}</p>
                      <button
                        className="text-xs underline"
                        onClick={() => setWithdrawSuccess(null)}
                      >
                        Dismiss
                      </button>
                    </div>
                  )}
                  <div className="flex space-x-2">
                    <Input
                      id="withdrawAmount"
                      label=""
                      type="text"
                      value={withdrawAmount}
                      onChange={(e) => handleAmountChange(setWithdrawAmount, e.target.value)}
                      placeholder="Enter amount"
                      error={withdrawError || ''}
                      className="mb-0"
                    />
                    <Button
                      onClick={handleWithdraw}
                      disabled={loading}
                      variant="outline"
                      className="mt-auto"
                    >
                      Withdraw
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        );
      case 'allocation':
        return (
          <TradingAllocation 
            account={account} 
            onAllocationComplete={fetchAccountData} 
          />
        );
      case 'history':
        return (
          <TransactionHistory 
            accountId={account?.id || ''} 
            currency={account?.currency || 'USD'} 
          />
        );
      default:
        return <div>Unknown tab</div>;
    }
  };

  if (loading && !account) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error && !account) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
        <p>{error}</p>
        <button
          className="text-sm underline"
          onClick={() => {
            setError(null);
            fetchAccountData();
          }}
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="bg-white shadow-md rounded-lg p-6">
      <h2 className="text-xl font-semibold mb-6">Account Management</h2>
      
      {/* Tab Navigation */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="-mb-px flex space-x-8">
          <button
            className={`pb-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'overview'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
            onClick={() => setActiveTab('overview')}
          >
            Overview
          </button>
          <button
            className={`pb-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'allocation'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
            onClick={() => setActiveTab('allocation')}
          >
            Trading Allocation
          </button>
          <button
            className={`pb-4 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'history'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
            onClick={() => setActiveTab('history')}
          >
            Transaction History
          </button>
        </nav>
      </div>
      
      {/* Tab Content */}
      {renderTabContent()}
    </div>
  );
};

export default AccountManagement;
