import React from 'react';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ 
  children 
  // requireSetup parameter removed as it's unused
}) => {
  // Auto-authenticated, so we can just render the children directly
  // No need for authentication checks since we're bypassing login
  return <>{children}</>;
};

export default ProtectedRoute;
