"""
Seed demo data script
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.companies.models import Company, FinancialData


def seed_demo_data():
    """Seed database with demo data"""
    
    # Create sample companies
    companies_data = [
        {
            'name': 'Tata Consultancy Services',
            'symbol': 'TCS',
            'isin': 'INE467B01029',
            'sector': 'IT',
            'industry': 'Software Services',
            'market_cap': 1400000000000,
        },
        {
            'name': 'Infosys Limited',
            'symbol': 'INFY',
            'isin': 'INE009A01021',
            'sector': 'IT',
            'industry': 'Software Services',
            'market_cap': 550000000000,
        },
    ]
    
    for data in companies_data:
        company, created = Company.objects.get_or_create(
            symbol=data['symbol'],
            defaults=data
        )
        if created:
            print(f"Created company: {company.name}")


if __name__ == '__main__':
    seed_demo_data()
