-- PostgreSQL Star Schema Setup for NIFTY 100 Financial Intelligence

-- ==========================================
-- DIMENSION TABLES
-- ==========================================

CREATE TABLE IF NOT EXISTS dim_sector (
    sector_id SERIAL PRIMARY KEY,
    sector_name VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dim_company (
    company_id SERIAL PRIMARY KEY,
    symbol VARCHAR(50) UNIQUE NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    sector_id INTEGER REFERENCES dim_sector(sector_id),
    industry VARCHAR(100),
    market_cap_cr NUMERIC(15, 2),
    current_price NUMERIC(15, 2),
    pe_ratio NUMERIC(10, 2),
    dividend_yield NUMERIC(10, 2),
    roce NUMERIC(10, 2),
    roe NUMERIC(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dim_year (
    year_id SERIAL PRIMARY KEY,
    year_value INTEGER UNIQUE NOT NULL,
    financial_year VARCHAR(20) -- e.g. "FY2023"
);

CREATE TABLE IF NOT EXISTS dim_health_label (
    label_id SERIAL PRIMARY KEY,
    label_name VARCHAR(50) UNIQUE NOT NULL, -- 'EXCELLENT', 'GOOD', 'AVERAGE', 'WEAK', 'POOR'
    description TEXT
);

-- Pre-populate dim_health_label
INSERT INTO dim_health_label (label_name, description) VALUES
('EXCELLENT', 'Outstanding financial health, high profitability, low debt.'),
('GOOD', 'Strong financials, minor areas for improvement.'),
('AVERAGE', 'Stable financials but lacks significant growth.'),
('WEAK', 'Vulnerable financial position, high leverage or low margins.'),
('POOR', 'Critical financial distress, high risk.')
ON CONFLICT (label_name) DO NOTHING;

-- ==========================================
-- FACT TABLES
-- ==========================================

CREATE TABLE IF NOT EXISTS fact_profit_loss (
    pl_id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES dim_company(company_id) ON DELETE CASCADE,
    year_id INTEGER REFERENCES dim_year(year_id) ON DELETE CASCADE,
    revenue NUMERIC(15, 2),
    expenses NUMERIC(15, 2),
    operating_profit NUMERIC(15, 2),
    opm_percentage NUMERIC(10, 2), -- Operating Profit Margin
    other_income NUMERIC(15, 2),
    interest NUMERIC(15, 2),
    depreciation NUMERIC(15, 2),
    profit_before_tax NUMERIC(15, 2),
    tax_percentage NUMERIC(10, 2),
    net_profit NUMERIC(15, 2),
    eps NUMERIC(15, 2), -- Earnings Per Share
    dividend_payout NUMERIC(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(company_id, year_id)
);

CREATE TABLE IF NOT EXISTS fact_balance_sheet (
    bs_id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES dim_company(company_id) ON DELETE CASCADE,
    year_id INTEGER REFERENCES dim_year(year_id) ON DELETE CASCADE,
    equity_capital NUMERIC(15, 2),
    reserves NUMERIC(15, 2),
    borrowings NUMERIC(15, 2),
    other_liabilities NUMERIC(15, 2),
    total_liabilities NUMERIC(15, 2),
    fixed_assets NUMERIC(15, 2),
    cwip NUMERIC(15, 2), -- Capital Work in Progress
    investments NUMERIC(15, 2),
    other_assets NUMERIC(15, 2),
    total_assets NUMERIC(15, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(company_id, year_id)
);

CREATE TABLE IF NOT EXISTS fact_cash_flow (
    cf_id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES dim_company(company_id) ON DELETE CASCADE,
    year_id INTEGER REFERENCES dim_year(year_id) ON DELETE CASCADE,
    operating_cash_flow NUMERIC(15, 2),
    investing_cash_flow NUMERIC(15, 2),
    financing_cash_flow NUMERIC(15, 2),
    net_cash_flow NUMERIC(15, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(company_id, year_id)
);

CREATE TABLE IF NOT EXISTS fact_analysis (
    analysis_id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES dim_company(company_id) ON DELETE CASCADE,
    year_id INTEGER REFERENCES dim_year(year_id) ON DELETE CASCADE,
    roe_percentage NUMERIC(10, 2),
    roce_percentage NUMERIC(10, 2),
    debt_to_equity NUMERIC(10, 2),
    sales_growth_percentage NUMERIC(10, 2),
    profit_growth_percentage NUMERIC(10, 2),
    cagr_3yr NUMERIC(10, 2),
    cagr_5yr NUMERIC(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(company_id, year_id)
);

CREATE TABLE IF NOT EXISTS fact_ml_scores (
    score_id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES dim_company(company_id) ON DELETE CASCADE,
    health_score NUMERIC(5, 2), -- 0 to 100
    label_id INTEGER REFERENCES dim_health_label(label_id),
    anomaly_flag BOOLEAN DEFAULT FALSE,
    anomaly_score NUMERIC(10, 4),
    forecasted_revenue_1yr NUMERIC(15, 2),
    forecasted_revenue_3yr NUMERIC(15, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(company_id)
);

CREATE TABLE IF NOT EXISTS fact_pros_cons (
    pc_id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES dim_company(company_id) ON DELETE CASCADE,
    pro_con_type VARCHAR(10), -- 'PRO' or 'CON'
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- INDEXES FOR POWER BI & API OPTIMIZATION
-- ==========================================
CREATE INDEX idx_company_sector ON dim_company(sector_id);
CREATE INDEX idx_pl_company ON fact_profit_loss(company_id);
CREATE INDEX idx_pl_year ON fact_profit_loss(year_id);
CREATE INDEX idx_bs_company ON fact_balance_sheet(company_id);
CREATE INDEX idx_cf_company ON fact_cash_flow(company_id);
CREATE INDEX idx_analysis_company ON fact_analysis(company_id);
CREATE INDEX idx_ml_company ON fact_ml_scores(company_id);
