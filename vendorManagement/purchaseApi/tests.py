from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from vendorApi.models import Vendor
from .models import PurchaseOrder
from rest_framework.authtoken.models import Token


class PurchaseViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
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

        self.po_data = {
            'po_number': 'PO123',
            'vendor': self.vendor,
            'order_date': '2023-01-01T12:00:00Z',
            'delivery_date': '2023-01-10T12:00:00Z',
            'items': [{'item_name': 'Item1', 'quantity': 5}],
            'quantity': 5,
            'status': 'Pending',
            'issue_date': '2023-01-05T12:00:00Z',
        }
        self.po = PurchaseOrder.objects.create(**self.po_data)

        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_purchase_orders_list(self):
        url = reverse('purchase_orders')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_purchase_order_create(self):
        url = reverse('purchase_order_create')
        response = self.client.post(url, data=self.po_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_purchase_order_detail(self):
        url = reverse('purchase_order_detail', args=[self.po.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_purchase_order_update(self):
        url = reverse('purchase_order_detail', args=[self.po.id])
        updated_data = {
            'po_number': 'PO123',
            'order_date': '2023-01-01T12:00:00Z',
            'delivery_date': '2023-01-10T12:00:00Z',
            'items': '[{"item_name": "Item1", "quantity": 5}]',
            'quantity': 5,
            'status': 'Completed',
            'acknowledgment_date': '2023-01-15T12:00:00Z',
            'issue_date': '2023-01-05T12:00:00Z',
            'vendor': self.vendor.id,
        }
        response = self.client.put(url, data=updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_po = PurchaseOrder.objects.get(pk=self.po.id)
        self.assertEqual(updated_po.quantity, 5)
        self.assertIsNotNone(updated_po.acknowledgment_date)

    def test_purchase_order_delete(self):
        url = reverse('purchase_order_detail', args=[self.po.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(PurchaseOrder.DoesNotExist):
            PurchaseOrder.objects.get(pk=self.po.id)
