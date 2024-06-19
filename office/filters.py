from django_filters import rest_framework as filters
from .models import Office

class OfficeFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    address = filters.CharFilter(field_name='address', lookup_expr='icontains')
    
    class Meta:
        model = Office
        fields = ['name', 'address', 'office_units', 'office_rep']