from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import*

app_name = 'landlord'

router = DefaultRouter()
router.register(r'landlord/(?P<company>\d+)', LandlordViewset)

urlpatterns = [
    path('', include(router.urls)),
]
