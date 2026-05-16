import os
import logging
import pandas as pd
from typing import Dict
from etl.config import RAW_DATA_PATH

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ExcelExtractor:
    """
    Extracts data directly from existing Excel (.xlsx) files.
    Skips the first row which contains a title string in these specific files.
    """
    def __init__(self, raw_dir: str):
        self.raw_dir = raw_dir

    def extract(self) -> Dict[str, pd.DataFrame]:
        logger.info(f"Reading Excel files from {self.raw_dir}")
        dataframes = {}
        for file in os.listdir(self.raw_dir):
            if file.endswith('.xlsx'):
                # Extract the base name (e.g. 'companies' from 'companies.xlsx')
                table_name = file.replace('.xlsx', '')
                file_path = os.path.join(self.raw_dir, file)
                try:
                    # header=1 because row 0 is a title
                    df = pd.read_excel(file_path, header=1)
                    dataframes[table_name] = df
                    logger.info(f"Loaded {table_name} from Excel with {len(df)} rows.")
                except Exception as e:
                    logger.error(f"Error loading {file_path}: {e}")
        return dataframes

if __name__ == "__main__":
    extractor = ExcelExtractor(RAW_DATA_PATH)
    dfs = extractor.extract()
    for name, df in dfs.items():
        print(f"{name}: {len(df)} rows")
