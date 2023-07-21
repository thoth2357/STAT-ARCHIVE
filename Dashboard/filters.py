import django_filters
from django import forms
from django.db.models import Q
from .models import PastQuestion, Project, TextBook, Sessions
from .utils import convert_list_to_queryset, unionalize_models


CATEGORY = (
    ("Exam_Questions", "Exam Questions"),
    ("Text_Questions", "Text Questions"),
    ("Textbooks", "Textbooks"),
    ("Projects", "Projects"),
)


class ResourcesFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method="search_filter",
    )
    category = django_filters.ChoiceFilter(
        method="category_filter",
        empty_label="Category",
        choices=CATEGORY,
    )
    session = django_filters.ModelChoiceFilter(
        method="session_filter",
        queryset=Sessions.objects.all(),
        empty_label="Session",
    )
        
    def search_filter(self, queryset, name, value):
        
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
    
    def category_filter(self, queryset, name, value):
        print("got here seyi oye",name, value,queryset)
        # queryset = unionalize_models(PastQuestion, TextBook, Project)
        if value == "Textbooks":
            id_name_list = [(item['id'], item['Name']) for item in queryset]
            found_textbooks = TextBook.objects.filter(id__in=[item[0] for item in id_name_list], Name__in=[item[1] for item in id_name_list])
            print(found_textbooks, "God is good")
            return found_textbooks
        elif value == "Projects":
            id_name_list = [(item['id'], item['Name']) for item in queryset]
            found_projects = Project.objects.filter(id__in=[item[0] for item in id_name_list], Name__in=[item[1] for item in id_name_list])
            print(found_projects, "God is good")
            return found_projects
        elif value == "Exam_Questions":
            id_name_list = [(item['id'], item['Name'], item['Type']) for item in queryset]
            found_examques = PastQuestion.objects.filter(id__in=[item[0] for item in id_name_list], Name__in=[item[1] for item in id_name_list], Type="Exam_Questions")
            print(found_examques, "God is good")
            return found_examques
        elif value == "Text_Questions":
            print("\n\n",queryset)
            id_name_list = [(item['id'], item['Name'], item['Type']) for item in queryset]
            found_textques = PastQuestion.objects.filter(id__in=[item[0] for item in id_name_list], Name__in=[item[1] for item in id_name_list], Type="Text_Questions")
            print(found_textques, "God is good")
            return found_textques



    def session_filter(self,queryset, name, value):
        print("got to search mr",value,name)
        print(queryset)
        return queryset