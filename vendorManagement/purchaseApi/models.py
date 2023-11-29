from django.db import models
from django.utils import timezone
from vendorApi.models import Vendor


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
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PO #{self.po_number} - {self.vendor.name}"

    def save(self, *args, **kwargs):
        if self.acknowledgment_date is None:
            self.acknowledgment_date = timezone.now()
        super().save(*args, **kwargs)
