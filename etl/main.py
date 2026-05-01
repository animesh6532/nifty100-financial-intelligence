import logging
import sys
import os

# Add parent dir to path so we can import etl modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl.config import RAW_DATA_PATH
from etl.extract import SQLExtractor, CSVExtractor
from etl.transform import DataTransformer
from etl.load import DataLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_pipeline(sql_dump_path=None):
    logger.info("Starting ETL Pipeline...")
    
    # 1. Extract
    if sql_dump_path and os.path.exists(sql_dump_path):
        extractor = SQLExtractor(sql_dump_path)
    else:
        logger.info("No SQL dump provided or found. Attempting to read from raw CSVs.")
        extractor = CSVExtractor(RAW_DATA_PATH)
        
    try:
        raw_data = extractor.extract()
        if not raw_data:
            logger.error("No data extracted. Pipeline aborted.")
            return
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        return

    # 2. Transform
    transformer = DataTransformer(raw_data)
    try:
        clean_data = transformer.transform()
    except Exception as e:
        logger.error(f"Transformation failed: {e}")
        return

    # 3. Load
    loader = DataLoader()
    try:
        loader.load(clean_data)
    except Exception as e:
        logger.error(f"Loading failed: {e}")
        return

    logger.info("ETL Pipeline completed successfully!")

if __name__ == "__main__":
    # Specify your SQL dump path here if available
    dump_path = "data/raw_dump.sql"
    run_pipeline(dump_path)
