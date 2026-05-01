import logging
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from typing import Dict, List
from etl.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

logger = logging.getLogger(__name__)

class DataLoader:
    """
    Loads transformed data into the PostgreSQL Data Warehouse using idempotent upserts.
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
        
        # Define loading order to respect Foreign Keys
        load_order = [
            ('dim_sector', 'sector_name'),
            ('dim_year', 'year_value'),
            ('dim_company', 'symbol'),
            ('fact_profit_loss', 'company_id, year_id'),
            ('fact_balance_sheet', 'company_id, year_id'),
            ('fact_cash_flow', 'company_id, year_id'),
            ('fact_analysis', 'company_id, year_id')
        ]
        
        for table_name, conflict_cols in load_order:
            # We assume df key might not perfectly match if it's extracted from arbitrary SQL,
            # but we look for a match.
            matched_key = None
            for key in dataframes.keys():
                if table_name in key.lower():
                    matched_key = key
                    break
            
            if matched_key:
                df = dataframes[matched_key]
                self._upsert_table(table_name, df, conflict_cols)
            else:
                logger.info(f"No data found for table {table_name}, skipping.")
                
        self.conn.close()
        logger.info("Data loading complete.")

    def _upsert_table(self, table_name: str, df: pd.DataFrame, conflict_cols: str):
        if df.empty:
            logger.warning(f"DataFrame for {table_name} is empty. Skipping.")
            return

        # Prepare columns and values
        columns = list(df.columns)
        # remove 'id' if it exists since it's serial usually, but we keep it if it's explicitly inserted.
        if 'id' in columns and table_name.startswith('fact_'):
             # let sequences handle it or keep it if it's an explicit UPSERT
             pass
             
        cols_str = ','.join(columns)
        
        # Prepare ON CONFLICT DO UPDATE clause
        conflict_col_list = [c.strip() for c in conflict_cols.split(',')]
        update_set = ', '.join([f"{col} = EXCLUDED.{col}" for col in columns if col not in conflict_col_list])
        
        # If there's nothing to update (e.g. only conflict cols), just DO NOTHING
        if not update_set:
            on_conflict = f"ON CONFLICT ({conflict_cols}) DO NOTHING"
        else:
            on_conflict = f"ON CONFLICT ({conflict_cols}) DO UPDATE SET {update_set}"

        query = f"""
            INSERT INTO {table_name} ({cols_str})
            VALUES %s
            {on_conflict};
        """
        
        # Convert df to list of tuples
        # Replace NaN with None
        df = df.replace({pd.NA: None})
        values = [tuple(x) for x in df.to_numpy()]

        cursor = self.conn.cursor()
        try:
            execute_values(cursor, query, values)
            self.conn.commit()
            logger.info(f"Successfully upserted {len(values)} rows into {table_name}")
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Failed to upsert into {table_name}: {e}")
            raise
        finally:
            cursor.close()

if __name__ == "__main__":
    pass
