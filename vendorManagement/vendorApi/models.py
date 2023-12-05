from django.db import models, transaction
from django.db.models import Avg
from django.utils import timezone


# Create your models here.


class Vendor(models.Model):
    """
        Model representing a vendor.

        Attributes:
        - name: Name of the vendor.
        - contact_details: Contact details of the vendor.
        - address: Address of the vendor.
        - vendor_code: Unique code for the vendor.
        - on_time_delivery_rate: Percentage of on-time deliveries.
        - quality_rating_avg: Average quality rating of completed purchase orders.
        - average_response_time: Average response time from acknowledgment to issue date.
        - fulfillment_rate: Percentage of successfully completed purchase orders.
        """

    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def update_on_time_delivery_rate(self):
        """
        Update the on-time delivery rate for the vendor.

        Calculates the percentage of on-time deliveries based on completed purchase orders.

        Steps:
        1. Retrieve completed purchase orders.
        2. Filter on-time deliveries based on the delivery date being on or before the current time.
        3. Calculate the on-time delivery rate as the percentage of on-time deliveries to total completed purchase orders.

        Result:
        - Updates the `on_time_delivery_rate` attribute of the vendor.
        """
        completed_pos = self.purchaseorder_set.filter(status='completed')
        on_time_delivery_pos = completed_pos.filter(
            delivery_date__lte=timezone.now())
        total_completed_pos = completed_pos.count()

        if total_completed_pos > 0:
            on_time_delivery_count = on_time_delivery_pos.count()
            self.on_time_delivery_rate = (
                on_time_delivery_count / total_completed_pos) * 100
        else:
            self.on_time_delivery_rate = 0.0

    def update_quality_rating_avg(self):
        """
        Update the average quality rating for the vendor.

        Calculates the average quality rating of completed purchase orders.

        Steps:
        1. Retrieve completed purchase orders with a non-null quality rating.
        2. Calculate the average quality rating using the `aggregate` function.

        Result:
        - Updates the `quality_rating_avg` attribute of the vendor.
        """
        completed_pos = self.purchaseorder_set.filter(
            status='completed', quality_rating__isnull=False)
        total_completed_pos = completed_pos.count()

        if total_completed_pos > 0:
            self.quality_rating_avg = completed_pos.aggregate(
                Avg('quality_rating'))['quality_rating__avg']
        else:
            self.quality_rating_avg = 0.0

    def update_average_response_time(self):
        """
        Update the average response time for the vendor.

        Calculates the average response time from acknowledgment to issue date.

        Steps:
        1. Retrieve acknowledged purchase orders.
        2. Calculate the response time for each acknowledged purchase order.
        3. Calculate the average response time based on all acknowledged purchase orders.

        Result:
        - Updates the `average_response_time` attribute of the vendor.
        """
        acknowledged_pos = self.purchaseorder_set.filter(
            acknowledgment_date__isnull=False)
        total_acknowledged_pos = acknowledged_pos.count()

        if total_acknowledged_pos > 0:
            response_times = [
                (po.acknowledgment_date - po.issue_date).total_seconds()
                for po in acknowledged_pos if po.issue_date and po.acknowledgment_date
            ]
            self.average_response_time = sum(
                response_times) / total_acknowledged_pos
        else:
            self.average_response_time = 0.0

    def update_fulfillment_rate(self):
        """
        Update the fulfillment rate for the vendor.

        Calculates the percentage of successfully completed purchase orders.

        Steps:
        1. Retrieve total purchase orders for the vendor.
        2. Filter successfully completed purchase orders.
        3. Calculate the fulfillment rate as the percentage of successful orders to total purchase orders.

        Result:
        - Updates the `fulfillment_rate` attribute of the vendor.
        """
        total_pos = self.purchaseorder_set.count()

        if total_pos > 0:
            successful_pos = self.purchaseorder_set.filter(
                status='completed', acknowledgment_date__isnull=False)
            successful_pos_count = successful_pos.count()
            self.fulfillment_rate = (successful_pos_count / total_pos) * 100
        else:
            self.fulfillment_rate = 0.0

    def save(self, *args, **kwargs):
        """
        Save the vendor instance and create a historical performance record.

        Overrides the default save method to create a historical performance record after saving.

        Steps:
        1. Save the vendor instance.
        2. Create a historical performance record with the current performance metrics.

        Result:
        - Vendor instance is saved, and a historical performance record is created.
        """
        from historyApi.models import HistoricalPerformance
        try:
            super().save(*args, **kwargs)  # Save the Vendor instance first

            # Create a historical performance record with a timestamp
            historical_performance = HistoricalPerformance(
                vendor=self,
                on_time_delivery_rate=self.on_time_delivery_rate,
                quality_rating_avg=self.quality_rating_avg,
                average_response_time=self.average_response_time,
                fulfillment_rate=self.fulfillment_rate,
            )
            historical_performance.save()

        except Exception as e:
            print(f"Error saving vendor: {e}")

    @transaction.atomic()
    def update_performance_metrics(self):
        """
        Update all performance metrics for the vendor in a transaction.

        Calls individual methods to update on-time delivery rate, quality rating, response time, and fulfillment rate.

        Steps:
        1. Update on-time delivery rate.
        2. Update average quality rating.
        3. Update average response time.
        4. Update fulfillment rate.
        5. Save the vendor instance.

        Result:
        - All performance metrics are updated, and changes are saved in a transaction.
        """

        self.update_on_time_delivery_rate()
        self.update_quality_rating_avg()
        self.update_average_response_time()
        self.update_fulfillment_rate()

        self.save()

    def __str__(self):
        return self.name
