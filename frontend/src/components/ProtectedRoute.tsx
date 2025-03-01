import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

interface ProtectedRouteProps {
  children: React.ReactNode;
  requireSetup?: boolean;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ 
  children, 
  requireSetup = true 
}) => {
  // Auto-authenticated, so we can just render the children directly
  // No need for authentication checks since we're bypassing login
  return <>{children}</>;
};

export default ProtectedRoute;
