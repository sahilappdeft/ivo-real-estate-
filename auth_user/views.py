from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from utility.helpers import success, error
from .utilis import call_auth_microservice
from utility.emailTemplates import send_verify_email, send_forgot_password_email
from .models import CustomUser
from .permission import IsTokenValid


# Define Django views that communicate with FastAPI endpoints

class RegisterUser(APIView):
    """
    API endpoint for user registration.
    """
    
    def get(self, request):
        # Render the HTML template for register user
        return render(request, 'sign-up.html')
    
    def post(self, request):
        print("::::::::::::::::::::::::::::::::OPOPOPOPO")
        data = request.data

        if not 'first_name' in data and not 'last_name' in data:
            # Name is required
            return Response(error("First Name and Last Name is required", {}), status=status.HTTP_400_BAD_REQUEST)
        
        if not 'email' in data:
            # Email is required
            return Response(error("Email is required", {}), status=status.HTTP_400_BAD_REQUEST)
        
        if data.get('password') != data.get('confirmPassword'):
            # Password should same to confirm password
            return Response(error("confirm password does not match password", {}), status=status.HTTP_400_BAD_REQUEST)

          
        #hit request to auth microservice
        response = call_auth_microservice('/signup', data)

        # Check if the response is successful
        if response.status_code == 200:
            response_data = response.json()
            user_id = response_data.get('id')

            #create user wih response User-ID.
            user = CustomUser.objects.create(user_id=user_id)

            # Send OTP to user for email verification
            send_verify_email('Confirm your email', [response_data.get('email')],
                              response_data.get('otp'), response_data.get('first_name'))

            # Registration Successful
            return Response({"message": "Registration Successful"}, status=status.HTTP_200_OK)
        else:
            # Return error from the authentication microservice
            error_message = response.json().get('detail', 'Unknown error')
            return Response({"error": error_message}, status=response.status_code)


class VerifyEmail(APIView):
    """
    API endpoint for verifying user email.
    """
    
    def get(self, request):
        # Render the HTML template for verify user
        return render(request, 'otp-verfication.html')
    
    def post(self, request):
        data = request.data

        if not 'otp' in data:
            # Otp is required
            return Response(error("Otp is required.", {}), status=status.HTTP_400_BAD_REQUEST)
        
        if not 'email' in data:
            # Email is required
            return Response(error("Email is required", {}), status=status.HTTP_400_BAD_REQUEST)

        #hit request to auth microservice
        response = call_auth_microservice('/verify-email', data)

        # Check if the response is successful
        if response.status_code == 200:
            response_data = response.json()
            message = response_data.get('message')
            # Registration Successful
            return Response({"message": message}, status=status.HTTP_200_OK)
        else:
            # Return error from the authentication microservice
            error_message = response.json().get('detail', 'Unknown error')
            return Response({"error": error_message}, status=response.status_code)


class Login(APIView):
    """
    API endpoint for user login.
    """
    def get(self, request):
        # Render the HTML template for login password
        return render(request, 'sign-in.html')
    
    def post(self, request):
        data = request.data

        if not 'password' in data:
            # password is required
            return Response(error("Password is required.", {}), status=status.HTTP_400_BAD_REQUEST)
        
        if not 'email' in data:
            # Email is required
            return Response(error("Email is required", {}), status=status.HTTP_400_BAD_REQUEST)

        #hit request to auth microservice
        response = call_auth_microservice('/login', data)

        # Check if the response is successful
        if response.status_code == 200:
            response_data = response.json()
            # Registration Successful
            return Response({"message": "Login sucessfully", "data":response_data}, status=status.HTTP_200_OK)
        else:
            # Return error from the authentication microservice
            error_message = response.json().get('detail', 'Unknown error')
            return Response({"error": error_message}, status=response.status_code)
        

class ChangePassword(APIView):
    """
    API endpoint for change user password.
    """
    permission_classes = (IsTokenValid,)
    
    def post(self, request):
        data = request.data
        # Extract token from the request header
        token = request.headers.get('Authorization', '').split(' ')[-1]
        
        # Prepare data for the change password request
        data = {
            'old_password': data.get('old_password'),
            'new_password': data.get('new_password'),
            'confirm_password': data.get('confirm_password')
        }
        
        # Make a POST request to the FastAPI microservice
        response = call_auth_microservice('/change-password', data, token)
        
        # Check the response from the FastAPI microservice
        if response.status_code == 200:
            response_data = response.json()
            message = response_data.get('message')
            # Change password successfully Successful
            return Response({"message": message}, status=status.HTTP_200_OK)
        else:
            error_message = response.json().get('detail', 'Unknown error')
            return Response({"error": error_message}, status=response.status_code)


class SendOtp(APIView):
    """
    API endpoint for send otp to the user for
    reset his password.
    """

    def post(self, request, *args, **kwargs):
        data = request.data
        otp_type = self.kwargs.get('type')

        # Prepare data for the change password request
        data = {
            'email': data.get('email'),
            'type': otp_type
        }
        
        # Make a POST request to the FastAPI microservice
        response = call_auth_microservice('/send-otp', data)
        
        # Check the response from the FastAPI microservice
        if response.status_code == 200:
            response_data = response.json()
            email = response_data.get('email')
            otp = response_data.get('otp')
            first_name = response_data.get('first_name')

            if otp_type == 'forgot':
                # Send OTP to user for reset password.
                send_forgot_password_email('Forgot password', [email],
                                otp, first_name)
                
            elif otp_type == "verify":
                # Send OTP to user for email verification
                send_verify_email('Confirm your email', [response_data.get('email')],
                              response_data.get('otp'), response_data.get('first_name'))

            # Otp send successfully 
            return Response({"message": "Otp send successfully"}, status=status.HTTP_200_OK)
        else:
            error_message = response.json().get('detail', 'Unknown error')
            return Response({"error": error_message}, status=response.status_code)
        

class ForgotPassword(APIView):
    """
    API endpoint for change user password with otp.
    """
    def get(self, request):
        # Check the request path to determine which template to render
        if 'forgot-otp' in request.path:
            return render(request, 'otp-verfication.html')
        elif 'forgot-email' in request.path:
            return render(request, 'reset-email.html')
        else:
            return render(request, 'reset-password.html')
    
    def post(self, request):
        data = request.data
        
        # Prepare data for the change password request
        data = {
            'email': str(data.get('email')),
            'password': str(data.get('password')),
            'otp': str(data.get('otp')),
            'confirm_password': str( data.get('confirmPassword'))
        }
        
        # Make a POST request to the FastAPI microservice
        response = call_auth_microservice('/reset-password', data)
        
        # Check the response from the FastAPI microservice
        if response.status_code == 200:
            response_data = response.json()
            message = response_data.get('message')
            # Change password successfully Successful
            return Response({"message": message}, status=status.HTTP_200_OK)
        else:
            error_message = response.json().get('detail', 'Unknown error')
            return Response({"error": error_message}, status=response.status_code)
    

class ForgotPawwordSucess(APIView):
    """
    API endpoint for render forgot password sucess.html.
    """
    def get(self, request):
        # Render the HTML template for verify user
        return render(request, 'forgot-sucess.html')
    
    
class SetupAccount(APIView):
    def post(self, request, *args, **kwargs):
        
        # get invite employe objet
        
        # get emil from emlye object and get other user detail from request.data
        
        # hit auth microservice sign-up data
        
        # create user object here
        
        # get employe from that user
        
        # crate employeoffice object with emplye role and office 
        
        pass