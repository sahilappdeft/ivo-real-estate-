from django.db import transaction

from rest_framework import serializers
from .models import (Building, Property, BuildingUnit, Room, EnergyMeter)

  
class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'
        
        
class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'
        

class RoomSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Room
        exclude = ['building_unit']
        
        
class EnergyTableSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EnergyMeter
        exclude = ['building_unit']


class BuildingUnitSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BuildingUnit
        fields = '__all__'


class BuildingUnitRoomMeterSerializer(serializers.ModelSerializer):
    # building_unit = BuildingUnitSerializer()
    rooms = RoomSerializer(many=True)
    energy_meters = EnergyTableSerializer(many=True)
    
    class Meta:
        model = BuildingUnit
        fields = '__all__'
    
    def create(self, validated_data):
        rooms_data = validated_data.pop('rooms', [])
        energy_meters_data = validated_data.pop('energy_meters', [])
        # building_unit_unit_data = validated_data.pop('building_unit', {})
        
        # Extract property instance
        property_instance = validated_data.pop('property', None)
        
        try:
            with transaction.atomic():
                 # Assign property instance to the building unit data
                if property_instance:
                    validated_data['property'] = property_instance
                    
                # create  building unit object
                building_unit = BuildingUnit.objects.create(**validated_data)
                # Create rooms for the building unit
                for room_data in rooms_data:
                    room_instance = Room.objects.create(building_unit=building_unit,  **room_data)

                # Create energy meters for the building unit
                for energy_meter_data in energy_meters_data:
                    energy_meter_instance = EnergyMeter.objects.create(building_unit=building_unit, **energy_meter_data)
                
        except Exception as e:
            print(e)
            
            raise serializers.ValidationError({"error":"Failed to create Building unit"})

        return {
                'building_unit': BuildingUnitSerializer(building_unit).data,
                }
        
    def update(self, instance, validated_data):
        rooms_data = validated_data.pop('rooms', [])
        energy_meters_data = validated_data.pop('energy_meters', [])
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return BuildingUnitSerializer(instance).data