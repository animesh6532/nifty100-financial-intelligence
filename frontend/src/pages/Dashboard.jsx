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
  const [data, setData] = useState({ 
    companies: [], 
    stats: { mcap: null, avgPE: null, health: null, anomalies: null },
    revenueChartData: null,
    trendChartData: null,
    error: null
  });

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        // We will now call the real dashboard endpoint. 
        // We expect it to return stats, chart data, and top companies.
        const res = await api.get('/dashboards/overview/');
        const dashboardData = res.data;
        
        setData({
          companies: dashboardData.top_companies || [],
          stats: dashboardData.stats || { mcap: null, avgPE: null, health: null, anomalies: null },
          revenueChartData: dashboardData.revenue_chart || null,
          trendChartData: dashboardData.trend_chart || null,
          error: null
        });
      } catch (err) {
        console.error("Dashboard data fetch failed", err);
        setData(prev => ({ ...prev, error: "Failed to load dashboard data." }));
      } finally {
        setLoading(false);
      }
    };
    
    fetchDashboardData();
  }, []);

  if (data.error) {
    return (
      <div className="flex items-center justify-center h-full p-8 text-fin-red">
        <AlertTriangle className="mr-2" />
        {data.error}
      </div>
    );
  }

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
          value={data.stats.mcap !== null ? data.stats.mcap : '-'} icon={<DollarSign size={20} />}
          subtitle="NIFTY 100" 
        />
        <StatCard 
          isLoading={loading} title="Average P/E Ratio" 
          value={data.stats.avgPE !== null ? data.stats.avgPE : '-'} icon={<Activity size={20} />}
          subtitle="Sector adjusted" 
        />
        <StatCard 
          isLoading={loading} title="Excellent Health" 
          value={data.stats.health !== null ? data.stats.health : '-'} icon={<TrendingUp size={20} />}
          subtitle="Companies upgraded" 
        />
        <StatCard 
          isLoading={loading} title="Anomalies Detected" 
          value={data.stats.anomalies !== null ? data.stats.anomalies : '-'} icon={<AlertTriangle size={20} />}
          subtitle="Requires attention" 
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card title="Quarterly Revenue Aggregation" className="h-[350px] flex flex-col">
          <div className="flex-1 relative flex items-center justify-center">
            {loading ? <Skeleton className="h-full w-full" /> : 
              data.revenueChartData ? <BarChart data={data.revenueChartData} /> : 
              <span className="text-fin-muted">No chart data available</span>}
          </div>
        </Card>
        <Card title="Margin Trends (NIFTY 100 Avg)" className="h-[350px] flex flex-col">
          <div className="flex-1 relative flex items-center justify-center">
            {loading ? <Skeleton className="h-full w-full" /> : 
              data.trendChartData ? <LineChart data={data.trendChartData} /> : 
              <span className="text-fin-muted">No chart data available</span>}
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
                {data.companies.length > 0 ? data.companies.map(company => (
                  <tr key={company.id || company.company_id} className="border-b border-fin-border hover:bg-fin-border/20">
                    <td className="px-4 py-3 font-semibold text-fin-blue">{company.symbol}</td>
                    <td className="px-4 py-3">{company.name || company.company_name}</td>
                    <td className="px-4 py-3 text-fin-muted">{company.sector || company.sector_name || '-'}</td>
                    <td className="px-4 py-3 text-right">{company.market_cap || company.market_cap_cr || '-'}</td>
                    <td className="px-4 py-3 text-center">
                      <span className={`px-2 py-1 rounded text-xs font-bold ${
                        company.health_label === 'EXCELLENT' ? 'bg-fin-green/20 text-fin-green' : 
                        company.health_label === 'POOR' ? 'bg-fin-red/20 text-fin-red' : 'bg-fin-blue/20 text-fin-blue'
                      }`}>
                        {company.health_label || 'UNKNOWN'}
                      </span>
                    </td>
                  </tr>
                )) : (
                  <tr>
                    <td colSpan="5" className="px-4 py-8 text-center text-fin-muted">
                      No companies found
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </div>
  );
};

export default Dashboard;
