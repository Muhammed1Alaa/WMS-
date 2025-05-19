import { useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/auth';

export const useAuth = () => {
  const navigate = useNavigate();
  const { login, register, logout, isAuthenticated } = useAuthStore();

  const handleLogin = useCallback(
    async (email: string, password: string) => {
      try {
        await login(email, password);
        navigate('/dashboard');
      } catch (error) {
        console.error('Login failed:', error);
        throw error;
      }
    },
    [login, navigate]
  );

  const handleRegister = useCallback(
    async (email: string, password: string, full_name: string) => {
      try {
        await register(email, password, full_name);
        navigate('/dashboard');
      } catch (error) {
        console.error('Registration failed:', error);
        throw error;
      }
    },
    [register, navigate]
  );

  const handleLogout = useCallback(() => {
    logout();
    navigate('/login');
  }, [logout, navigate]);

  return {
    isAuthenticated,
    login: handleLogin,
    register: handleRegister,
    logout: handleLogout,
  };
}; 