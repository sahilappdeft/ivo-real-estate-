from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView

from auth_user.permission import IsTokenValid, token_required
from .models import Office, CompanyRole
from .serializers import (OfficeSerializer, OfficeAndBankAccountsSerializer,
                          CompanyRoleSerializer, CompanyRolePermissionSerializer
                        )


class OfficeApiView(APIView):
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer
    
    def get(self, request):
        # Render the HTML template for verify user
        return render(request, 'office-register.html')
    
    @method_decorator(token_required)
    def post(self, request):
        serializer = OfficeAndBankAccountsSerializer(data=request.data)

        # Add request to serializer context
        serializer.context['request'] = request
        
        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CompanyRoleApiView(APIView):
    serializer_class = CompanyRoleSerializer
    
    @method_decorator(token_required)
    def get(self, request):
        
        user=request.user
        if user.role == "company":
            company = user.company_user
        elif user.role == "employee":
            company = user.office.company
            
        # Get all CompanyRole objects   
        company_roles = CompanyRole.objects.filter(Company=company)
        
        # Serialize the data
        serializer = self.serializer_class(company_roles, many=True)
        
        # Return serialized data with status 200
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        
        data = request.data
        serializer = CompanyRolePermissionSerializer(data=data)
        
        if serializer.is_valid():
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

    