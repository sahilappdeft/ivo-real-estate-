from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets

from .models import Office
from .serializers import OfficeSerializer, OfficeAndBankAccountsSerializer


class OfficeViewSet(viewsets.ModelViewSet):
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer

    def create(self, request):
        serializer = OfficeAndBankAccountsSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Office and bank accounts created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)