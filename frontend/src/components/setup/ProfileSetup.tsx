import React, { useState, useEffect } from 'react';
import Input from '../common/Input';
import Button from '../common/Button';
import Select from '../common/Select';

interface ProfileSetupProps {
  initialData: any;
  onComplete: (data: any) => void;
  loading: boolean;
}

const ProfileSetup: React.FC<ProfileSetupProps> = ({
  initialData,
  onComplete,
  loading,
}) => {
  const [fullName, setFullName] = useState<string>('');
  const [preferredCurrency, setPreferredCurrency] = useState<string>('USD');
  const [errors, setErrors] = useState<{ [key: string]: string }>({});

  // Load initial data if available
  useEffect(() => {
    if (initialData) {
      setFullName(initialData.full_name || '');
      setPreferredCurrency(initialData.preferred_currency || 'USD');
    }
  }, [initialData]);

  // Validate form
  const validateForm = (): boolean => {
    const newErrors: { [key: string]: string } = {};

    if (!fullName.trim()) {
      newErrors.fullName = 'Full name is required';
    }

    if (!preferredCurrency) {
      newErrors.preferredCurrency = 'Preferred currency is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle form submission
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (validateForm()) {
      onComplete({
        full_name: fullName,
        preferred_currency: preferredCurrency,
      });
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
      <h2 className="text-xl font-semibold mb-4">Profile Setup</h2>
      <p className="text-gray-600 mb-6">
        Please provide your personal information to get started with QT.AI.
      </p>

      <form onSubmit={handleSubmit}>
        <Input
          id="fullName"
          label="Full Name"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          placeholder="Enter your full name"
          error={errors.fullName}
          required
        />

        <Select
          id="preferredCurrency"
          label="Preferred Currency"
          value={preferredCurrency}
          onChange={(e) => setPreferredCurrency(e.target.value)}
          options={currencyOptions}
          error={errors.preferredCurrency}
          required
        />

        <div className="mt-6 flex justify-end">
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

export default ProfileSetup;
