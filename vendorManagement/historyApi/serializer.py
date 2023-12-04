from rest_framework import serializers
from .models import HistoricalPerformance

from vendorApi.serializer import VendorSerializer
class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer()
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'
