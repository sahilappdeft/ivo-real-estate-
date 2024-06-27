from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.RegisterUser.as_view(), name='signup'),
    # path('verify-email/', views.VerifyEmail.as_view(), name='verify_email'),
    path('verify-otp/<str:type>/', views.VerifyOtp.as_view(), name='verify_otp'),
    path('setup-account/', views.SetupAccount.as_view(), name='setup-account'),
    path('login/', views.Login.as_view(), name='login'),
    path('check-user/', views.GetUserByEmail.as_view(), name='user-by-email'),
    
    path('change-password/', views.ChangePassword.as_view(), name='change_password'),
    path('send-otp/<str:type>/', views.SendOtp.as_view(), name='send-otp' ),
    
    path('forgot-password/', views.ForgotPassword.as_view(), name='forgot-password'),
    path('delete_user/', views.UserDeleteView.as_view(), name='delete_user'),

]