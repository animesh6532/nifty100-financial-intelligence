# PROJECT STATUS

## 1. Completed
- **Project Structure**: Skeleton is set up (`backend/`, `frontend/`, `etl/`, `data/`, `dashboards/`, `docs/`, `tests/`).
- **Data Resources**: Raw dataset is available in `data/raw/` as `.xlsx` files (`analysis.xlsx`, `balancesheet.xlsx`, `cashflow.xlsx`, `companies.xlsx`, `documents.xlsx`, `profitandloss.xlsx`, `prosandcons.xlsx`).
- **Django Core Settings**: PostgreSQL, Celery, Redis, and JWT configurations exist in `settings.py`.
- **Basic Companies API**: The `/api/companies/` endpoint has models, views, and URLs partially implemented.
- **Frontend Skeleton**: React + Vite environment works, standard UI components (`Navbar`, `Sidebar`, `Card`, `Skeleton`) and base pages (`Dashboard.jsx`, `Screener.jsx`, `CompanyDetail.jsx`) are defined.
- **ThemeContext Boilerplate**: Basic React Context established for theme toggling.

## 2. Partially Implemented
- **ETL Pipeline (`etl/`)**: Scripts exist (`extract.py`, `transform.py`, `load.py`), but extraction logic currently expects `.sql` or `.csv` rather than processing the existing `.xlsx` files. The load mechanism does not fully leverage robust UPSERTs.
- **Django APIs (`backend/`)**: Several apps (`dashboards`, `ml_engine`, `analytics`) have empty or incomplete views and lack necessary serializers.
- **PostgreSQL Integration**: Database initialization file `db_setup.sql` is present and `powerbi_views.sql` exists, but the automated data flow into these tables is unfinished.
- **Frontend Integration**: Frontend components call `/api/companies/`, but heavily rely on dummy data or mock aggregations for dashboards and charts.

## 3. Missing
- **Full ETL Transformations**: No comprehensive year normalization, NULL cleaning, duplicate removal, or complex metric computation (debt-to-equity, ROA, profit margin) implemented for the Excel data.
- **Star Schema Population**: The script to fully build and populate `dim_company`, `dim_year`, `dim_sector`, `dim_health`, `fact_profit_loss`, `fact_balance`, `fact_cashflow`, `fact_analysis`, and `fact_ml_scores`.
- **Complete APIs**: Missing or incomplete functional endpoints for `/api/sector/`, `/api/health/`, `/api/analytics/`, and `/api/dashboard/`.
- **ML Health Score System**: Logic to compute and assign labels (EXCELLENT, GOOD, AVERAGE, WEAK, POOR) and store them in `fact_ml_scores`.
- **Power BI Implementation**: Actual `.pbix` dashboards using PostgreSQL warehouse data (only SQL views exist).
- **Tests**: Comprehensive tests for ETL, APIs, and the Frontend.
- **Documentation**: Missing detailed architecture, deployment, and ETL docs.

## 4. Broken / Uses Dummy Data
- **Dummy Data**: Frontend charts in `Dashboard.jsx` (e.g., `revenueChartData`, `trendChartData`) use hardcoded placeholders and arrays instead of fetching real data.
- **Dummy Aggregations**: Stats like "Average P/E" and "Total Market Cap" are computed loosely on the client side with mock fallbacks rather than relying on a solid backend dashboard endpoint.
- **Theme Context**: `ThemeContext.jsx` has `isDarkMode` state but fails to persist to `localStorage` or append the dark mode class globally to the HTML document.
- **Incomplete API Responses**: `MLScoreViewSet`, `AnomalyViewSet` and others are missing serializers causing them to break if accessed.
