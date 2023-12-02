from django.db import models
from django.db.models import Avg
from django.utils import timezone
# Create your models here.


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def update_on_time_delivery_rate(self):
        completed_pos = self.purchaseorder_set.filter(status='completed')
        on_time_delivery_pos = completed_pos.filter(
            delivery_date__lte=timezone.now())
        total_completed_pos = completed_pos.count()

        if total_completed_pos > 0:
            on_time_delivery_count = on_time_delivery_pos.count()
            self.on_time_delivery_rate = (on_time_delivery_count / total_completed_pos) * 100
        else:
            self.on_time_delivery_rate = 0.0

    def update_quality_rating_avg(self):
        completed_pos = self.purchaseorder_set.filter(
            status='completed', quality_rating__isnull=False)
        total_completed_pos = completed_pos.count()

        if total_completed_pos > 0:
            self.quality_rating_avg = completed_pos.aggregate(
                Avg('quality_rating'))['quality_rating__avg']
        else:
            self.quality_rating_avg = 0.0

    def update_average_response_time(self):
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
        total_pos = self.purchaseorder_set.count()

        if total_pos > 0:
            successful_pos = self.purchaseorder_set.filter(
                status='completed', acknowledgment_date__isnull=False)
            successful_pos_count = successful_pos.count()
            self.fulfillment_rate = (successful_pos_count / total_pos) * 100
        else:
            self.fulfillment_rate = 0.0

    def update_performance_metrics(self):
        from historyApi.models import HistoricalPerformance

        self.update_on_time_delivery_rate()
        self.update_quality_rating_avg()
        self.update_average_response_time()
        self.update_fulfillment_rate()

        self.save()
        HistoricalPerformance.objects.create(
            vendor=self,
            on_time_delivery_rate=self.on_time_delivery_rate,
            quality_rating_avg=self.quality_rating_avg,
            average_response_time=self.average_response_time,
            fulfillment_rate=self.fulfillment_rate,
        )

    def __str__(self):
        return self.name
