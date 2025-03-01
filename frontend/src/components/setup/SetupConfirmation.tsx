import React from 'react';
import Button from '../common/Button';

interface SetupConfirmationProps {
  setupData: any;
  onComplete: () => void;
  loading: boolean;
}

const SetupConfirmation: React.FC<SetupConfirmationProps> = ({
  setupData,
  onComplete,
  loading,
}) => {
  // Format currency
  const formatCurrency = (amount: number, currency: string) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency || 'USD',
    }).format(amount);
  };

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Setup Confirmation</h2>
      <p className="text-gray-600 mb-6">
        Please review your setup information before completing the process.
      </p>

      <div className="space-y-6">
        {/* Profile Information */}
        <div className="bg-white border border-gray-200 rounded-md p-4">
          <h3 className="text-lg font-medium text-gray-900 mb-2">Profile Information</h3>
          <div className="grid grid-cols-2 gap-2">
            <div className="text-sm text-gray-500">Full Name</div>
            <div className="text-sm text-gray-900">{setupData.profile?.full_name || 'Not provided'}</div>
            
            <div className="text-sm text-gray-500">Preferred Currency</div>
            <div className="text-sm text-gray-900">{setupData.profile?.preferred_currency || 'USD'}</div>
          </div>
        </div>

        {/* Security Settings */}
        <div className="bg-white border border-gray-200 rounded-md p-4">
          <h3 className="text-lg font-medium text-gray-900 mb-2">Security Settings</h3>
          <div className="grid grid-cols-2 gap-2">
            <div className="text-sm text-gray-500">Two-Factor Authentication</div>
            <div className="text-sm text-gray-900">
              {setupData.security?.two_factor_enabled ? 'Enabled' : 'Disabled'}
            </div>
            
            {setupData.security?.two_factor_enabled && (
              <>
                <div className="text-sm text-gray-500">Authentication Method</div>
                <div className="text-sm text-gray-900">
                  {setupData.security?.two_factor_method === 'app' && 'Authenticator App'}
                  {setupData.security?.two_factor_method === 'sms' && 'SMS'}
                  {setupData.security?.two_factor_method === 'email' && 'Email'}
                </div>
              </>
            )}
          </div>
        </div>

        {/* Trading Preferences */}
        <div className="bg-white border border-gray-200 rounded-md p-4">
          <h3 className="text-lg font-medium text-gray-900 mb-2">Trading Preferences</h3>
          <div className="grid grid-cols-2 gap-2">
            <div className="text-sm text-gray-500">Risk Tolerance</div>
            <div className="text-sm text-gray-900">
              {setupData.trading_preferences?.risk_tolerance === 'low' && 'Low (Conservative)'}
              {setupData.trading_preferences?.risk_tolerance === 'medium' && 'Medium (Balanced)'}
              {setupData.trading_preferences?.risk_tolerance === 'high' && 'High (Aggressive)'}
            </div>
            
            <div className="text-sm text-gray-500">Preferred Assets</div>
            <div className="text-sm text-gray-900">
              {setupData.trading_preferences?.preferred_assets?.join(', ') || 'None selected'}
            </div>
            
            <div className="text-sm text-gray-500">Trading Frequency</div>
            <div className="text-sm text-gray-900">
              {setupData.trading_preferences?.trading_frequency === 'daily' && 'Daily'}
              {setupData.trading_preferences?.trading_frequency === 'weekly' && 'Weekly'}
              {setupData.trading_preferences?.trading_frequency === 'monthly' && 'Monthly'}
            </div>
            
            <div className="text-sm text-gray-500">Automated Trading</div>
            <div className="text-sm text-gray-900">
              {setupData.trading_preferences?.auto_trading_enabled ? 'Enabled' : 'Disabled'}
            </div>
          </div>
        </div>

        {/* Account Funding */}
        <div className="bg-white border border-gray-200 rounded-md p-4">
          <h3 className="text-lg font-medium text-gray-900 mb-2">Account Funding</h3>
          <div className="grid grid-cols-2 gap-2">
            <div className="text-sm text-gray-500">Initial Deposit</div>
            <div className="text-sm text-gray-900">
              {setupData.account_funding?.initial_deposit
                ? formatCurrency(
                    setupData.account_funding.initial_deposit,
                    setupData.account_funding.currency
                  )
                : 'Not provided'}
            </div>
            
            <div className="text-sm text-gray-500">Currency</div>
            <div className="text-sm text-gray-900">{setupData.account_funding?.currency || 'USD'}</div>
          </div>
        </div>
      </div>

      <div className="mt-8 bg-blue-50 border border-blue-200 rounded-md p-4 mb-6">
        <h3 className="text-sm font-medium text-blue-800 mb-2">Important Information</h3>
        <p className="text-sm text-blue-700">
          By completing the setup, you agree to the terms and conditions of QT.AI Trading Bot.
          You can modify these settings later from your account dashboard.
        </p>
      </div>

      <div className="mt-6 flex justify-between">
        <Button
          type="button"
          variant="outline"
          onClick={() => window.history.back()}
        >
          Back
        </Button>
        <Button
          type="button"
          onClick={onComplete}
          disabled={loading}
        >
          {loading ? 'Completing Setup...' : 'Complete Setup'}
        </Button>
      </div>
    </div>
  );
};

export default SetupConfirmation;
