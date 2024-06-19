from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import*

app_name = 'office'

router = DefaultRouter()
router.register(r'employee/(?P<company>\d+)', EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
