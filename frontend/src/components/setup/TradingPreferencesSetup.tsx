import React, { useState, useEffect } from 'react';
import Button from '../common/Button';
import Select from '../common/Select';
import Checkbox from '../common/Checkbox';

interface TradingPreferencesSetupProps {
  initialData: any;
  onComplete: (data: any) => void;
  loading: boolean;
}

const TradingPreferencesSetup: React.FC<TradingPreferencesSetupProps> = ({
  initialData,
  onComplete,
  loading,
}) => {
  const [riskTolerance, setRiskTolerance] = useState<string>('medium');
  const [preferredAssets, setPreferredAssets] = useState<string[]>(['crypto']);
  const [tradingFrequency, setTradingFrequency] = useState<string>('daily');
  const [autoTradingEnabled, setAutoTradingEnabled] = useState<boolean>(false);
  const [errors, setErrors] = useState<{ [key: string]: string }>({});

  // Load initial data if available
  useEffect(() => {
    if (initialData) {
      setRiskTolerance(initialData.risk_tolerance || 'medium');
      setPreferredAssets(initialData.preferred_assets || ['crypto']);
      setTradingFrequency(initialData.trading_frequency || 'daily');
      setAutoTradingEnabled(initialData.auto_trading_enabled || false);
    }
  }, [initialData]);

  // Validate form
  const validateForm = (): boolean => {
    const newErrors: { [key: string]: string } = {};

    if (!riskTolerance) {
      newErrors.riskTolerance = 'Risk tolerance is required';
    }

    if (!preferredAssets || preferredAssets.length === 0) {
      newErrors.preferredAssets = 'At least one asset type must be selected';
    }

    if (!tradingFrequency) {
      newErrors.tradingFrequency = 'Trading frequency is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle form submission
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (validateForm()) {
      onComplete({
        risk_tolerance: riskTolerance,
        preferred_assets: preferredAssets,
        trading_frequency: tradingFrequency,
        auto_trading_enabled: autoTradingEnabled,
      });
    }
  };

  // Handle asset selection
  const handleAssetToggle = (asset: string) => {
    if (preferredAssets.includes(asset)) {
      setPreferredAssets(preferredAssets.filter((a) => a !== asset));
    } else {
      setPreferredAssets([...preferredAssets, asset]);
    }
  };

  const riskToleranceOptions = [
    { value: 'low', label: 'Low - Conservative approach with minimal risk' },
    { value: 'medium', label: 'Medium - Balanced approach with moderate risk' },
    { value: 'high', label: 'High - Aggressive approach with higher risk' },
  ];

  const tradingFrequencyOptions = [
    { value: 'daily', label: 'Daily - Multiple trades per day' },
    { value: 'weekly', label: 'Weekly - A few trades per week' },
    { value: 'monthly', label: 'Monthly - A few trades per month' },
  ];

  const assetTypes = [
    { value: 'crypto', label: 'Cryptocurrencies' },
    { value: 'stocks', label: 'Stocks' },
    { value: 'forex', label: 'Forex' },
    { value: 'commodities', label: 'Commodities' },
  ];

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Trading Preferences</h2>
      <p className="text-gray-600 mb-6">
        Configure your trading preferences to customize how QT.AI will trade for you.
      </p>

      <form onSubmit={handleSubmit}>
        <Select
          id="riskTolerance"
          label="Risk Tolerance"
          value={riskTolerance}
          onChange={(e) => setRiskTolerance(e.target.value)}
          options={riskToleranceOptions}
          error={errors.riskTolerance}
          required
        />

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Preferred Asset Types
            {errors.preferredAssets && (
              <span className="text-red-500 ml-1">{errors.preferredAssets}</span>
            )}
          </label>
          <div className="space-y-2">
            {assetTypes.map((asset) => (
              <Checkbox
                key={asset.value}
                id={`asset-${asset.value}`}
                label={asset.label}
                checked={preferredAssets.includes(asset.value)}
                onChange={() => handleAssetToggle(asset.value)}
              />
            ))}
          </div>
        </div>

        <Select
          id="tradingFrequency"
          label="Trading Frequency"
          value={tradingFrequency}
          onChange={(e) => setTradingFrequency(e.target.value)}
          options={tradingFrequencyOptions}
          error={errors.tradingFrequency}
          required
        />

        <Checkbox
          id="autoTradingEnabled"
          label="Enable Automated Trading"
          checked={autoTradingEnabled}
          onChange={(e) => setAutoTradingEnabled(e.target.checked)}
        />

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

export default TradingPreferencesSetup;
