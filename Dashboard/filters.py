import django_filters
from django import forms
from django.db.models import Q
from .models import PastQuestion, Project, TextBook, Sessions
from .utils import convert_list_to_queryset


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
        
        print("got to search filter", name, value)
        pastquestion = PastQuestion.objects.filter(
            Q(Name__icontains=value)|
            Q(Course_code__icontains=value)|
            Q(Lecturer_name__icontains=value)
        )
        textbook = TextBook.objects.filter(
            Q(Name__icontains=value)|
            Q(Author__icontains=value)
        )
        project = Project.objects.filter(
            Q(Name__icontains=value)|
            Q(Author__icontains=value)|
            Q(Supervisor__icontains=value)
        )
        combined= list(pastquestion) + list(textbook) + list(project)
        result_queryset = convert_list_to_queryset(combined, PastQuestion, TextBook, Project)        
        # print("result_queryset",result_queryset)    
        return result_queryset