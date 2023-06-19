from django.urls import path,include # new
from .views import LoginView, RegisterView, VerifyEmailView, ForgotPasswordView,ResetPasswordView

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("verify/<uidb64>/<token>/", VerifyEmailView.as_view(), name="verify_email"),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    
]