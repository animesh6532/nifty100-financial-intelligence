# Power BI DAX Measures - NIFTY 100 Platform

Use these DAX measures in your Power BI `.pbix` file to calculate dynamic aggregations for your visual dashboards.

## 1. Top-Level KPIs

```dax
Total Market Cap (Cr) = SUM(vw_powerbi_executive_summary[market_cap_cr])

Average P/E Ratio = AVERAGE(vw_powerbi_executive_summary[pe_ratio])

Average Health Score = AVERAGE(vw_powerbi_executive_summary[health_score])

Total Revenue = SUM(vw_powerbi_financial_trend[revenue])

Total Net Profit = SUM(vw_powerbi_financial_trend[net_profit])
```

## 2. Margin & Growth Measures

```dax
Average OPM % = 
DIVIDE(
    SUM(vw_powerbi_financial_trend[operating_profit]),
    SUM(vw_powerbi_financial_trend[revenue]),
    0
) * 100

Net Profit Margin % = 
DIVIDE(
    SUM(vw_powerbi_financial_trend[net_profit]),
    SUM(vw_powerbi_financial_trend[revenue]),
    0
) * 100

Revenue YoY Growth % = 
VAR CurrentRev = SUM(vw_powerbi_financial_trend[revenue])
VAR PrevRev = CALCULATE(SUM(vw_powerbi_financial_trend[revenue]), SAMEPERIODLASTYEAR(vw_powerbi_financial_trend[year_value])) -- Requires Date Table or adjust for integer year
RETURN
DIVIDE(CurrentRev - PrevRev, PrevRev, 0)
```

## 3. Leverage & Return Measures

```dax
Average Debt to Equity = AVERAGE(vw_powerbi_balance_sheet[debt_to_equity])

Average ROE % = AVERAGE(vw_powerbi_balance_sheet[roe_percentage])

Average ROCE % = AVERAGE(vw_powerbi_balance_sheet[roce_percentage])
```

## 4. Anomaly Tracking

```dax
Total Anomalies Flagged = 
CALCULATE(
    COUNT(vw_powerbi_ml_insights[symbol]),
    vw_powerbi_ml_insights[anomaly_flag] = TRUE
)

Anomaly Rate % = 
DIVIDE(
    [Total Anomalies Flagged],
    COUNT(vw_powerbi_ml_insights[symbol]),
    0
)
```

## Dashboard Assignment Matrix

- **Executive Market Overview**: `Total Market Cap (Cr)`, `Average Health Score`, `Average P/E Ratio`
- **Company Deep Dive**: Filter by `symbol`, display all `vw_powerbi_financial_trend` metrics using a Waterfall Chart for Profit/Loss breakdown.
- **Sector Comparison Analyzer**: Matrix using `vw_powerbi_financial_trend` rows `sector_name` -> `symbol` with Margin % columns.
- **Financial Health Scorecard**: Gauge Chart using `Average Health Score`.
- **Debt & Leverage Monitor**: Scatter plot of `debt_to_equity` vs `roce_percentage`.
