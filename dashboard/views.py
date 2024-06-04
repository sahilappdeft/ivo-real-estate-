from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.
class Dashboard(APIView):
    """
    API endpoint for change user password with otp.
    """
    
    def get(self, request):
        # Render the HTML template for verify user
        return render(request, 'index.html')