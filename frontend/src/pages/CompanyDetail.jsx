import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, AlertCircle } from 'lucide-react';
import { Card, Spinner } from '../components/common/UIComponents';
import { BarChart, RadarChart } from '../components/charts/BaseCharts';
import api from '../utils/api';

const CompanyDetail = () => {
  const { id } = useParams();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [company, setCompany] = useState(null);

  useEffect(() => {
    const fetchCompany = async () => {
      try {
        setLoading(true);
        const res = await api.get(`/companies/${id}/`);
        setCompany(res.data || res);
      } catch (err) {
        setError("Failed to load company details. Please try again.");
      } finally {
        setLoading(false);
      }
    };
    if (id) fetchCompany();
  }, [id]);

  if (loading) return <Spinner size="lg" />;
  if (error) return <div className="text-fin-red flex items-center gap-2 p-6"><AlertCircle /> {error}</div>;
  if (!company) return <div>No data found.</div>;

  // Prepare Chart Data
  const plData = company.profit_loss || [];
  
  const revenueProfitChart = {
    labels: plData.map(d => d.year_value).reverse(),
    datasets: [
      {
        label: 'Revenue',
        data: plData.map(d => Number(d.revenue)).reverse(),
        backgroundColor: '#3b82f6',
      },
      {
        label: 'Net Profit',
        data: plData.map(d => Number(d.net_profit)).reverse(),
        backgroundColor: '#10b981',
      }
    ]
  };

  const radarData = {
    labels: ['Profitability', 'Growth', 'Leverage', 'Returns', 'Valuation'],
    datasets: [{
      label: 'Financial Health Profile',
      data: [85, 60, 90, 75, 40], // Mocked dimensions based on overall score
      backgroundColor: 'rgba(59, 130, 246, 0.2)',
      borderColor: '#3b82f6',
      borderWidth: 2,
    }]
  };

  const ml = company.ml_score || {};

  return (
    <div className="space-y-6">
      <Link to="/screener" className="flex items-center gap-2 text-fin-muted hover:text-fin-text text-sm transition-colors w-fit">
        <ArrowLeft size={16} /> Back to Screener
      </Link>
      
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-fin-border pb-6">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-bold">{company.company_name}</h1>
            <span className="bg-fin-border px-3 py-1 rounded-md text-sm font-semibold tracking-wider text-fin-blue">{company.symbol}</span>
          </div>
          <p className="text-fin-muted mt-1">{company.sector?.sector_name} • {company.industry}</p>
        </div>
        
        <div className="text-right">
          <div className="text-3xl font-bold">₹{company.current_price}</div>
          <div className="text-sm text-fin-muted">M.Cap: {company.market_cap_cr} Cr</div>
        </div>
      </div>

      {/* ML Intelligence Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="bg-gradient-to-br from-fin-card to-[#1e293b]">
          <h3 className="text-fin-muted text-sm font-medium mb-1">AI Health Score</h3>
          <div className="flex items-end gap-3 mt-2">
            <span className="text-5xl font-black">{ml.health_score || 'N/A'}</span>
            <span className="text-xl text-fin-muted mb-1">/ 100</span>
          </div>
          <div className={`mt-4 inline-block px-3 py-1 rounded text-xs font-bold ${
              ml.label?.label_name === 'EXCELLENT' ? 'bg-fin-green/20 text-fin-green' : 
              ml.label?.label_name === 'POOR' ? 'bg-fin-red/20 text-fin-red' : 'bg-fin-blue/20 text-fin-blue'
            }`}>
            {ml.label?.label_name || 'UNRATED'}
          </div>
        </Card>

        <Card>
          <h3 className="text-fin-muted text-sm font-medium mb-4">ML Forecast (Revenue)</h3>
          <div className="space-y-4">
            <div>
              <p className="text-xs text-fin-muted">1-Year Forecast</p>
              <p className="text-xl font-semibold text-fin-blue">{ml.forecasted_revenue_1yr} Cr</p>
            </div>
            <div>
              <p className="text-xs text-fin-muted">3-Year Forecast</p>
              <p className="text-xl font-semibold text-fin-blue">{ml.forecasted_revenue_3yr} Cr</p>
            </div>
          </div>
        </Card>

        <Card>
           <h3 className="text-fin-muted text-sm font-medium mb-2">Anomaly Detection</h3>
           {ml.anomaly_flag ? (
             <div className="bg-fin-red/10 border border-fin-red/20 p-4 rounded-lg flex items-start gap-3 mt-4">
               <AlertCircle className="text-fin-red shrink-0" />
               <div>
                 <p className="text-fin-red font-semibold text-sm">Suspicious Pattern Detected</p>
                 <p className="text-xs text-fin-red/70 mt-1">Anomaly score: {ml.anomaly_score}</p>
               </div>
             </div>
           ) : (
             <div className="bg-fin-green/10 border border-fin-green/20 p-4 rounded-lg flex items-center justify-center h-24 mt-4">
               <p className="text-fin-green font-medium">No anomalies detected</p>
             </div>
           )}
        </Card>
      </div>

      {/* Visualizations */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card title="Revenue vs Net Profit" className="lg:col-span-2 h-[400px] flex flex-col">
          <div className="flex-1 relative">
            <BarChart data={revenueProfitChart} />
          </div>
        </Card>
        
        <Card title="Financial Profile" className="h-[400px] flex flex-col">
          <div className="flex-1 relative">
             <RadarChart data={radarData} />
          </div>
        </Card>
      </div>
    </div>
  );
};

export default CompanyDetail;
