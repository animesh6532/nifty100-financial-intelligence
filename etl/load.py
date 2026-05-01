"""
ETL Load module
"""

import logging
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class DataLoader:
    @staticmethod
    def load_to_database(data, model):
        """Load transformed data into database"""
        # Bulk create or update
        pass


def load_companies(data):
    """Load company data"""
    pass


def load_financial_data(data):
    """Load financial data"""
    pass
