import React, { useState, useEffect } from 'react';
import Input from '../common/Input';
import Button from '../common/Button';
import Select from '../common/Select';

interface AccountFundingSetupProps {
  initialData: any;
  onComplete: (data: any) => void;
  loading: boolean;
}

const AccountFundingSetup: React.FC<AccountFundingSetupProps> = ({
  initialData,
  onComplete,
  loading,
}) => {
  const [initialDeposit, setInitialDeposit] = useState<string>('1000');
  const [currency, setCurrency] = useState<string>('USD');
  const [errors, setErrors] = useState<{ [key: string]: string }>({});

  // Load initial data if available
  useEffect(() => {
    if (initialData) {
      setInitialDeposit(initialData.initial_deposit?.toString() || '1000');
      setCurrency(initialData.currency || 'USD');
    }
  }, [initialData]);

  // Validate form
  const validateForm = (): boolean => {
    const newErrors: { [key: string]: string } = {};
    const depositAmount = parseFloat(initialDeposit);

    if (isNaN(depositAmount)) {
      newErrors.initialDeposit = 'Initial deposit must be a valid number';
    } else if (depositAmount <= 0) {
      newErrors.initialDeposit = 'Initial deposit must be greater than zero';
    }

    if (!currency) {
      newErrors.currency = 'Currency is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle form submission
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (validateForm()) {
      onComplete({
        initial_deposit: parseFloat(initialDeposit),
        currency: currency,
      });
    }
  };

  // Handle input change for initial deposit
  const handleDepositChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    // Allow only numbers and decimal point
    if (value === '' || /^\d*\.?\d*$/.test(value)) {
      setInitialDeposit(value);
    }
  };

  const currencyOptions = [
    { value: 'USD', label: 'US Dollar (USD)' },
    { value: 'EUR', label: 'Euro (EUR)' },
    { value: 'GBP', label: 'British Pound (GBP)' },
    { value: 'JPY', label: 'Japanese Yen (JPY)' },
    { value: 'AUD', label: 'Australian Dollar (AUD)' },
    { value: 'CAD', label: 'Canadian Dollar (CAD)' },
    { value: 'CHF', label: 'Swiss Franc (CHF)' },
    { value: 'CNY', label: 'Chinese Yuan (CNY)' },
  ];

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Account Funding</h2>
      <p className="text-gray-600 mb-6">
        Set up your initial trading budget. This amount will be used for trading operations.
      </p>

      <form onSubmit={handleSubmit}>
        <Input
          id="initialDeposit"
          label="Initial Deposit"
          type="text"
          value={initialDeposit}
          onChange={handleDepositChange}
          placeholder="Enter initial deposit amount"
          error={errors.initialDeposit}
          required
        />

        <Select
          id="currency"
          label="Currency"
          value={currency}
          onChange={(e) => setCurrency(e.target.value)}
          options={currencyOptions}
          error={errors.currency}
          required
        />

        <div className="mt-6">
          <div className="bg-blue-50 border border-blue-200 rounded-md p-4 mb-6">
            <h3 className="text-sm font-medium text-blue-800 mb-2">Important Information</h3>
            <p className="text-sm text-blue-700">
              The initial deposit amount will be used to fund your trading account. You can add or withdraw funds later from your account dashboard.
            </p>
          </div>
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
            type="submit"
            disabled={loading}
          >
            {loading ? 'Saving...' : 'Continue'}
          </Button>
        </div>
      </form>
    </div>
  );
};

export default AccountFundingSetup;
