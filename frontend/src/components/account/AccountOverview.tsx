import React from 'react';

interface AccountOverviewProps {
  account: any;
  loading: boolean;
}

const AccountOverview: React.FC<AccountOverviewProps> = ({ account, loading }) => {
  // Format currency
  const formatCurrency = (amount: number, currency: string = 'USD') => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency,
    }).format(amount);
  };

  if (loading) {
    return (
      <div className="animate-pulse">
        <div className="h-6 bg-gray-200 rounded w-1/4 mb-2"></div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="h-24 bg-gray-200 rounded"></div>
          <div className="h-24 bg-gray-200 rounded"></div>
          <div className="h-24 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  return (
    <div>
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
  );
};

export default AccountOverview;
