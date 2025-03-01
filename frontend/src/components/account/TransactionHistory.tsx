import React, { useState, useEffect } from 'react';

interface Transaction {
  id: string;
  account_id: string;
  amount: number;
  transaction_type: string;
  status: string;
  created_at: string;
  asset_type?: string;
  asset_id?: string;
  notes?: string;
}

interface TransactionHistoryProps {
  accountId: string;
  currency: string;
}

const TransactionHistory: React.FC<TransactionHistoryProps> = ({ accountId, currency }) => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Mock transactions for demonstration
  useEffect(() => {
    // In a real implementation, this would fetch from the API
    const mockTransactions: Transaction[] = [
      {
        id: '1',
        account_id: accountId,
        amount: 1000,
        transaction_type: 'deposit',
        status: 'completed',
        created_at: new Date().toISOString(),
        notes: 'Initial deposit',
      },
      {
        id: '2',
        account_id: accountId,
        amount: 250,
        transaction_type: 'allocation',
        status: 'completed',
        created_at: new Date(Date.now() - 86400000).toISOString(),
        asset_type: 'crypto',
        asset_id: 'BTC',
        notes: 'Allocated for Bitcoin trading',
      },
      {
        id: '3',
        account_id: accountId,
        amount: 100,
        transaction_type: 'withdrawal',
        status: 'completed',
        created_at: new Date(Date.now() - 172800000).toISOString(),
        notes: 'User withdrawal',
      },
    ];

    // Simulate API call
    setTimeout(() => {
      setTransactions(mockTransactions);
      setLoading(false);
    }, 1000);
  }, [accountId]);

  // Format currency
  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency || 'USD',
    }).format(amount);
  };

  // Format date
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  // Get transaction type badge color
  const getTransactionTypeColor = (type: string) => {
    switch (type) {
      case 'deposit':
        return 'bg-green-100 text-green-800';
      case 'withdrawal':
        return 'bg-red-100 text-red-800';
      case 'allocation':
        return 'bg-blue-100 text-blue-800';
      case 'deallocation':
        return 'bg-purple-100 text-purple-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="animate-pulse">
        <div className="h-6 bg-gray-200 rounded w-1/4 mb-4"></div>
        <div className="space-y-3">
          <div className="h-12 bg-gray-200 rounded"></div>
          <div className="h-12 bg-gray-200 rounded"></div>
          <div className="h-12 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  if (error) {
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
    <div>
      <h3 className="text-lg font-medium mb-3">Transaction History</h3>
      
      {transactions.length === 0 ? (
        <div className="text-center py-8 bg-gray-50 rounded-md">
          <p className="text-gray-500">No transactions found</p>
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Date
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Type
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Amount
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Notes
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {transactions.map((transaction) => (
                <tr key={transaction.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {formatDate(transaction.created_at)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getTransactionTypeColor(transaction.transaction_type)}`}>
                      {transaction.transaction_type.charAt(0).toUpperCase() + transaction.transaction_type.slice(1)}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {formatCurrency(transaction.amount)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                      transaction.status === 'completed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {transaction.status.charAt(0).toUpperCase() + transaction.status.slice(1)}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {transaction.notes || '-'}
                    {transaction.asset_type && transaction.asset_id && (
                      <span className="ml-1 text-xs text-gray-400">
                        ({transaction.asset_type}: {transaction.asset_id})
                      </span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default TransactionHistory;
