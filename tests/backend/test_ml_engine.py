"""
ML Engine tests
"""

import pytest
from django.test import TestCase
from apps.companies.models import Company
from apps.ml_engine.models import MLScore


class MLEngineTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            name='Test Company',
            symbol='TEST',
            isin='INE000TEST01',
            sector='IT',
            industry='Tech'
        )
    
    def test_health_score_creation(self):
        score = MLScore.objects.create(
            company=self.company,
            health_score=85.5
        )
        self.assertEqual(score.health_score, 85.5)
