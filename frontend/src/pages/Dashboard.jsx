import React, { useState, useEffect } from 'react';
import { Activity, TrendingUp, DollarSign, AlertTriangle } from 'lucide-react';
import { Card, Skeleton } from '../components/common/UIComponents';
import { BarChart, LineChart } from '../components/charts/BaseCharts';
import api from '../utils/api';

const StatCard = ({ title, value, icon, subtitle, trend, isLoading }) => {
  if (isLoading) return <Skeleton className="h-32 w-full" />;
  
  return (
    <Card className="flex flex-col">
      <div className="flex justify-between items-start mb-2">
        <p className="text-fin-muted text-sm font-medium">{title}</p>
        <div className="text-fin-blue bg-fin-blue/10 p-2 rounded-lg">{icon}</div>
      </div>
      <h3 className="text-2xl font-bold text-fin-text">{value}</h3>
      <div className="flex items-center gap-2 mt-2">
        {trend && (
          <span className={`text-xs font-semibold ${trend > 0 ? 'text-fin-green' : 'text-fin-red'}`}>
            {trend > 0 ? '+' : ''}{trend}%
          </span>
        )}
        <span className="text-xs text-fin-muted">{subtitle}</span>
      </div>
    </Card>
  );
};

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState({ companies: [], stats: null });

  useEffect(() => {
    // In a real scenario, we might hit a specific /dashboard/ endpoint
    // For now, we simulate fetching aggregated data from companies list
    const fetchDashboardData = async () => {
      try {
        const res = await api.get('/companies/?limit=100');
        const companies = res.results || res.data || [];
        
        // Aggregate stats manually for demo
        const totalMcap = companies.reduce((acc, curr) => acc + Number(curr.market_cap_cr || 0), 0);
        const avgPE = companies.reduce((acc, curr) => acc + Number(curr.pe_ratio || 0), 0) / (companies.length || 1);
        const excellentHealth = companies.filter(c => c.health_label === 'EXCELLENT').length;
        
        setData({
          companies,
          stats: {
            mcap: (totalMcap / 100000).toFixed(2) + 'L Cr',
            avgPE: avgPE.toFixed(1),
            health: `${excellentHealth} Cos.`,
          }
        });
      } catch (err) {
        console.error("Dashboard data fetch failed", err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchDashboardData();
  }, []);

  const revenueChartData = {
    labels: ['Q1', 'Q2', 'Q3', 'Q4'],
    datasets: [
      {
        label: 'Aggregated Revenue (Cr)',
        data: [12000, 19000, 15000, 22000],
        backgroundColor: '#3b82f6',
        borderRadius: 4,
      }
    ]
  };

  const trendChartData = {
    labels: ['2019', '2020', '2021', '2022', '2023'],
    datasets: [
      {
        label: 'Avg Operating Margin %',
        data: [15, 12, 18, 22, 21],
        borderColor: '#10b981',
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        fill: true,
        tension: 0.4
      }
    ]
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold tracking-tight">Executive Overview</h1>
        <div className="text-sm text-fin-muted">NIFTY 100 Universe</div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard 
          isLoading={loading} title="Total Market Cap" 
          value={data.stats?.mcap || '0'} icon={<DollarSign size={20} />}
          subtitle="vs last quarter" trend={4.2}
        />
        <StatCard 
          isLoading={loading} title="Average P/E Ratio" 
          value={data.stats?.avgPE || '0'} icon={<Activity size={20} />}
          subtitle="Sector adjusted" trend={-1.5}
        />
        <StatCard 
          isLoading={loading} title="Excellent Health" 
          value={data.stats?.health || '0'} icon={<TrendingUp size={20} />}
          subtitle="Companies upgraded" trend={12}
        />
        <StatCard 
          isLoading={loading} title="Anomalies Detected" 
          value="3" icon={<AlertTriangle size={20} />}
          subtitle="Requires attention" 
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card title="Quarterly Revenue Aggregation" className="h-[350px] flex flex-col">
          <div className="flex-1 relative">
            <BarChart data={revenueChartData} />
          </div>
        </Card>
        <Card title="Margin Trends (NIFTY 100 Avg)" className="h-[350px] flex flex-col">
          <div className="flex-1 relative">
            <LineChart data={trendChartData} />
          </div>
        </Card>
      </div>
      
      {/* Recent Companies Table */}
      <Card title="Top Movers (Market Cap)">
        {loading ? <Skeleton className="h-64" /> : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-fin-muted uppercase bg-fin-dark/50 border-b border-fin-border">
                <tr>
                  <th className="px-4 py-3">Symbol</th>
                  <th className="px-4 py-3">Company</th>
                  <th className="px-4 py-3">Sector</th>
                  <th className="px-4 py-3 text-right">M.Cap (Cr)</th>
                  <th className="px-4 py-3 text-center">Health</th>
                </tr>
              </thead>
              <tbody>
                {data.companies.slice(0, 5).map(company => (
                  <tr key={company.company_id} className="border-b border-fin-border hover:bg-fin-border/20">
                    <td className="px-4 py-3 font-semibold text-fin-blue">{company.symbol}</td>
                    <td className="px-4 py-3">{company.company_name}</td>
                    <td className="px-4 py-3 text-fin-muted">{company.sector_name}</td>
                    <td className="px-4 py-3 text-right">{company.market_cap_cr}</td>
                    <td className="px-4 py-3 text-center">
                      <span className={`px-2 py-1 rounded text-xs font-bold ${
                        company.health_label === 'EXCELLENT' ? 'bg-fin-green/20 text-fin-green' : 
                        company.health_label === 'POOR' ? 'bg-fin-red/20 text-fin-red' : 'bg-fin-blue/20 text-fin-blue'
                      }`}>
                        {company.health_label || 'UNKNOWN'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </div>
  );
};

export default Dashboard;
