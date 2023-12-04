from django.db import models
from django.utils import timezone
from vendorApi.models import Vendor


class PurchaseOrder(models.Model):
    """
    Model representing a purchase order.

    Attributes:
    - po_number: Unique identifier for the purchase order.
    - vendor: Foreign key referencing the vendor associated with the purchase order.
    - order_date: Date and time when the purchase order was created.
    - delivery_date: Date and time when the items are expected to be delivered.
    - items: JSON field containing details of the ordered items.
    - quantity: Quantity of items in the purchase order.
    - status: Current status of the purchase order (e.g., pending, completed).
    - quality_rating: Optional field for providing a quality rating for the purchase order.
    - issue_date: Date and time when the purchase order was issued.
    - acknowledgment_date: Date and time when the purchase order was acknowledged.

    Methods:
    - __str__: String representation of the purchase order.

    Custom Save Method:
    - Overrides the default save method to automatically set the acknowledgment_date if not provided.

    """
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
