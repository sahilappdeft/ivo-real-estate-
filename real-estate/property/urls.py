from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import*

app_name = 'property'

router = DefaultRouter()
router.register(r'building/(?P<company>\d+)', BuildingViewSet)
router.register(r'property/(?P<company>\d+)', PropertyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
