from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import*

app_name = 'office'

urlpatterns = [
    path('offices/', OfficeApiView.as_view(), name='office-list'),
    path('roles/', CompanyRoleApiView.as_view(), name='office-list'),

]
