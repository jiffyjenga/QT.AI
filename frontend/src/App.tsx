import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import SetupWizard from './components/setup/SetupWizard';

// Placeholder components for other routes
const Login = () => (
  <div className="flex justify-center items-center h-screen">
    <div className="bg-white shadow-md rounded-lg p-8 max-w-md w-full">
      <h1 className="text-2xl font-bold mb-6">Login to QT.AI</h1>
      <p className="text-gray-600 mb-4">Login functionality will be implemented here.</p>
      <button className="bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700">
        Go to Setup Wizard
      </button>
    </div>
  </div>
);

const Dashboard = () => (
  <div className="p-6">
    <h1 className="text-2xl font-bold mb-6">QT.AI Dashboard</h1>
    <p className="text-gray-600 mb-4">Dashboard will be implemented here.</p>
  </div>
);

const App: React.FC = () => {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/setup" element={<SetupWizard />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/" element={<Navigate to="/setup" replace />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
