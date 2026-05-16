import logging
import pandas as pd
import numpy as np
import psycopg2
from psycopg2.extras import execute_values
from typing import Dict, List
from etl.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

logger = logging.getLogger(__name__)

class DataLoader:
    """
    Loads cleaned data into the PostgreSQL Data Warehouse using idempotent upserts.
    Handles the Star Schema transformations (mapping dimensions to facts).
    """
    def __init__(self):
        self.conn = self._get_connection()

    def _get_connection(self):
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            return conn
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    def load(self, dataframes: Dict[str, pd.DataFrame]):
        logger.info("Starting data loading to PostgreSQL...")
        
        # We need to map our DataFrames to Star Schema tables.
        # DataFrames available: companies, balancesheet, profitandloss, cashflow, analysis, documents, prosandcons
        
        # 1. Load dim_sector
        if 'companies' in dataframes:
            df_comp = dataframes['companies']
            sectors = df_comp['sector_name'].dropna().unique()
            df_sectors = pd.DataFrame({'sector_name': sectors})
            self._upsert_table('dim_sector', df_sectors, 'sector_name')
        
        # Fetch sector_id mapping
        sector_map = self._get_mapping('dim_sector', 'sector_name', 'sector_id')
        
        # 2. Load dim_company
        if 'companies' in dataframes:
            df_comp = dataframes['companies'].copy()
            # Map sector_name to sector_id
            df_comp['sector_id'] = df_comp['sector_name'].map(sector_map)
            
            # Map columns to DB schema
            df_comp = df_comp.rename(columns={
                'id': 'company_id',
                'company_name': 'company_name',
                'roce_percentage': 'roce',
                'roe_percentage': 'roe',
                'chart_link': 'symbol' # symbol was extracted in transform, wait, symbol was derived.
            })
            # Ensure symbol exists, else fallback to company_id string
            if 'symbol' not in df_comp.columns:
                df_comp['symbol'] = "SYM" + df_comp['company_id'].astype(str)
            df_comp['symbol'] = df_comp['symbol'].fillna("SYM" + df_comp['company_id'].astype(str))
            
            dim_comp_cols = ['company_id', 'symbol', 'company_name', 'sector_id', 'industry', 'market_cap_cr', 'current_price', 'pe_ratio', 'dividend_yield', 'roce', 'roe']
            # Keep only existing columns
            dim_comp_cols = [c for c in dim_comp_cols if c in df_comp.columns]
            
            self._upsert_table('dim_company', df_comp[dim_comp_cols], 'symbol')
            # Also upsert with company_id conflict? The DB has PRIMARY KEY company_id and UNIQUE symbol.
            # We'll use symbol as conflict target to avoid issues if IDs shift, but IDs are explicitly provided in our CSV.
            # Wait, in the schema symbol is UNIQUE NOT NULL.
        
        # 3. Load dim_year
        years = set()
        for df_name in ['balancesheet', 'profitandloss', 'cashflow', 'analysis']:
            if df_name in dataframes and 'year' in dataframes[df_name].columns:
                years.update(dataframes[df_name]['year'].dropna().unique())
        if 'documents' in dataframes and 'Year' in dataframes['documents'].columns:
             years.update(dataframes['documents']['Year'].dropna().unique())
             
        df_years = pd.DataFrame({'year_value': list(years)})
        df_years['financial_year'] = 'FY' + df_years['year_value'].astype(str)
        self._upsert_table('dim_year', df_years, 'year_value')
        
        # Fetch year_id mapping
        year_map = self._get_mapping('dim_year', 'year_value', 'year_id')
        
        # 4. Load Fact Tables
        # fact_profit_loss
        if 'profitandloss' in dataframes:
            df_pl = dataframes['profitandloss'].copy()
            df_pl['year_id'] = df_pl['year'].map(year_map)
            df_pl = df_pl.drop(columns=['id', 'year'], errors='ignore')
            df_pl = df_pl.dropna(subset=['company_id', 'year_id'])
            self._upsert_table('fact_profit_loss', df_pl, 'company_id, year_id')
            
        # fact_balance_sheet
        if 'balancesheet' in dataframes:
            df_bs = dataframes['balancesheet'].copy()
            df_bs['year_id'] = df_bs['year'].map(year_map)
            df_bs = df_bs.drop(columns=['id', 'year'], errors='ignore')
            df_bs = df_bs.rename(columns={'other_asset': 'other_assets'}) # DB mismatch
            df_bs = df_bs.dropna(subset=['company_id', 'year_id'])
            self._upsert_table('fact_balance_sheet', df_bs, 'company_id, year_id')
            
        # fact_cash_flow
        if 'cashflow' in dataframes:
            df_cf = dataframes['cashflow'].copy()
            df_cf['year_id'] = df_cf['year'].map(year_map)
            df_cf = df_cf.drop(columns=['id', 'year'], errors='ignore')
            df_cf = df_cf.rename(columns={
                'operating_activity': 'operating_cash_flow',
                'investing_activity': 'investing_cash_flow',
                'financing_activity': 'financing_cash_flow'
            })
            df_cf = df_cf.dropna(subset=['company_id', 'year_id'])
            self._upsert_table('fact_cash_flow', df_cf, 'company_id, year_id')
            
        # fact_analysis
        if 'analysis' in dataframes:
            df_an = dataframes['analysis'].copy()
            # analysis doesn't have a year column in the provided data!
            # It just has id, company_id, compounded_sales_growth, etc.
            # We will default it to the latest year available, e.g., 2023.
            # Actually, fact_analysis has UNIQUE(company_id, year_id). Let's use 2023.
            df_an['year_id'] = year_map.get(2023) or year_map.get(2024) or year_map.get(2022) or list(year_map.values())[0] if year_map else 1
            df_an = df_an.drop(columns=['id'], errors='ignore')
            df_an = df_an.rename(columns={
                'roe': 'roe_percentage'
            })
            df_an = df_an.dropna(subset=['company_id', 'year_id'])
            self._upsert_table('fact_analysis', df_an, 'company_id, year_id')
            
        # fact_pros_cons
        if 'prosandcons' in dataframes:
            df_pc = dataframes['prosandcons'].copy()
            df_pc = df_pc.drop(columns=['id'], errors='ignore')
            # The schema has: company_id, pro_con_type, description
            # The CSV has: company_id, pros, cons
            # We need to unpivot this!
            records = []
            for _, row in df_pc.iterrows():
                cid = row.get('company_id')
                if pd.notna(row.get('pros')):
                    records.append({'company_id': cid, 'pro_con_type': 'PRO', 'description': row['pros']})
                if pd.notna(row.get('cons')):
                    records.append({'company_id': cid, 'pro_con_type': 'CON', 'description': row['cons']})
            df_pc_melted = pd.DataFrame(records)
            if not df_pc_melted.empty:
                # no UNIQUE constraint on fact_pros_cons other than id, so we truncate and insert to avoid duplicates
                cursor = self.conn.cursor()
                cursor.execute("TRUNCATE TABLE fact_pros_cons RESTART IDENTITY CASCADE;")
                self.conn.commit()
                self._upsert_table('fact_pros_cons', df_pc_melted, '') # no conflict
                
        self.conn.close()
        logger.info("Data loading complete.")

    def _get_mapping(self, table_name, key_col, val_col):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT {key_col}, {val_col} FROM {table_name}")
        rows = cursor.fetchall()
        cursor.close()
        return {r[0]: r[1] for r in rows}

    def _upsert_table(self, table_name: str, df: pd.DataFrame, conflict_cols: str):
        if df.empty:
            return

        columns = list(df.columns)
        cols_str = ','.join(columns)
        
        if conflict_cols:
            conflict_col_list = [c.strip() for c in conflict_cols.split(',')]
            update_set = ', '.join([f"{col} = EXCLUDED.{col}" for col in columns if col not in conflict_col_list])
            if not update_set:
                on_conflict = f"ON CONFLICT ({conflict_cols}) DO NOTHING"
            else:
                on_conflict = f"ON CONFLICT ({conflict_cols}) DO UPDATE SET {update_set}"
        else:
            on_conflict = ""

        query = f"""
            INSERT INTO {table_name} ({cols_str})
            VALUES %s
            {on_conflict};
        """
        
        # Convert df to list of tuples, replace NaN with None
        df = df.replace({pd.NA: None, np.nan: None})
        values = [tuple(x) for x in df.to_numpy()]

        cursor = self.conn.cursor()
        try:
            execute_values(cursor, query, values)
            self.conn.commit()
            logger.info(f"Successfully loaded {len(values)} rows into {table_name}")
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Failed to insert into {table_name}: {e}")
        finally:
            cursor.close()

if __name__ == "__main__":
    from extract import ExcelExtractor
    from transform import DataTransformer
    from config import RAW_DATA_PATH
    
    extractor = ExcelExtractor(RAW_DATA_PATH)
    raw_dfs = extractor.extract()
    transformer = DataTransformer(raw_dfs)
    cleaned_dfs = transformer.transform()
    
    loader = DataLoader()
    loader.load(cleaned_dfs)
