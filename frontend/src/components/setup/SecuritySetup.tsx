import React, { useState, useEffect } from 'react';
import Checkbox from '../common/Checkbox';
import Button from '../common/Button';
import Select from '../common/Select';

interface SecuritySetupProps {
  initialData: any;
  onComplete: (data: any) => void;
  loading: boolean;
}

const SecuritySetup: React.FC<SecuritySetupProps> = ({
  initialData,
  onComplete,
  loading,
}) => {
  const [twoFactorEnabled, setTwoFactorEnabled] = useState<boolean>(false);
  const [twoFactorMethod, setTwoFactorMethod] = useState<string>('none');
  const [errors, setErrors] = useState<{ [key: string]: string }>({});

  // Load initial data if available
  useEffect(() => {
    if (initialData) {
      setTwoFactorEnabled(initialData.two_factor_enabled || false);
      setTwoFactorMethod(initialData.two_factor_method || 'none');
    }
  }, [initialData]);

  // Validate form
  const validateForm = (): boolean => {
    const newErrors: { [key: string]: string } = {};

    if (twoFactorEnabled && twoFactorMethod === 'none') {
      newErrors.twoFactorMethod = 'Please select a two-factor authentication method';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle form submission
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (validateForm()) {
      onComplete({
        two_factor_enabled: twoFactorEnabled,
        two_factor_method: twoFactorEnabled ? twoFactorMethod : 'none',
      });
    }
  };

  const twoFactorOptions = [
    { value: 'app', label: 'Authenticator App' },
    { value: 'sms', label: 'SMS' },
    { value: 'email', label: 'Email' },
  ];

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Security Setup</h2>
      <p className="text-gray-600 mb-6">
        Configure your security settings to protect your QT.AI account.
      </p>

      <form onSubmit={handleSubmit}>
        <Checkbox
          id="twoFactorEnabled"
          label="Enable Two-Factor Authentication (Recommended)"
          checked={twoFactorEnabled}
          onChange={(e) => setTwoFactorEnabled(e.target.checked)}
        />

        {twoFactorEnabled && (
          <Select
            id="twoFactorMethod"
            label="Two-Factor Authentication Method"
            value={twoFactorMethod}
            onChange={(e) => setTwoFactorMethod(e.target.value)}
            options={twoFactorOptions}
            error={errors.twoFactorMethod}
            required
          />
        )}

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

export default SecuritySetup;
