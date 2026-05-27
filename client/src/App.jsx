import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { InterviewProvider } from './context/InterviewContext';
import Layout from './components/layout/Layout';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import InterviewSetupPage from './pages/InterviewSetupPage';
import InterviewPage from './pages/InterviewPage';
import ResultsPage from './pages/ResultsPage';

// Route blocker for unauthorized sessions
const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) return null; // loading screen handled in Layout
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

const AppContent = () => {
  return (
    <Routes>
      {/* Public Pages */}
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<LoginPage />} />

      {/* Protected Dashboards */}
      <Route 
        path="/dashboard" 
        element={
          <ProtectedRoute>
            <Layout>
              <DashboardPage />
            </Layout>
          </ProtectedRoute>
        } 
      />
      
      <Route 
        path="/interview/setup" 
        element={
          <ProtectedRoute>
            <Layout>
              <InterviewSetupPage />
            </Layout>
          </ProtectedRoute>
        } 
      />

      <Route 
        path="/interview/:sessionId" 
        element={
          <ProtectedRoute>
            <InterviewPage />
          </ProtectedRoute>
        } 
      />

      <Route 
        path="/results/:sessionId" 
        element={
          <ProtectedRoute>
            <Layout>
              <ResultsPage />
            </Layout>
          </ProtectedRoute>
        } 
      />

      {/* Wildcard Fallback */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

const App = () => {
  return (
    <AuthProvider>
      <InterviewProvider>
        <AppContent />
      </InterviewProvider>
    </AuthProvider>
  );
};

export default App;
