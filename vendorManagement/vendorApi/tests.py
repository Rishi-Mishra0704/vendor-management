from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Vendor
from django.urls import reverse


class VendorViewsTestCase(TestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )

        # Create a vendor for testing
        self.vendor_data = {
            'name': 'Test Vendor',
            'contact_details': 'Test Contact',
            'address': 'Test Address',
            'vendor_code': 'TEST001',
            'on_time_delivery_rate': 0.9,
            'quality_rating_avg': 4.5,
            'average_response_time': 24.5,
            'fulfillment_rate': 0.95,
        }
        self.vendor = Vendor.objects.create(**self.vendor_data)

        self.client = APIClient()

    def test_vendor_list(self):
        url = reverse('vendors')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vendor_create(self):
        url = reverse('vendors_create')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=self.vendor_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vendor_detail(self):
        url = reverse('vendor_detail', args=[self.vendor.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vendor_update(self):
        url = reverse('vendor_detail', args=[self.vendor.id])
        updated_data = {
            'name': 'Updated Vendor Name',
            'contact_details': 'Updated Contact',
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data=updated_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_vendor_delete(self):
        url = reverse('vendor_detail', args=[self.vendor.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
