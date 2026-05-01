import pandas as pd
import numpy as np
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class DataTransformer:
    """
    Cleans, normalizes, and enriches financial data.
    """
    def __init__(self, dataframes: Dict[str, pd.DataFrame]):
        self.dfs = dataframes
        self.cleaned_dfs: Dict[str, pd.DataFrame] = {}

    def transform(self) -> Dict[str, pd.DataFrame]:
        logger.info("Starting data transformation...")
        
        for table_name, df in self.dfs.items():
            # 1. Standard cleaning for all tables
            df = self._clean_general(df)
            
            # 2. Table specific transformations
            if 'company' in table_name.lower():
                df = self._transform_company(df)
            elif 'profit_loss' in table_name.lower() or 'pl' in table_name.lower():
                df = self._transform_financials(df, 'pl')
            elif 'balance_sheet' in table_name.lower() or 'bs' in table_name.lower():
                df = self._transform_financials(df, 'bs')
            elif 'cash_flow' in table_name.lower() or 'cf' in table_name.lower():
                df = self._transform_financials(df, 'cf')
                
            self.cleaned_dfs[table_name] = df
            logger.info(f"Transformed {table_name} - Output rows: {len(df)}")
            
        return self.cleaned_dfs

    def _clean_general(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle nulls, duplicates, and basic text cleaning."""
        # Drop fully duplicate rows
        df = df.drop_duplicates()
        
        # Replace empty strings or 'null' text with NaN
        df = df.replace(r'^\s*$', np.nan, regex=True)
        df = df.replace(['null', 'None', 'NULL'], np.nan)
        
        # Strip whitespace from object columns
        obj_cols = df.select_dtypes(include=['object']).columns
        for col in obj_cols:
            df[col] = df[col].astype(str).str.strip()
            
        return df

    def _transform_company(self, df: pd.DataFrame) -> pd.DataFrame:
        """Specific transforms for company dimension."""
        # Ensure numeric columns are floats
        numeric_cols = ['market_cap_cr', 'current_price', 'pe_ratio', 'dividend_yield', 'roce', 'roe']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
        
        # Upper case symbols
        if 'symbol' in df.columns:
            df['symbol'] = df['symbol'].str.upper()
            
        return df

    def _transform_financials(self, df: pd.DataFrame, statement_type: str) -> pd.DataFrame:
        """Specific transforms for fact tables (financials)."""
        # Convert all financial metrics to numeric
        exclude_cols = ['id', 'company_id', 'year_id', 'symbol', 'financial_year']
        numeric_cols = [c for c in df.columns if c not in exclude_cols]
        
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
            
        # Compute derived metrics based on statement type
        if statement_type == 'pl':
            if 'operating_profit' in df.columns and 'revenue' in df.columns:
                df['opm_percentage'] = np.where(df['revenue'] > 0, 
                                                (df['operating_profit'] / df['revenue']) * 100, 
                                                0)
        return df

if __name__ == "__main__":
    pass
