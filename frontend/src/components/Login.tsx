import React, { useState } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { useAuthContext } from '../App';
import Button from './common/Button';
import Input from './common/Input';

const Login: React.FC = () => {
  const { login } = useAuthContext();
  
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  // Always redirect to dashboard in single-user mode
  return <Navigate to="/dashboard" replace />;

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!email || !password) {
      setError('Please enter both email and password');
      return;
    }
    
    try {
      setLoading(true);
      setError(null);
      
      const success = await login(email, password);
      
      if (!success) {
        setError('Invalid email or password');
      }
      
      setLoading(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Invalid email or password');
      setLoading(false);
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen">
      <div className="bg-white shadow-md rounded-lg p-8 max-w-md w-full">
        <h1 className="text-2xl font-bold mb-6 text-center">Login to QT.AI</h1>
        
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4 text-sm">
            {error}
          </div>
        )}
        
        <form onSubmit={handleLogin}>
          <Input
            id="email"
            label="Email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          
          <Input
            id="password"
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          
          <Button
            type="submit"
            disabled={loading}
            className="w-full mt-4"
          >
            {loading ? 'Logging in...' : 'Sign In'}
          </Button>
        </form>
        
        <div className="mt-4 text-center">
          <p>
            Don't have an account?{' '}
            <Link to="/register" className="text-blue-600 hover:text-blue-800">
              Register
            </Link>
          </p>
        </div>
        
        <div className="mt-8 pt-6 border-t border-gray-200 text-center">
          <p className="text-xs text-gray-500">
            For demo purposes, you can also{' '}
            <Link to="/setup" className="text-blue-600 hover:text-blue-800">
              go directly to the setup wizard
            </Link>
            {' '}or{' '}
            <Link to="/dashboard" className="text-blue-600 hover:text-blue-800">
              view the dashboard
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
