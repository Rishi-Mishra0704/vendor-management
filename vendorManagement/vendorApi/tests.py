from django.utils import timezone
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from purchaseApi.models import PurchaseOrder
from .models import Vendor
from django.urls import reverse


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
        self.vendor.update_performance_metrics()
        self.assertEqual(self.vendor.historicalperformance_set.count(), 1)
        historical_performance = self.vendor.historicalperformance_set.first()
        self.assertEqual(historical_performance.on_time_delivery_rate,
                         self.vendor.on_time_delivery_rate)
        self.assertEqual(historical_performance.quality_rating_avg,
                         self.vendor.quality_rating_avg)
        self.assertEqual(historical_performance.average_response_time,
                         self.vendor.average_response_time)
        self.assertEqual(historical_performance.fulfillment_rate,
                         self.vendor.fulfillment_rate)
