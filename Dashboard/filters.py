import django_filters
from .models import PastQuestion, Project, TextBook, Sessions
from django import forms
from django.db.models import Q


CATEGORY = (
    ("Exam Questions", "Exam Questions"),
    ("Text Questions", "Text Questions"),
    ("Textbooks", "Textbooks"),
    ("Projects", "Projects"),
)


class ResourcesFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method="search_filter",
    )
    category = django_filters.ChoiceFilter(
        method="my_custom_filter",
        empty_label="Category",
        choices=CATEGORY,
    )
    session = django_filters.ModelChoiceFilter(
        queryset=Sessions.objects.all(),
        empty_label="Session",
    )

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(Name__icontains=value)
            | Q(Course_code__icontains=value)
            | Q(Lecturer_name__icontains=value)
            | Q(Author__icontains=value)
            | Q(Supervisor__icontains=value)
        )