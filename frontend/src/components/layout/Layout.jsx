import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';

const Layout = () => {
  return (
    <div className="flex h-screen overflow-hidden bg-fin-dark">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Navbar / Header could go here */}
        <header className="h-16 border-b border-fin-border flex items-center justify-between px-6 bg-fin-card">
          <h2 className="text-xl font-semibold tracking-tight">NIFTY 100 Analytics</h2>
          <div className="flex items-center gap-4">
            {/* User profile, notifications, etc. */}
            <div className="w-8 h-8 rounded-full bg-fin-blue flex items-center justify-center font-bold text-sm">
              AI
            </div>
          </div>
        </header>
        
        {/* Main Content Area */}
        <main className="flex-1 overflow-y-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Layout;
