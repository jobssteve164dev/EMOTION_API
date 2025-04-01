import { useState, useEffect } from 'react';
import axios from 'axios';

interface AuthState {
  isAuthenticated: boolean;
  user: any | null;
  token: string | null;
}

export const useAuth = () => {
  const [authState, setAuthState] = useState<AuthState>({
    isAuthenticated: false,
    user: null,
    token: localStorage.getItem('token'),
  });

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      checkAuth(token);
    }
  }, []);

  const checkAuth = async (token: string) => {
    try {
      const response = await axios.get('http://localhost:8000/api/v1/users/me', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setAuthState({
        isAuthenticated: true,
        user: response.data,
        token
      });
    } catch (error) {
      logout();
    }
  };

  const login = async (username: string, password: string) => {
    try {
      const response = await axios.post('http://localhost:8000/api/v1/token', {
        username,
        password
      });
      const { access_token } = response.data;
      localStorage.setItem('token', access_token);
      await checkAuth(access_token);
      return true;
    } catch (error) {
      return false;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setAuthState({
      isAuthenticated: false,
      user: null,
      token: null
    });
  };

  return {
    ...authState,
    login,
    logout
  };
}; 