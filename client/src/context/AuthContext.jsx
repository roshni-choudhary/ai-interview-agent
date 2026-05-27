import React, { createContext, useContext, useState, useEffect } from 'react';
import { authApi } from '../services/api';
import { useNavigate } from 'react-router-dom';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const loadUser = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      setLoading(false);
      return;
    }
    try {
      const data = await authApi.getMe();
      setUser(data);
    } catch (err) {
      localStorage.removeItem('token');
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUser();
  }, []);

  const login = async (username, password) => {
    setLoading(true);
    try {
      await authApi.login(username, password);
      await loadUser();
      navigate('/dashboard');
    } catch (err) {
      setLoading(false);
      throw err;
    }
  };

  const register = async (username, email, password) => {
    setLoading(true);
    try {
      await authApi.register(username, email, password);
      await authApi.login(username, password);
      await loadUser();
      navigate('/dashboard');
    } catch (err) {
      setLoading(false);
      throw err;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
    navigate('/login');
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, reloadUser: loadUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
