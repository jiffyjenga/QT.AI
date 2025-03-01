import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import { useAuth } from './hooks/useAuth';

// Create Auth Context
export const AuthContext = React.createContext<ReturnType<typeof useAuth> | null>(null);

// Auth Provider Component
const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const auth = useAuth();
  
  return (
    <AuthContext.Provider value={auth}>
      {children}
    </AuthContext.Provider>
  );
};

// Hook to use auth context
export const useAuthContext = () => {
  const context = React.useContext(AuthContext);
  if (!context) {
    throw new Error('useAuthContext must be used within an AuthProvider');
  }
  return context;
};

// App Component with Router
const AppWithRouter: React.FC = () => {
  // Force redirect to dashboard in single-user mode
  return (
    <div className="min-h-screen bg-gray-50">
      <Routes>
        {/* All routes redirect to dashboard in single-user mode */}
        <Route path="/login" element={<Navigate to="/dashboard" replace />} />
        <Route path="/register" element={<Navigate to="/dashboard" replace />} />
        <Route path="/setup" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </div>
  );
};

// Main App Component with Auth Provider
const App: React.FC = () => {
  return (
    <Router>
      <AuthProvider>
        <AppWithRouter />
      </AuthProvider>
    </Router>
  );
};

export default App;
