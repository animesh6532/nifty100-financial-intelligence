import os
import re
import csv
import logging
import pandas as pd
from typing import Dict, List, Optional
from etl.config import RAW_DATA_PATH

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SQLExtractor:
    """
    Extracts data from raw SQL dumps and converts them to CSV or pandas DataFrames.
    """
    def __init__(self, sql_file_path: str):
        self.sql_file_path = sql_file_path
        self.extracted_tables: Dict[str, pd.DataFrame] = {}

    def extract(self) -> Dict[str, pd.DataFrame]:
        """
        Parses the SQL dump file to extract INSERT INTO statements.
        Returns a dictionary of DataFrames keyed by table name.
        """
        if not os.path.exists(self.sql_file_path):
            logger.error(f"SQL file not found at {self.sql_file_path}")
            raise FileNotFoundError(f"File {self.sql_file_path} not found.")

        logger.info(f"Starting extraction from {self.sql_file_path}")
        
        # Regex to match INSERT INTO statements
        insert_pattern = re.compile(r"INSERT\s+INTO\s+([`'\"]?\w+[`'\"]?)\s*\((.*?)\)\s*VALUES\s*(.*);", re.IGNORECASE | re.DOTALL)
        
        with open(self.sql_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        matches = insert_pattern.findall(content)
        
        table_data = {}
        
        for match in matches:
            table_name = match[0].strip("`'\"")
            columns = [c.strip(" `'\"") for c in match[1].split(',')]
            values_str = match[2]
            
            # Basic parsing of values (handles simple cases, but production might need sqlparse)
            # Find all tuples like (val1, val2), (val3, val4)
            value_tuples = re.findall(r"\((.*?)\)", values_str)
            
            parsed_rows = []
            for vt in value_tuples:
                # Split by comma but respect string quotes (simplistic approach)
                # A more robust approach uses csv reader on the string
                try:
                    row = [val.strip(" `'\"") if val.strip() not in ('NULL', 'null') else None for val in vt.split(',')]
                    # Pad or truncate row to match column length
                    if len(row) > len(columns):
                        row = row[:len(columns)]
                    elif len(row) < len(columns):
                        row.extend([None] * (len(columns) - len(row)))
                    parsed_rows.append(row)
                except Exception as e:
                    logger.warning(f"Failed to parse row {vt} for table {table_name}: {e}")
            
            if table_name not in table_data:
                table_data[table_name] = {'columns': columns, 'rows': parsed_rows}
            else:
                table_data[table_name]['rows'].extend(parsed_rows)
                
        # Convert to DataFrames
        for t_name, data in table_data.items():
            df = pd.DataFrame(data['rows'], columns=data['columns'])
            self.extracted_tables[t_name] = df
            
            # Save to CSV in RAW_DATA_PATH
            csv_path = os.path.join(RAW_DATA_PATH, f"{t_name}.csv")
            df.to_csv(csv_path, index=False)
            logger.info(f"Extracted table {t_name} with {len(df)} rows. Saved to {csv_path}")

        return self.extracted_tables


class CSVExtractor:
    """
    Extracts data directly from existing CSV files if SQL dump is not provided.
    """
    def __init__(self, raw_dir: str):
        self.raw_dir = raw_dir

    def extract(self) -> Dict[str, pd.DataFrame]:
        logger.info(f"Reading CSVs from {self.raw_dir}")
        dataframes = {}
        for file in os.listdir(self.raw_dir):
            if file.endswith('.csv'):
                table_name = file.replace('.csv', '')
                file_path = os.path.join(self.raw_dir, file)
                df = pd.read_csv(file_path)
                dataframes[table_name] = df
                logger.info(f"Loaded {table_name} from CSV with {len(df)} rows.")
        return dataframes

if __name__ == "__main__":
    # Example usage
    # extractor = SQLExtractor("data/sample_dump.sql")
    # extractor.extract()
    pass
