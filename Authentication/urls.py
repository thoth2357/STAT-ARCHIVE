from django.urls import path,include # new
from .views import LoginView, RegisterView, VerifyEmailView

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("verify/<uidb64>/<token>/", VerifyEmailView.as_view(), name="verify_email")
]