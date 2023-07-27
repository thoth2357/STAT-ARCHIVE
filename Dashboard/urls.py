from django.urls import path
from .views import Bibliotheca, UploadResources, ResourcesSearch, ResourcesReportView

urlpatterns = [
    path("", Bibliotheca.as_view(), name="Bibliotheca"),
    path("upload/", UploadResources.as_view(), name="upload"),
    path("resource-search/", ResourcesSearch.as_view(), name="resource-search"),
    path("report/", ResourcesReportView.as_view(), name="report"),
]
