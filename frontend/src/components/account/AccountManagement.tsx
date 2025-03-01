import React, { useState, useEffect } from 'react';
import { accountAPI } from '../../services/api';
import Button from '../common/Button';
import Input from '../common/Input';

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

  // Fetch account data
  useEffect(() => {
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
      setLoading(false);
    } catch (err: any) {
      setWithdrawError(err.response?.data?.detail || 'Failed to withdraw funds');
      setLoading(false);
    }
  };

  // Format currency
  const formatCurrency = (amount: number, currency: string = 'USD') => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency,
    }).format(amount);
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
          onClick={() => setError(null)}
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="bg-white shadow-md rounded-lg p-6">
      <h2 className="text-xl font-semibold mb-4">Account Management</h2>
      
      {/* Account Overview */}
      <div className="mb-8">
        <h3 className="text-lg font-medium mb-3">Account Overview</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-blue-50 p-4 rounded-md">
            <div className="text-sm text-blue-600">Total Balance</div>
            <div className="text-2xl font-bold">
              {account ? formatCurrency(account.total_balance, account.currency) : '-'}
            </div>
          </div>
          <div className="bg-green-50 p-4 rounded-md">
            <div className="text-sm text-green-600">Available Balance</div>
            <div className="text-2xl font-bold">
              {account ? formatCurrency(account.available_balance, account.currency) : '-'}
            </div>
          </div>
          <div className="bg-purple-50 p-4 rounded-md">
            <div className="text-sm text-purple-600">Allocated for Trading</div>
            <div className="text-2xl font-bold">
              {account ? formatCurrency(account.allocated_balance, account.currency) : '-'}
            </div>
          </div>
        </div>
      </div>
      
      {/* Deposit and Withdraw */}
      <div className="mb-8">
        <h3 className="text-lg font-medium mb-3">Manage Funds</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Deposit */}
          <div className="border border-gray-200 rounded-md p-4">
            <h4 className="text-md font-medium mb-2">Deposit Funds</h4>
            <div className="flex space-x-2">
              <Input
                id="depositAmount"
                label=""
                type="text"
                value={depositAmount}
                onChange={(e) => setDepositAmount(e.target.value)}
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
            <div className="flex space-x-2">
              <Input
                id="withdrawAmount"
                label=""
                type="text"
                value={withdrawAmount}
                onChange={(e) => setWithdrawAmount(e.target.value)}
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
      
      {/* Trading Allocation */}
      <div>
        <h3 className="text-lg font-medium mb-3">Trading Allocation</h3>
        <p className="text-gray-600 mb-4">
          Allocate funds for trading across different asset classes.
        </p>
        <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4 mb-4">
          <p className="text-sm text-yellow-700">
            Trading allocation functionality will be implemented in the next phase.
          </p>
        </div>
      </div>
    </div>
  );
};

export default AccountManagement;
