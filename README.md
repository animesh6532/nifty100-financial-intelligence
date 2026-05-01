# Nifty100 Financial Intelligence Platform

A comprehensive financial intelligence platform for analyzing and screening NIFTY 100 companies with advanced analytics, machine learning insights, and real-time data processing.

## Features

- **Company Analysis**: Comprehensive financial metrics and historical data for NIFTY 100 companies
- **Screener**: Advanced filtering and comparison tools based on financial health
- **Analytics Engine**: Multi-dimensional financial analysis and insights
- **ML Engine**: Anomaly detection, clustering, and forecasting capabilities
- **Partner API**: RESTful API for third-party integrations
- **Dashboards**: Interactive visualizations and reporting
- **ETL Pipeline**: Automated data extraction, transformation, and loading

## Project Structure

```
├── backend/          # Django REST API
├── frontend/         # React/Vite SPA
├── etl/             # Data pipeline
├── notebooks/       # Jupyter analysis notebooks
├── dashboards/      # Power BI reports
├── data/            # Data storage (raw, cleaned, exports)
├── docs/            # Documentation and diagrams
├── deployment/      # Docker, Kubernetes, Nginx configs
├── tests/           # Test suites
└── scripts/         # Utility scripts
```

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- Docker & Docker Compose (optional)

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd nifty100-financial-intelligence
```

2. Setup Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r ../requirements.txt
python manage.py migrate
python manage.py runserver
```

3. Setup Frontend
```bash
cd frontend
npm install
npm run dev
```

### Using Docker
```bash
docker-compose up -d
```

## Documentation

See [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md) for detailed documentation.

## License

See LICENSE file for details.
