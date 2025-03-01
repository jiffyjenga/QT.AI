import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { setupAPI } from '../../services/api';
import ProfileSetup from './ProfileSetup';
import SecuritySetup from './SecuritySetup';
import TradingPreferencesSetup from './TradingPreferencesSetup';
import AccountFundingSetup from './AccountFundingSetup';
import SetupConfirmation from './SetupConfirmation';
import { useAuthContext } from '../../App';

const SetupWizard: React.FC = () => {
  const navigate = useNavigate();
  const { completeSetup } = useAuthContext();
  const [currentStep, setCurrentStep] = useState<string>('profile');
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [setupData, setSetupData] = useState<any>({
    profile: {},
    security: {},
    trading_preferences: {},
    account_funding: {},
  });
  const [wizardState, setWizardState] = useState<any>(null);

  // Fetch setup status on component mount
  useEffect(() => {
    const fetchSetupStatus = async () => {
      try {
        setLoading(true);
        const response = await setupAPI.getStatus();
        const { data } = response;
        
        setWizardState(data);
        setCurrentStep(data.current_step);
        
        // If setup is already completed, redirect to dashboard
        if (data.completed) {
          navigate('/dashboard');
        }
        
        // Extract data from steps
        data.steps.forEach((step: any) => {
          if (step.completed && step.data) {
            setSetupData((prev: any) => ({
              ...prev,
              [step.step]: step.data,
            }));
          }
        });
        
        setLoading(false);
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to fetch setup status');
        setLoading(false);
      }
    };
    
    fetchSetupStatus();
  }, [navigate]);

  // Handle step completion
  const handleStepComplete = async (step: string, data: any) => {
    try {
      setLoading(true);
      let response;
      
      // Update setup data
      setSetupData((prev: any) => ({
        ...prev,
        [step]: data,
      }));
      
      // Call appropriate API based on step
      switch (step) {
        case 'profile':
          response = await setupAPI.setupProfile(data);
          break;
        case 'security':
          response = await setupAPI.setupSecurity(data);
          break;
        case 'trading_preferences':
          response = await setupAPI.setupTradingPreferences(data);
          break;
        case 'account_funding':
          response = await setupAPI.setupAccountFunding(data);
          break;
        case 'confirmation':
          response = await setupAPI.completeSetup();
          // Update auth context and redirect to dashboard after completion
          completeSetup();
          navigate('/dashboard');
          break;
        default:
          break;
      }
      
      // Update wizard state and current step
      if (response) {
        setWizardState(response.data);
        setCurrentStep(response.data.current_step);
      }
      
      setLoading(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || `Failed to complete ${step} setup`);
      setLoading(false);
    }
  };

  // Render current step
  const renderStep = () => {
    switch (currentStep) {
      case 'profile':
        return (
          <ProfileSetup
            initialData={setupData.profile}
            onComplete={(data) => handleStepComplete('profile', data)}
            loading={loading}
          />
        );
      case 'security':
        return (
          <SecuritySetup
            initialData={setupData.security}
            onComplete={(data) => handleStepComplete('security', data)}
            loading={loading}
          />
        );
      case 'trading_preferences':
        return (
          <TradingPreferencesSetup
            initialData={setupData.trading_preferences}
            onComplete={(data) => handleStepComplete('trading_preferences', data)}
            loading={loading}
          />
        );
      case 'account_funding':
        return (
          <AccountFundingSetup
            initialData={setupData.account_funding}
            onComplete={(data) => handleStepComplete('account_funding', data)}
            loading={loading}
          />
        );
      case 'confirmation':
        return (
          <SetupConfirmation
            setupData={setupData}
            onComplete={() => handleStepComplete('confirmation', {})}
            loading={loading}
          />
        );
      default:
        return <div>Unknown step</div>;
    }
  };

  if (loading && !wizardState) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">QT.AI Setup Wizard</h1>
        <p className="text-gray-600">Complete the setup to start using QT.AI Trading Bot</p>
      </div>
      
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
      
      {/* Progress indicator */}
      <div className="mb-8">
        <div className="flex justify-between">
          {wizardState?.steps.map((step: any, index: number) => (
            <div
              key={step.step}
              className={`flex flex-col items-center ${index < wizardState.steps.length - 1 ? 'w-1/5' : ''}`}
            >
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center ${
                  step.completed
                    ? 'bg-green-500 text-white'
                    : currentStep === step.step
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-200 text-gray-600'
                }`}
              >
                {index + 1}
              </div>
              <div className="text-xs mt-1 text-center">{step.step.replace('_', ' ')}</div>
              {index < wizardState.steps.length - 1 && (
                <div
                  className={`h-1 w-full mt-3 ${
                    step.completed ? 'bg-green-500' : 'bg-gray-200'
                  }`}
                ></div>
              )}
            </div>
          ))}
        </div>
      </div>
      
      {/* Current step content */}
      <div className="bg-white shadow-md rounded-lg p-6">
        {renderStep()}
      </div>
    </div>
  );
};

export default SetupWizard;
