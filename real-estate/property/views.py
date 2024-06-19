from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action

from utility.helpers import success, error
from auth_user.permission import IsTokenValid
from .models import Building, Property
from .serializers import (BuildingSerializer, PropertySerializer)


class BuildingViewSet(viewsets.ModelViewSet):
    serializer_class = BuildingSerializer
    permission_classes = (IsTokenValid,)
    queryset = Building.objects.all()
    
    def list(self, request, *args, **kwargs):
        company_id = kwargs.get('company', None)
        
        if not company_id:
            return Response(error('Company not found', {}), status=status.HTTP_404_NOT_FOUND)
    
        queryset = self.queryset.filter(company__id=company_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    
class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    permission_classes = (IsTokenValid,)
    queryset = Property.objects.all()
    
    def list(self, request, *args, **kwargs):
        company_id = kwargs.get('company', None)
        
        if not company_id:
            return Response(error('Company not found', {}), status=status.HTTP_404_NOT_FOUND)
    
        queryset = self.queryset.filter(company__id=company_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)