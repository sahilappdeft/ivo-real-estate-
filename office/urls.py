from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import*

app_name = 'office'

router = DefaultRouter()
router.register(r'roles/(?P<company>\d+)', CompanyRoleViewSet)
router.register(r'unit/(?P<company>\d+)', OfficeUnitViewSet)
router.register(r'offices/(?P<company>\d+)', OfficeApiView, basename='office')

urlpatterns = [
    path('', include(router.urls)),
]
