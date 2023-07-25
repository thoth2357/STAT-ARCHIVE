import django_filters
from django import forms
from django.db.models import Q
from django.db.utils import NotSupportedError
from .models import PastQuestion, Project, TextBook, Sessions
from .utils import convert_list_to_queryset, unionalize_models, filter_by_type


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
        try:
            id_name_list = [(item['id'], item['Name']) for item in queryset]
            if value == "Textbooks":
                found_resources = TextBook.objects.filter(id__in=[item[0] for item in id_name_list], Name__in=[item[1] for item in id_name_list])
            elif value == "Projects":
                found_resources = Project.objects.filter(id__in=[item[0] for item in id_name_list], Name__in=[item[1] for item in id_name_list])
            elif value == "Exam_Questions":
                found_resources = PastQuestion.objects.filter(id__in=[item[0] for item in id_name_list], Name__in=[item[1] for item in id_name_list], Type="Exam_Questions")
            elif value == "Text_Questions":
                found_resources = PastQuestion.objects.filter(id__in=[item[0] for item in id_name_list], Name__in=[item[1] for item in id_name_list], Type="Text_Questions")
        except TypeError:
            queryset = unionalize_models(PastQuestion, TextBook, Project)  # Uncomment situation when category stands alone
            id_name_list = [(item['id'], item['Name']) for item in queryset]
            if value == "Textbooks":
                found_resources = TextBook.objects.filter(id__in=[item[0] for item in id_name_list], Name__in=[item[1] for item in id_name_list])
            elif value == "Projects":
                found_resources = Project.objects.filter(id__in=[item[0] for item in id_name_list], Name__in=[item[1] for item in id_name_list])
            elif value == "Exam_Questions":
                found_resources = PastQuestion.objects.filter(id__in=[item[0] for item in id_name_list], Name__in=[item[1] for item in id_name_list], Type="Exam_Questions")
            elif value == "Text_Questions":
                found_resources = PastQuestion.objects.filter(id__in=[item[0] for item in id_name_list], Name__in=[item[1] for item in id_name_list], Type="Text_Questions")

        return found_resources

    def session_filter(self,queryset, name, value):
        try:
            filtered = queryset.filter(Session=value)
            print(filtered)
        except NotSupportedError:
                print("exception gots")
                id_name_list = [(item['id'], item['Name'], item['Type']) for item in queryset]
                print(id_name_list, 'anmelist')
                filtered = filter_by_type(id_name_list, PastQuestion, Project, value)
                
        return filtered
