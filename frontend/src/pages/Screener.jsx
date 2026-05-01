import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Filter, Search } from 'lucide-react';
import { Card, Spinner } from '../components/common/UIComponents';
import api from '../utils/api';

const Screener = () => {
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchParams, setSearchParams] = useState({ search: '', min_health: '' });
  const navigate = useNavigate();

  const fetchResults = async () => {
    setLoading(true);
    try {
      let query = `/screener/?`;
      if (searchParams.search) query += `search=${searchParams.search}&`;
      if (searchParams.min_health) query += `min_health=${searchParams.min_health}&`;
      
      const res = await api.get(query);
      setCompanies(res.results || res.data || []);
    } catch (err) {
      console.error("Failed to fetch screener results", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchResults();
  }, []); // Initial load

  const handleSearch = (e) => {
    e.preventDefault();
    fetchResults();
  };

  return (
    <div className="space-y-6 flex flex-col h-full">
      <h1 className="text-2xl font-bold tracking-tight">Stock Screener</h1>
      
      <Card>
        <form onSubmit={handleSearch} className="flex flex-wrap gap-4 items-end">
          <div className="flex-1 min-w-[200px]">
            <label className="block text-xs text-fin-muted mb-1">Company or Symbol</label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-fin-muted" size={18} />
              <input 
                type="text" 
                className="fin-input w-full pl-10" 
                placeholder="Search HDFC, Reliance..."
                value={searchParams.search}
                onChange={e => setSearchParams({...searchParams, search: e.target.value})}
              />
            </div>
          </div>
          
          <div className="w-48">
            <label className="block text-xs text-fin-muted mb-1">Min Health Score</label>
            <select 
              className="fin-input w-full"
              value={searchParams.min_health}
              onChange={e => setSearchParams({...searchParams, min_health: e.target.value})}
            >
              <option value="">Any</option>
              <option value="80">Excellent (80+)</option>
              <option value="60">Good (60+)</option>
              <option value="40">Average (40+)</option>
            </select>
          </div>
          
          <button type="submit" className="fin-button-primary">
            <Filter size={18} /> Apply Filters
          </button>
        </form>
      </Card>

      <Card className="flex-1 flex flex-col overflow-hidden p-0" title="Results" action={<span className="text-sm text-fin-muted mr-4">{companies.length} matches</span>}>
        {loading ? (
          <Spinner size="lg" />
        ) : (
          <div className="overflow-y-auto flex-1">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-fin-muted uppercase bg-fin-dark/80 sticky top-0 border-b border-fin-border">
                <tr>
                  <th className="px-6 py-4">Symbol</th>
                  <th className="px-6 py-4">Company</th>
                  <th className="px-6 py-4">Sector</th>
                  <th className="px-6 py-4 text-right">Health Score</th>
                  <th className="px-6 py-4 text-center">Action</th>
                </tr>
              </thead>
              <tbody>
                {companies.length > 0 ? companies.map(company => (
                  <tr key={company.company_id} className="border-b border-fin-border hover:bg-fin-border/20 transition-colors">
                    <td className="px-6 py-4 font-semibold text-fin-blue">{company.symbol}</td>
                    <td className="px-6 py-4">{company.company_name}</td>
                    <td className="px-6 py-4 text-fin-muted">{company.sector_name}</td>
                    <td className="px-6 py-4 text-right">
                      <span className="font-mono text-lg font-bold">{company.health_score || 'N/A'}</span>
                    </td>
                    <td className="px-6 py-4 text-center">
                      <button 
                        onClick={() => navigate(`/company/${company.company_id}`)}
                        className="fin-button-outline text-xs py-1"
                      >
                        Deep Dive
                      </button>
                    </td>
                  </tr>
                )) : (
                  <tr>
                    <td colSpan="5" className="px-6 py-12 text-center text-fin-muted">No companies match your filters.</td>
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

export default Screener;
