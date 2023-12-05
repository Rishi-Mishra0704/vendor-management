from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import HistoricalPerformance
from .serializer import HistoricalPerformanceSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def index(request):
    historical_performances = HistoricalPerformance.objects.all()
    serializer = HistoricalPerformanceSerializer(
        historical_performances, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
