from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from auth_user.permission import token_required

# Create your views here.
class Dashboard(APIView):
    """
    API endpoint for change user password with otp.
    """
    # permission_classes = (IsTokenValid,)
    
    # @method_decorator(token_required)
    def get(self, request):
        # Render the HTML template for verify user
        return render(request, 'index.html')