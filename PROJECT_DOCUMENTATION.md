# Nifty100 Financial Intelligence Platform - Project Documentation

## Overview

The Nifty100 Financial Intelligence Platform is a comprehensive system for analyzing, screening, and predicting financial metrics for companies in the NIFTY 100 index. The platform combines real-time data collection, advanced analytics, machine learning models, and interactive dashboards.

## Architecture

### Backend (Django REST API)
- REST API for data access and operations
- PostgreSQL database for persistent storage
- Redis for caching and task queues
- Celery for asynchronous task processing

### Frontend (React + Vite)
- Modern SPA built with React 18
- Real-time charts and visualizations with Plotly
- Responsive design with Tailwind CSS
- State management with Context API

### ETL Pipeline
- Automated data extraction from multiple sources
- Data cleaning and validation
- Transformation and enrichment
- Loading into PostgreSQL

### ML Engine
- Financial health scoring
- Anomaly detection in metrics
- Company clustering and categorization
- Time series forecasting

## Key Features

### 1. Company Management
- Complete financial data for NIFTY 100 companies
- Historical metrics tracking
- Sector categorization
- Company comparison tools

### 2. Screener
- Advanced filtering based on financial metrics
- Custom criteria creation
- Saved filter templates
- Export capabilities

### 3. Analytics
- Multi-dimensional financial analysis
- Ratio analysis and trend analysis
- Peer comparison
- Sector insights

### 4. Machine Learning Engine
- **Health Scoring**: Financial health assessment
- **Anomaly Detection**: Identifying unusual patterns
- **Clustering**: Similar company grouping
- **Forecasting**: Revenue/profit predictions

### 5. Partner API
- Authenticated API access
- Rate limiting and throttling
- Webhook support
- Comprehensive documentation

### 6. Dashboards
- Power BI integration
- Custom metrics visualization
- Real-time updates
- Export to multiple formats

## API Endpoints

### Companies
- `GET /api/companies/` - List all companies
- `GET /api/companies/{id}/` - Get company details
- `GET /api/companies/{id}/financials/` - Get financial data
- `GET /api/companies/{id}/analysis/` - Get analysis

### Analytics
- `GET /api/analytics/sectors/` - Sector analysis
- `GET /api/analytics/trends/` - Trend analysis
- `GET /api/analytics/ratios/{company_id}/` - Financial ratios

### Screener
- `POST /api/screener/` - Create screen
- `GET /api/screener/{id}/results/` - Get results

### ML Engine
- `GET /api/ml/scores/{company_id}/` - Health scores
- `GET /api/ml/anomalies/` - Anomalies detected
- `GET /api/ml/clusters/` - Company clusters
- `POST /api/ml/forecast/` - Forecast request

### Partner API
- `GET /api/partner/companies/` - Partner API access
- `POST /api/partner/webhooks/` - Register webhook

## Database Schema

### Core Tables
- **Companies**: Company metadata
- **FinancialData**: Quarterly/Annual financial metrics
- **AnalysisMetrics**: Computed analysis data
- **MLScores**: ML model outputs

### Supporting Tables
- **Sectors**: Industry classification
- **Users**: Platform users
- **APIKeys**: Partner API keys
- **AuditLog**: Change tracking

## Installation and Setup

See README.md for quick start guide.

### Development Setup
```bash
# Clone and navigate
git clone <url>
cd nifty100-financial-intelligence

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Database setup
cd backend
python manage.py migrate

# Load initial data (optional)
python manage.py loaddata companies

# Run development server
python manage.py runserver

# In another terminal, start frontend
cd frontend
npm install
npm run dev
```

## Deployment

See `deployment/` folder for:
- Docker configuration
- Kubernetes manifests
- Nginx configuration
- Gunicorn settings

### Docker Deployment
```bash
docker-compose up -d
```

## Testing

### Backend Tests
```bash
cd backend
pytest
pytest --cov=apps
```

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage
```

### Integration Tests
```bash
pytest tests/integration/
```

## Data Pipeline

### ETL Process
1. **Extract**: Fetch data from external sources
2. **Transform**: Clean, validate, and enrich data
3. **Load**: Store in PostgreSQL
4. **Schedule**: Automated daily/weekly runs via Celery

### Data Sources
- NSE/BSE official APIs
- Financial data providers
- News sources for sentiment
- Company websites

## Performance Optimization

- Database indexing on frequently queried fields
- Redis caching for API responses
- Pagination for large datasets
- Async processing with Celery
- CDN for static assets
- Database query optimization

## Security

- JWT authentication for API
- API key rotation for partners
- Rate limiting and throttling
- Input validation and sanitization
- CORS configuration
- SQL injection prevention
- CSRF protection

## Monitoring and Logging

- Application logging with Python logging
- Error tracking and reporting
- Performance monitoring
- Database query logging
- API request/response logging
- Celery task monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and add tests
4. Submit pull request

## Support

For issues and questions:
- GitHub Issues: Report bugs
- Email: support@bluestock.com
- Documentation: See docs/ folder

## License

MIT License - See LICENSE file for details
