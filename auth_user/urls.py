from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.RegisterUser.as_view(), name='signup'),
    path('verify-email/', views.VerifyEmail.as_view(), name='verify_email'),
    # path('login/', views.Login.as_view(), name='login'),
    
    path('change-password/', views.ChangePassword.as_view(), name='change_password'),
    path('send-otp/<str:type>/', views.SendOtp.as_view(), name='send-otp' ),
    
    path('forgot-password/', views.ForgotPassword.as_view(), name='forgot-password'),
    path('forgot-otp/', views.ForgotPassword.as_view(), name='forgot-otp'),
    path('forgot-email/', views.ForgotPassword.as_view(), name='forgot-email'),
    path('forgot-password-sucess/', views.ForgotPawwordSucess.as_view(), name='forgot-sucess'),
    
]