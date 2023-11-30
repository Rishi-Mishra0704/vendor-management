from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from vendorApi.models import Vendor
from .models import HistoricalPerformance
from django.urls import reverse

class VendorPerformanceViewTestCase(TestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )

        # Create a vendor for testing
        self.vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='Test Contact',
            address='Test Address',
            vendor_code='TEST001',
            on_time_delivery_rate=0.9,
            quality_rating_avg=4.5,
            average_response_time=24.5,
            fulfillment_rate=0.95,
        )

        # Set up the API client for making requests
        self.client = APIClient()

    def test_vendor_performance(self):
        url = reverse('vendor_performance', args=[self.vendor.id])
        self.client.force_authenticate(user=self.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Add assertions based on the expected structure of the response
        self.assertIn('vendor', response.data)
        self.assertIn('on_time_delivery_rate', response.data)
        self.assertIn('quality_rating_avg', response.data)
        self.assertIn('average_response_time', response.data)
        self.assertIn('fulfillment_rate', response.data)

    # Add more tests as needed, such as testing with different data scenarios
