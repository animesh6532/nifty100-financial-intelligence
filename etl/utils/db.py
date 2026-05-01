"""
Database utilities for ETL
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connections


class DatabaseManager:
    @staticmethod
    def bulk_insert(model, records, batch_size=1000):
        """Bulk insert records into database"""
        pass
    
    @staticmethod
    def bulk_update(model, records):
        """Bulk update records"""
        pass
