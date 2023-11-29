from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Avg, F
from .models import HistoricalPerformance
from vendorApi.models import Vendor


@api_view(['GET'])
def vendor_performance(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)

    vendor.update_performance_metrics()

    performances = HistoricalPerformance.objects.filter(vendor=vendor)

    if performances.count() > 0:
        on_time_delivery_rate = performances.aggregate(Avg('on_time_delivery_rate'))[
            'on_time_delivery_rate__avg']
        quality_rating_avg = performances.aggregate(Avg('quality_rating_avg'))[
            'quality_rating_avg__avg']
        average_response_time = performances.aggregate(Avg('average_response_time'))[
            'average_response_time__avg']
        fulfillment_rate = performances.aggregate(Avg('fulfillment_rate'))[
            'fulfillment_rate__avg']
    else:
        on_time_delivery_rate = quality_rating_avg = average_response_time = fulfillment_rate = None

    return Response({
        'on_time_delivery_rate': on_time_delivery_rate,
        'quality_rating_avg': quality_rating_avg,
        'average_response_time': average_response_time,
        'fulfillment_rate': fulfillment_rate,
    })
