import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from 'antd';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import UserManagement from './pages/UserManagement';
import EmotionAnalysis from './pages/EmotionAnalysis';
import PrivateRoute from './components/PrivateRoute';
import Sidebar from './components/Sidebar';

const { Content } = Layout;

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/"
          element={
            <PrivateRoute>
              <Layout style={{ minHeight: '100vh' }}>
                <Sidebar />
                <Layout>
                  <Content style={{ margin: '24px 16px', padding: 24, background: '#fff' }}>
                    <Routes>
                      <Route path="/" element={<Navigate to="/dashboard" replace />} />
                      <Route path="/dashboard" element={<Dashboard />} />
                      <Route path="/users" element={<UserManagement />} />
                      <Route path="/emotion" element={<EmotionAnalysis />} />
                    </Routes>
                  </Content>
                </Layout>
              </Layout>
            </PrivateRoute>
          }
        />
      </Routes>
    </Router>
  );
};

export default App; 