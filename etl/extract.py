"""
ETL Extract module
"""

import requests
import logging

logger = logging.getLogger(__name__)


class DataExtractor:
    @staticmethod
    def extract_from_api(api_url, params):
        """Extract data from API"""
        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Extraction error: {str(e)}")
            raise


def extract_company_data():
    """Extract company data from sources"""
    pass


def extract_financial_data():
    """Extract financial data"""
    pass
