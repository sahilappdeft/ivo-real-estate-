from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView

from .models import Office
from .serializers import OfficeSerializer, OfficeAndBankAccountsSerializer


class OfficeApiView(APIView):
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer

    def get(self, request):
        # Render the HTML template for verify user
        return render(request, 'office-register.html')
    
    def post(self, request):
        serializer = OfficeAndBankAccountsSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)