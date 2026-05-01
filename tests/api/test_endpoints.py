"""
API endpoint tests
"""

import pytest
from rest_framework.test import APITestCase
from rest_framework import status


class APITestCase(APITestCase):
    def test_companies_endpoint(self):
        response = self.client.get('/api/companies/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
