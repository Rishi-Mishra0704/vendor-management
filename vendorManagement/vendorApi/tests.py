from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Vendor

class VendorTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor_data = {
            'name': 'Test Vendor',
            'contact_details': 'Test Contact Details',
            'address': 'Test Address',
            'vendor_code': '123',
            'on_time_delivery_rate': 0.8,
            'quality_rating_avg': 4.2,
            'average_response_time': 24.5,
            'fulfillment_rate': 0.9,
        }
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_vendors(self):
        url = reverse('vendors')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_vendor(self):
        url = reverse('vendors_create')
        response = self.client.post(url, self.vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_vendor(self):
        url = reverse('vendors_create')
        response = self.client.post(url, {'name': ''}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_vendor_detail(self):
        vendor = Vendor.objects.create(name='Test Vendor', vendor_code='456')
        url = reverse('vendor_detail', args=[vendor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_vendor_detail(self):
        vendor = Vendor.objects.create(name='Test Vendor', vendor_code='789')
        url = reverse('vendor_detail', args=[vendor.id])

        updated_data = {
            'name': 'Updated Vendor',
            'contact_details': 'Updated Contact Details',
            'address': 'Updated Address',
            'vendor_code': '789',
            'on_time_delivery_rate': 0.9,
            'quality_rating_avg': 4.5,
            'average_response_time': 20.0,
            'fulfillment_rate': 0.95,
        }

        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_vendor_detail(self):
        vendor = Vendor.objects.create(name='Test Vendor', vendor_code='1011')
        url = reverse('vendor_detail', args=[vendor.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_vendor_performance(self):
        vendor = Vendor.objects.create(name='Test Vendor', vendor_code='1213')
        url = reverse('vendor_performance', args=[vendor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
