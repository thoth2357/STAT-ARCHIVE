from django.urls import path
from .views import Bibliotheca, UploadResources

urlpatterns = [
    path("", Bibliotheca.as_view(), name="Bibliotheca"),
    path("upload/", UploadResources.as_view(), name="upload"),
    
]
