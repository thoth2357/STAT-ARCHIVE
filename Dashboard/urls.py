from django.urls import path
from .views import Bibliotheca

urlpatterns = [
    path("", Bibliotheca.as_view(), name="Bibliotheca"),
    path("upload/?<str:resource_type>", Bibliotheca.as_view(), name="upload"),
]
