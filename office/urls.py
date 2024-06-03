from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OfficeViewSet

router = DefaultRouter()
router.register(r'offices', OfficeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
