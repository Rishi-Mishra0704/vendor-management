from datetime import timedelta
from django.db import models
from vendorApi.models import Vendor

# Create your models here.


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(
        null=True, blank=True, default=None)

    def recalculate_average_response_time(self):
        # Get all acknowledged purchase orders for the same vendor
        acknowledged_orders = PurchaseOrder.objects.filter(
            vendor=self.vendor,
            acknowledgment_date__isnull=False
        ).exclude(id=self.id)

        total_response_time = timedelta()

        # Calculate the total response time
        for order in acknowledged_orders:
            total_response_time += order.acknowledgment_date - order.order_date

        # Calculate the average response time
        if acknowledged_orders.exists():
            average_response_time = total_response_time / \
                len(acknowledged_orders)
        else:
            average_response_time = timedelta()

        # Update the vendor's average_response_time field
        self.vendor.average_response_time = average_response_time.total_seconds()
        self.vendor.save()

    def __str__(self):
        return f"PO #{self.po_number} - {self.vendor.name}"
