from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import HistoricalPerformance
from .serializer import HistoricalPerformanceSerializer

@api_view(['GET'])
def index(request):
    historical_performances = HistoricalPerformance.objects.all()
    serializer = HistoricalPerformanceSerializer(historical_performances, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
