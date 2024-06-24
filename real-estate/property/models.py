from django.db import models
from utility.models import BaseModel

# Create your models here
class Building(BaseModel):
    STAIRCASE_CHOICES = [
        ('direct', 'Direct Access'),
        ('common', 'Access to Common Floor'),
        ('combined', 'Combined Access'),
    ]
    building_id = models.CharField(max_length=255)
    max_floor = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    staircase = models.CharField(max_length=255, choices=STAIRCASE_CHOICES)
    size = models.CharField(max_length=255)
    company = models.ForeignKey('office.Company',on_delete=models.CASCADE, null=False,
                               blank=False, related_name='company_building')
    
    def __str__(self):
        return self.building_id + str(self.id)
    
    
class Property(BaseModel):
    
    property_id = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=6)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city_division = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    office = models.ForeignKey('office.Office', on_delete=models.CASCADE, null=False,
                               blank=False, related_name='offic_property')
    building = models.ForeignKey('Building', on_delete=models.CASCADE, null=False,
                               blank=False, related_name='building_property')

    def __str__(self) -> str:
        return str(self.id)
    

class BuildingUnit(BaseModel):
    
    LOCATION_CHOICES = [
        ("Left", "Left"),
        ("Middle Left", "Middle Left"),
        ("Middle", "Middle"),
        ("Middle Right", "Middle Right"),
        ("Right", "Right"),
        ("Not Practical", "Not Practical"),
    ]

    WATER_HEATING_CHOICES = [
        ("Centralized", "Centralized"),
        ("Decentralized", "Decentralized"),
    ]

    UNIT_TYPE_CHOICES = [
        ("Office", "Office"),
        ("Retail Space", "Retail Space"),
        ("Residential", "Residential"),
    ]
    
    name = models.CharField(max_length=255)
    floor = models.CharField(max_length=255)
    location = models.CharField(max_length=20,choices=LOCATION_CHOICES,)
    water_heating =  models.CharField(max_length=20,choices=WATER_HEATING_CHOICES,)
    unit_type =  models.CharField(max_length=20,choices=UNIT_TYPE_CHOICES,)
    property = models.OneToOneField('Property', on_delete=models.CASCADE, null=False,
                               blank=False, related_name='property_building_unit')
    
    def __str__(self) -> str:
        return self.name
    
    
class Room(BaseModel):
    
    doors = models.IntegerField()
    size = models.CharField(max_length=255)
    name = models.CharField(max_length=255, null=True, blank=True)
    building_unit = models.ForeignKey('BuildingUnit', on_delete=models.CASCADE, null=False,
                               blank=False, related_name='building_unit_rooms')
    
    def __str__(self) -> str:
        return str(self.building_unit.id)
    

class EnergyMeter(models.Model):
    PURPOSE_CHOICES = [
        ("Heat", "Heat"),
        ("Electricity", "Electricity"),
        ]

    TYPE_CHOICES = [
        ("Electricity", "Electricity"),
        ("Gas", "Gas"),
    ]

    LOCATION_CHOICES = [
        ("In unit", "In unit"),
        ("In Floor", "In Floor"),
        ("Basement", "Basement"),
    ]

    ACCESS_CHOICES = [
        ("Locked", "Locked"),
        ("Accessible", "Accessible"),
    ]
    purpose = models.CharField(max_length=20,choices=PURPOSE_CHOICES,)
    type = models.CharField(max_length=20,choices=TYPE_CHOICES,)
    name_id = models.CharField(max_length=255)
    location = models.CharField(max_length=20,choices=LOCATION_CHOICES,)
    access = models.CharField(max_length=20,choices=ACCESS_CHOICES,)
    amount = models.CharField(max_length=255)
    building_unit = models.ForeignKey('BuildingUnit', on_delete=models.CASCADE, null=False,
                               blank=False, related_name='building_unit_meters')

    def __str__(self):
        return self.name_id

    