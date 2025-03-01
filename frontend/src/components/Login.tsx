import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuthContext } from '../App';

const Login: React.FC = () => {
  // We only need the auth context for type checking, but don't use any of its properties
  useAuthContext();
  
  // Always redirect to dashboard in single-user mode
  return <Navigate to="/dashboard" replace />;
};

export default Login;
