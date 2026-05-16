import os
import pandas as pd
import numpy as np
import logging
from typing import Dict
from etl.config import CLEANED_DATA_PATH

logger = logging.getLogger(__name__)

class DataTransformer:
    """
    Cleans, normalizes, and enriches financial data from Excel.
    """
    def __init__(self, dataframes: Dict[str, pd.DataFrame]):
        self.dfs = dataframes
        self.cleaned_dfs: Dict[str, pd.DataFrame] = {}

    def transform(self) -> Dict[str, pd.DataFrame]:
        logger.info("Starting data transformation...")
        
        # Ensure output directory exists
        if not os.path.exists(CLEANED_DATA_PATH):
            os.makedirs(CLEANED_DATA_PATH)
        
        for table_name, df in self.dfs.items():
            if df.empty:
                continue

            # 1. Standard cleaning (NULLs, duplicates)
            df = self._clean_general(df)
            
            # 2. Table specific transformations
            if table_name == 'companies':
                df = self._transform_companies(df)
            elif table_name == 'balancesheet':
                df = self._transform_balancesheet(df)
            elif table_name == 'profitandloss':
                df = self._transform_profitandloss(df)
            elif table_name == 'cashflow':
                df = self._transform_cashflow(df)
            elif table_name == 'analysis':
                df = self._transform_analysis(df)
            elif table_name == 'documents':
                df = self._transform_documents(df)
            elif table_name == 'prosandcons':
                df = self._transform_prosandcons(df)
                
            self.cleaned_dfs[table_name] = df
            
            # Export to CSV
            csv_path = os.path.join(CLEANED_DATA_PATH, f"{table_name}.csv")
            df.to_csv(csv_path, index=False)
            logger.info(f"Transformed {table_name} - Output rows: {len(df)}. Saved to {csv_path}")
            
        return self.cleaned_dfs

    def _clean_general(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle nulls, duplicates, and basic text cleaning."""
        # Drop fully duplicate rows
        df = df.drop_duplicates()
        
        # Replace empty strings or 'null' text with NaN
        df = df.replace(r'^\s*$', np.nan, regex=True)
        df = df.replace(['null', 'None', 'NULL', '-'], np.nan)
        
        # Strip whitespace from object columns
        obj_cols = df.select_dtypes(include=['object']).columns
        for col in obj_cols:
            df[col] = df[col].astype(str).str.strip()
            # Restore True NaN after string conversion
            df[col] = df[col].replace('nan', np.nan)
            
        return df

    def _normalize_year(self, df: pd.DataFrame, col_name='year') -> pd.DataFrame:
        """Normalize year columns which might contain 'Mar 2023', '2023', etc."""
        if col_name in df.columns:
            # Extract 4-digit year
            df[col_name] = df[col_name].astype(str).str.extract(r'(\d{4})')
            df[col_name] = pd.to_numeric(df[col_name], errors='coerce')
        return df

    def _to_numeric_safe(self, df: pd.DataFrame, cols: list) -> pd.DataFrame:
        for col in cols:
            if col in df.columns:
                # Remove commas from numbers if stored as string
                if df[col].dtype == object:
                    df[col] = df[col].str.replace(',', '', regex=False)
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
        return df

    def _transform_companies(self, df: pd.DataFrame) -> pd.DataFrame:
        """Specific transforms for company dimension."""
        numeric_cols = ['face_value', 'book_value', 'roce_percentage', 'roe_percentage']
        df = self._to_numeric_safe(df, numeric_cols)
        
        # Derive symbol from chart_link or NSE profile
        # e.g., chart_link might be https://www.screener.in/company/RELIANCE/consolidated/
        if 'chart_link' in df.columns:
            df['symbol'] = df['chart_link'].astype(str).str.extract(r'/company/([^/]+)/')
            
        return df

    def _transform_balancesheet(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self._normalize_year(df, 'year')
        numeric_cols = [c for c in df.columns if c not in ['id', 'company_id', 'year']]
        df = self._to_numeric_safe(df, numeric_cols)
        
        # Compute Debt to Equity Ratio: borrowings / (equity_capital + reserves)
        if 'borrowings' in df.columns and 'equity_capital' in df.columns and 'reserves' in df.columns:
            equity = df['equity_capital'] + df['reserves']
            df['debt_to_equity'] = np.where(equity != 0, df['borrowings'] / equity, np.nan)
            
        # Compute Return on Assets (ROA) - simplified proxy using reserves/equity growth, but better if linked to Net Profit.
        # Here we just compute a structural ratio (Assets vs Liabilities match check).
        # We'll calculate real ROA later if needed, but for now we'll just keep the clean data.
        return df

    def _transform_profitandloss(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self._normalize_year(df, 'year')
        numeric_cols = [c for c in df.columns if c not in ['id', 'company_id', 'year']]
        df = self._to_numeric_safe(df, numeric_cols)
        
        # Compute Profit Margin: net_profit / sales
        if 'net_profit' in df.columns and 'sales' in df.columns:
            df['profit_margin'] = np.where(df['sales'] > 0, (df['net_profit'] / df['sales']) * 100, np.nan)
            
        return df

    def _transform_cashflow(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self._normalize_year(df, 'year')
        numeric_cols = [c for c in df.columns if c not in ['id', 'company_id', 'year']]
        df = self._to_numeric_safe(df, numeric_cols)
        return df

    def _transform_analysis(self, df: pd.DataFrame) -> pd.DataFrame:
        numeric_cols = [c for c in df.columns if c not in ['id', 'company_id']]
        df = self._to_numeric_safe(df, numeric_cols)
        return df

    def _transform_documents(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self._normalize_year(df, 'Year')
        return df

    def _transform_prosandcons(self, df: pd.DataFrame) -> pd.DataFrame:
        return df

if __name__ == "__main__":
    from extract import ExcelExtractor
    from config import RAW_DATA_PATH
    
    extractor = ExcelExtractor(RAW_DATA_PATH)
    raw_dfs = extractor.extract()
    
    transformer = DataTransformer(raw_dfs)
    cleaned_dfs = transformer.transform()
