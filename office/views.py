from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action

from auth_user.permission import IsTokenValid, token_required
from .models import Office, CompanyRole, OfficeUnit
from .serializers import (OfficeSerializer, OfficeAndBankAccountsSerializer,
                          CompanyRoleSerializer, OfficeUnitSerializer, OfficeSerializer
                        )


class OfficeApiView(APIView):
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer
    
    @action(detail=False, methods=['get'])
    @token_required  # assuming you have a token_required decorator
    def office_list(self, request):
        
        user = request.user
        # Check the user's role to determine the company
        if user.role == "company":
            company = user.company_user
        elif user.role == "employee":
            company = user.office.company
        
        # Filter offices based on the company
        offices = Office.objects.filter(company=company)
        serializer = OfficeSerializer(offices, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    
    @method_decorator(token_required)
    def post(self, request):
        serializer = OfficeAndBankAccountsSerializer(data=request.data)

        # Add request to serializer context
        serializer.context['request'] = request
        
        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class CompanyRoleViewSet(viewsets.ModelViewSet):
    '''
    This class provide the crud of the compnay role.
    '''
    serializer_class = CompanyRoleSerializer
    queryset = CompanyRole.objects.all()

    @method_decorator(token_required)
    def list(self, request):
        
        user=request.user
        if user.role == "company":
            company = user.company_user
        elif user.role == "employee":
            company = user.office.company
            
        # Get all CompanyRole objects   
        company_roles = CompanyRole.objects.filter(company=company)
        
        # Serialize the data
        serializer = self.serializer_class(company_roles, many=True)
        
        # Return serialized data with status 200
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk=None):
        try:
            company_role = self.get_queryset().get(pk=pk)
        except CompanyRole.DoesNotExist:
            return Response({"error": "Company role not found"}, status=status.HTTP_404_NOT_FOUND)
        
        company_role.soft_delete()
        return Response({"message": "Deleted Sucessfully"}, status=status.HTTP_204_NO_CONTENT)
    

class OfficeUnitViewSet(viewsets.ModelViewSet):
    '''
    This class provide the crud of the office unit.
    '''
    queryset = OfficeUnit.objects.all()
    serializer_class = OfficeUnitSerializer
    permission_classes = (IsTokenValid,)
    
    def destroy(self, request, pk=None):
        try:
            company_role = self.get_queryset().get(pk=pk)
        except OfficeUnit.DoesNotExist:
            return Response({"error": "Office unit not found"}, status=status.HTTP_404_NOT_FOUND)
        
        company_role.soft_delete()
        return Response({"message": "Deleted Sucessfully"}, status=status.HTTP_204_NO_CONTENT)