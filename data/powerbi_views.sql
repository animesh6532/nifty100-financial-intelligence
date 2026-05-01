-- ==========================================
-- POWER BI REPORTING VIEWS
-- Run this in PostgreSQL after ETL completes
-- ==========================================

-- 1. Executive Market Overview View
CREATE OR REPLACE VIEW vw_powerbi_executive_summary AS
SELECT 
    c.company_name,
    c.symbol,
    s.sector_name,
    c.industry,
    c.market_cap_cr,
    c.current_price,
    c.pe_ratio,
    c.dividend_yield,
    ml.health_score,
    hl.label_name AS health_status
FROM dim_company c
LEFT JOIN dim_sector s ON c.sector_id = s.sector_id
LEFT JOIN fact_ml_scores ml ON c.company_id = ml.company_id
LEFT JOIN dim_health_label hl ON ml.label_id = hl.label_id;


-- 2. Financial Performance Trend View
CREATE OR REPLACE VIEW vw_powerbi_financial_trend AS
SELECT 
    c.company_name,
    c.symbol,
    s.sector_name,
    y.year_value,
    y.financial_year,
    pl.revenue,
    pl.expenses,
    pl.operating_profit,
    pl.opm_percentage,
    pl.net_profit,
    pl.eps
FROM fact_profit_loss pl
JOIN dim_company c ON pl.company_id = c.company_id
JOIN dim_sector s ON c.sector_id = s.sector_id
JOIN dim_year y ON pl.year_id = y.year_id;


-- 3. Balance Sheet & Leverage View
CREATE OR REPLACE VIEW vw_powerbi_balance_sheet AS
SELECT 
    c.company_name,
    c.symbol,
    y.year_value,
    bs.equity_capital,
    bs.reserves,
    bs.borrowings,
    bs.total_liabilities,
    bs.fixed_assets,
    bs.total_assets,
    fa.debt_to_equity,
    fa.roce_percentage,
    fa.roe_percentage
FROM fact_balance_sheet bs
JOIN dim_company c ON bs.company_id = c.company_id
JOIN dim_year y ON bs.year_id = y.year_id
JOIN fact_analysis fa ON bs.company_id = fa.company_id AND bs.year_id = fa.year_id;


-- 4. Cash Flow View
CREATE OR REPLACE VIEW vw_powerbi_cash_flow AS
SELECT
    c.company_name,
    c.symbol,
    y.year_value,
    cf.operating_cash_flow,
    cf.investing_cash_flow,
    cf.financing_cash_flow,
    cf.net_cash_flow
FROM fact_cash_flow cf
JOIN dim_company c ON cf.company_id = c.company_id
JOIN dim_year y ON cf.year_id = y.year_id;

-- 5. Anomaly & Forecasting View
CREATE OR REPLACE VIEW vw_powerbi_ml_insights AS
SELECT
    c.company_name,
    c.symbol,
    s.sector_name,
    ml.anomaly_flag,
    ml.anomaly_score,
    ml.forecasted_revenue_1yr,
    ml.forecasted_revenue_3yr,
    pc.pro_con_type,
    pc.description AS analysis_note
FROM fact_ml_scores ml
JOIN dim_company c ON ml.company_id = c.company_id
JOIN dim_sector s ON c.sector_id = s.sector_id
LEFT JOIN fact_pros_cons pc ON c.company_id = pc.company_id;
