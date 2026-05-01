import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Dashboard from './pages/Dashboard';
import Screener from './pages/Screener';
import CompanyDetail from './pages/CompanyDetail';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="screener" element={<Screener />} />
          <Route path="company/:id" element={<CompanyDetail />} />
          
          {/* Placeholders for future routes */}
          <Route path="sectors" element={<div className="p-6">Sector Analytics (Coming Soon)</div>} />
          <Route path="forecasts" element={<div className="p-6">Forecast Dashboard (Coming Soon)</div>} />
          <Route path="api-docs" element={<div className="p-6">API Documentation (Coming Soon)</div>} />
          <Route path="settings" element={<div className="p-6">Settings (Coming Soon)</div>} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
