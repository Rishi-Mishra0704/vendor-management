from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Vendor
from purchaseApi.models import PurchaseOrder
from django.utils import timezone


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
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
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


class VendorModelTest(TestCase):

    def setUp(self):
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
        self.purchase_order_completed = PurchaseOrder.objects.create(
            vendor=self.vendor,
            po_number='PO123',  # Add a unique po_number
            order_date=timezone.now(),
            delivery_date=timezone.now(),
            items={
                'item1': 'item1',
                'item2': 'item2',
            },
            quantity=1,
            status='completed',
            quality_rating=4.0,
            issue_date=timezone.now(),
            acknowledgment_date=timezone.now(),
        )
        self.purchase_order_pending = PurchaseOrder.objects.create(
            vendor=self.vendor,
            po_number='PO456',
            order_date=timezone.now(),
            delivery_date=timezone.now(),
            items={
                'item1': 'item1',
                'item2': 'item2',
            },
            quantity=1,
            status='pending',
            issue_date=timezone.now(),
        )

    def test_update_on_time_delivery_rate(self):
        self.vendor.update_on_time_delivery_rate()
        # Assuming delivery_date is in the past for completed orders
        self.assertEqual(self.vendor.on_time_delivery_rate, 100.0)

    def test_update_quality_rating_avg(self):
        self.purchase_order_completed.quality_rating = 4.0
        self.purchase_order_completed.save()
        self.vendor.update_quality_rating_avg()
        self.assertEqual(self.vendor.quality_rating_avg, 4.0)

    def test_update_average_response_time(self):
        self.purchase_order_pending.acknowledgment_date = timezone.now()
        self.purchase_order_pending.issue_date = timezone.now() - \
            timezone.timedelta(hours=2)
        self.purchase_order_pending.save()
        self.vendor.update_average_response_time()
        self.assertEqual(self.vendor.average_response_time,
                         3600)

    def test_update_fulfillment_rate(self):
        self.vendor.update_fulfillment_rate()
        # Assuming one completed and one pending order
        self.assertEqual(self.vendor.fulfillment_rate, 50.0)
    

    def test_update_performance_metrics(self):
        # Call the update_performance_metrics method
        self.vendor.update_performance_metrics()

        # Refresh the vendor instance to get the latest data from the database
        self.vendor.refresh_from_db()

        # Assert that the metrics have been updated
        self.assertEqual(self.vendor.on_time_delivery_rate, 100.0)
        self.assertEqual(self.vendor.quality_rating_avg, 4.0)
        self.assertEqual(self.vendor.average_response_time, 0.0)  # Assuming there's no acknowledged purchase order
        self.assertEqual(self.vendor.fulfillment_rate, 50.0)  # Assuming one completed order

        # Add more assertions based on your specific logic and requirements
   