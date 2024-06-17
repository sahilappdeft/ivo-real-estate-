from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import*

app_name = 'office'

router = DefaultRouter()
router.register(r'roles', CompanyRoleViewSet)
router.register(r'unit', OfficeUnitViewSet)
router.register(r'offices', OfficeApiView, basename='offices')

urlpatterns = [
    path('', include(router.urls)),
    # path('offices/', OfficeApiView.as_view(), name='offices'),
    # path('roles/', CompanyRoleApiView.as_view(), name='office-list'),
]
