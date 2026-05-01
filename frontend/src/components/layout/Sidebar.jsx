import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, BarChart2, Search, LineChart, Server, Settings } from 'lucide-react';

const Sidebar = () => {
  const navItems = [
    { name: 'Dashboard', path: '/', icon: <LayoutDashboard size={20} /> },
    { name: 'Screener', path: '/screener', icon: <Search size={20} /> },
    { name: 'Sector Analytics', path: '/sectors', icon: <BarChart2 size={20} /> },
    { name: 'Forecasts', path: '/forecasts', icon: <LineChart size={20} /> },
    { name: 'API Docs', path: '/api-docs', icon: <Server size={20} /> },
    { name: 'Settings', path: '/settings', icon: <Settings size={20} /> },
  ];

  return (
    <div className="w-64 bg-fin-card border-r border-fin-border flex flex-col">
      <div className="h-16 flex items-center px-6 border-b border-fin-border">
        <div className="flex items-center gap-2 text-fin-blue font-bold text-xl tracking-tighter">
          <div className="w-6 h-6 rounded bg-fin-blue text-white flex items-center justify-center text-xs">N</div>
          <span>FINTELL</span>
        </div>
      </div>
      
      <nav className="flex-1 py-6 px-3 flex flex-col gap-2">
        {navItems.map((item) => (
          <NavLink
            key={item.name}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors ${
                isActive 
                  ? 'bg-fin-blue/10 text-fin-blue font-medium' 
                  : 'text-fin-muted hover:text-fin-text hover:bg-fin-border/50'
              }`
            }
          >
            {item.icon}
            <span>{item.name}</span>
          </NavLink>
        ))}
      </nav>
      
      <div className="p-4 border-t border-fin-border">
        <div className="bg-fin-dark rounded-lg p-4 border border-fin-border/50">
          <p className="text-xs text-fin-muted mb-2">API Usage</p>
          <div className="w-full bg-fin-border h-1.5 rounded-full overflow-hidden">
            <div className="bg-fin-green w-[45%] h-full"></div>
          </div>
          <p className="text-[10px] text-right mt-1 text-fin-muted">450 / 1000 Req</p>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
