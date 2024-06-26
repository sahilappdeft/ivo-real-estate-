from django.db import transaction

from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound

from utility.helpers import success, error
from office.models import Company
from auth_user.permission import IsTokenValid
from .models import Building, Property, BuildingUnit, Room, EnergyMeter
from .serializers import (BuildingSerializer, PropertySerializer, BuildingUnitRoomMeterSerializer,
                          BuildingUnitSerializer)


class BuildingViewSet(viewsets.ModelViewSet):
    '''
    This class provide the crud of the Building.
    '''
    serializer_class = BuildingSerializer
    permission_classes = (IsTokenValid,)
    queryset = Building.objects.all()
    
    def list(self, request, *args, **kwargs):
        company_id = kwargs.get('company', None)
        
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return Response(error("Company not found.", {}), status=status.HTTP_404_NOT_FOUND)
    
        queryset = self.queryset.filter(company=company)
        serializer = self.get_serializer(queryset, many=True)
        return Response(success("success", serializer.data))
    
    
class PropertyViewSet(viewsets.ModelViewSet):
    '''
    This class provide the crud of the Property.
    '''
    serializer_class = PropertySerializer
    permission_classes = (IsTokenValid,)
    queryset = Property.objects.all()
    
    def list(self, request, *args, **kwargs):
        company_id = kwargs.get('company', None)
        
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return Response(error("Company not found.", {}), status=status.HTTP_404_NOT_FOUND)
    
        queryset = self.queryset.filter(building__company=company)
        serializer = self.get_serializer(queryset, many=True)
        return Response(success("success", serializer.data))
    

class BuildingUnitViewset(viewsets.ModelViewSet):
    '''
    This class provide the crud of the BuildingUnit.
    '''
    serializer_class = BuildingUnitSerializer
    permission_classes = (IsTokenValid,)
    queryset = BuildingUnit.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = BuildingUnitRoomMeterSerializer(data=request.data)
        
        if serializer.is_valid():
            data = serializer.save()
            return Response(success("success", data), status=status.HTTP_201_CREATED)
        return Response(error(serializer.errors, {}), status=status.HTTP_400_BAD_REQUEST)
    
    
    def update(self, request, *args, **kwargs):
        
        instance = self.get_object()
        data = request.data.copy()
        serializer = BuildingUnitRoomMeterSerializer(instance, data=request.data)
        rooms_data = data.pop('rooms', [])
        energy_meters_data = data.pop('energy_meters', [])
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    data = serializer.save()

                    # Update or create rooms for the building unit
                    for room_data in rooms_data:
                        room_id = room_data.pop('id', None)
                        is_delete = room_data.pop('is_delete', False)
                        if room_id and not is_delete:
                            room_instance, created = Room.objects.update_or_create(
                                id=room_id,
                                defaults={**room_data, 'building_unit': instance}
                            )
                        elif is_delete:
                            Room.objects.get(id=room_id).soft_delete()
                        else:
                            Room.objects.create(building_unit=instance, **room_data)

                    # Update or create energy meters for the building unit
                    for energy_meter_data in energy_meters_data:
                        energy_meter_id = energy_meter_data.pop('id', None)
                        is_delete = energy_meter_data.pop('is_delete', False)
                        if energy_meter_id and not is_delete:
                            energy_meter_instance, created = EnergyMeter.objects.update_or_create(
                                id=energy_meter_id,
                                defaults={**energy_meter_data, 'building_unit': instance}
                            )
                        elif is_delete:
                            EnergyMeter.objects.get(id=energy_meter_id,).soft_delete()
                        else:
                            EnergyMeter.objects.create(building_unit=instance, **energy_meter_data)
                            
                    return Response(success("success", data), status=status.HTTP_201_CREATED)
            except Room.DoesNotExist:
                return Response(error("Room id not found", {}), status=status.HTTP_400_BAD_REQUEST)
            except EnergyMeter.DoesNotExist:
                return Response(error("Energy id not found", {}), status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)
                return Response(error("something went wrong", {}), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(error(serializer.errors, {}), status=status.HTTP_400_BAD_REQUEST)

    