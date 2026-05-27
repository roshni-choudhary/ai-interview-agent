import React from 'react';
import { useAuth } from '../../context/AuthContext';
import Header from './Header';
import LoadingSpinner from '../common/LoadingSpinner';

const Layout = ({ children }) => {
  const { loading } = useAuth();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-dark-950">
        <LoadingSpinner size="lg" text="Authenticating developer..." />
      </div>
    );
  }

  return (
    <div className="flex flex-col min-h-screen bg-dark-950">
      <Header />
      <main className="flex-1 w-full max-w-7xl mx-auto px-6 py-8">
        {children}
      </main>
    </div>
  );
};

export default Layout;
