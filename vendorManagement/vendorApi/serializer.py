from rest_framework import serializers
from .models import Vendor


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

    def save(self, **kwargs):
        # Handle related objects if necessary
        from purchaseApi.models import PurchaseOrder
        from historyApi.models import HistoricalPerformance
        purchase_orders_data = self.validated_data.pop('purchase_orders', [])
        historical_performances_data = self.validated_data.pop(
            'historical_performances', [])

        # Call the parent save method
        super().save(**kwargs)

        # Access the saved Vendor instance
        vendor_instance = self.instance

        # Save related PurchaseOrders
        for purchase_order_data in purchase_orders_data:
            PurchaseOrder.objects.create(
                vendor=vendor_instance, **purchase_order_data)

        # Save related HistoricalPerformances
        for historical_performance_data in historical_performances_data:
            HistoricalPerformance.objects.create(
                vendor=vendor_instance, **historical_performance_data)
