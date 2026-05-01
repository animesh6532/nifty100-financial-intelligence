import logging
import pandas as pd
from typing import Dict, Tuple

logger = logging.getLogger(__name__)

class FinancialHealthEngine:
    """
    Computes a weighted financial health score (0-100) and assigns a health label.
    Weights:
    - Profitability: 25%
    - Revenue Growth: 20%
    - Leverage: 20%
    - Cash Flow Quality: 15%
    - Dividend Track Record: 10%
    - Growth Trend: 10%
    """
    
    def __init__(self):
        self.weights = {
            'profitability': 0.25,
            'revenue_growth': 0.20,
            'leverage': 0.20,
            'cash_flow_quality': 0.15,
            'dividend_track': 0.10,
            'growth_trend': 0.10
        }

    def compute_score(self, metrics: Dict[str, float]) -> Tuple[float, str]:
        """
        Takes a dictionary of financial metrics and computes the overall score and label.
        
        Expected metrics:
        - opm_percentage (Operating Profit Margin)
        - revenue_growth_percentage
        - debt_to_equity
        - operating_cash_flow
        - net_profit
        - dividend_yield
        - cagr_3yr
        """
        logger.info("Computing financial health score.")
        try:
            # 1. Profitability (Scale 0-100, assuming 25% OPM is excellent)
            opm = metrics.get('opm_percentage', 0)
            prof_score = min(max(opm * 4, 0), 100)
            
            # 2. Revenue Growth (Assuming 20% YoY is excellent)
            rev_growth = metrics.get('revenue_growth_percentage', 0)
            rev_score = min(max(rev_growth * 5, 0), 100)
            
            # 3. Leverage (Lower is better. Assuming D/E > 2 is bad, 0 is excellent)
            dte = metrics.get('debt_to_equity', 0)
            if dte < 0: dte = 0
            lev_score = max(100 - (dte * 50), 0)
            
            # 4. Cash Flow Quality (OCF/Net Profit ratio. > 1 is excellent)
            ocf = metrics.get('operating_cash_flow', 0)
            np = metrics.get('net_profit', 0)
            cf_ratio = (ocf / np) if np > 0 else 0
            cf_score = min(max(cf_ratio * 100, 0), 100)
            
            # 5. Dividend Track Record (Assuming 5% yield is excellent)
            div_yield = metrics.get('dividend_yield', 0)
            div_score = min(max(div_yield * 20, 0), 100)
            
            # 6. Growth Trend (CAGR 3yr. Assuming 20% is excellent)
            cagr = metrics.get('cagr_3yr', 0)
            growth_score = min(max(cagr * 5, 0), 100)
            
            # Calculate final weighted score
            final_score = (
                prof_score * self.weights['profitability'] +
                rev_score * self.weights['revenue_growth'] +
                lev_score * self.weights['leverage'] +
                cf_score * self.weights['cash_flow_quality'] +
                div_score * self.weights['dividend_track'] +
                growth_score * self.weights['growth_trend']
            )
            
            label = self._assign_label(final_score)
            logger.info(f"Computed Score: {final_score:.2f}, Label: {label}")
            return round(final_score, 2), label

        except Exception as e:
            logger.error(f"Error computing health score: {e}")
            return 0.0, "POOR"

    def _assign_label(self, score: float) -> str:
        if score >= 80:
            return 'EXCELLENT'
        elif score >= 60:
            return 'GOOD'
        elif score >= 40:
            return 'AVERAGE'
        elif score >= 20:
            return 'WEAK'
        else:
            return 'POOR'
