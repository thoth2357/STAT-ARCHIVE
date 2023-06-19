from django.urls import path
from .views import Bibliotheca

urlpatterns = [
    path("", Bibliotheca.as_view(), name="Bibliotheca"),
]
