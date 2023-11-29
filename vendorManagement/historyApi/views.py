from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import HistoricalPerformance
from .serializer import HistoricalPerformanceSerializer
from vendorApi.models import Vendor

@api_view(['GET'])
def vendor_performance(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

    performance_data = HistoricalPerformance.objects.filter(vendor=vendor).last()

    if not performance_data:
        return Response({"error": "Performance data not available for this vendor"}, status=status.HTTP_404_NOT_FOUND)

    serializer = HistoricalPerformanceSerializer(performance_data)
    return Response(serializer.data, status=status.HTTP_200_OK)
