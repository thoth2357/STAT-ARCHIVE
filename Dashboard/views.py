import random
import string
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.http.request import QueryDict
from django.core.files import File
from urllib.parse import urlparse
from .utils import create_pastquestion_thumbnail, generate_textbook_thumbnail
from .models import PastQuestion, TextBook, Project, Sessions
from .filters import ResourcesFilter
from django_filters.views import FilterView
from django.views.generic import ListView


class Bibliotheca(View):
    def get(self, request):
        all_resources = list(PastQuestion.objects.all()) + list(TextBook.objects.all()) + list(Project.objects.all())
        sorted_resources = sorted(all_resources, key=lambda resource: resource.Date_uploaded)
        filtering = ResourcesFilter(request.GET, queryset=PastQuestion.objects.all())
        context = {
            'user': request.user,
            'sessions':Sessions.objects.all(),
            'resources':sorted_resources,
            'resources_count':len(sorted_resources),
            'filter':filtering,
            'type':"home"
        }
        return render(request, 'Bibliotheca.html', context=context)

class UploadResources(View):
    def post(self,request):
        upload_type = QueryDict(urlparse(request.get_full_path()).query).get("query","")
        if upload_type == 'pq':
            session = request.POST.get('session')
            pq_type = request.POST.get('PastQuestionsType')
            lecturer_name = request.POST.get('LecturerName')
            course_name = request.POST.get('CourseName')
            course_code = request.POST.get('CourseCode')
            file = request.FILES.get('QuestionFile')
            thumbnail_name = ''.join(random.choices(string.ascii_letters + string.digits, k=8))          
            output_path = create_pastquestion_thumbnail(course_name, course_code, lecturer_name, session, pq_type, thumbnail_name)
            pq_object = PastQuestion.objects.create(
                Session = Sessions.objects.get(id=session),
                Type = pq_type,
                Lecturer_name = lecturer_name,
                Name = course_name,
                Course_code = course_code,
                file = file,
            )
            try:           
                with open(output_path, 'rb') as image_file:
                    pq_object.thumbnail.save(f'{thumbnail_name}.png', File(image_file))
            except Exception:
                pass #TODO send log to admin
            return JsonResponse({'status': 'success'})    
        elif upload_type == 'txb':
            textbook_name = request.POST.get('textbookName')
            textbook_author = request.POST.get('textbookAuthor')
            file = request.FILES.get('textbookFile')
            
            txb_object = TextBook.objects.create(
                Name = textbook_name,
                Author = textbook_author,
                file = file,
            )
            try:
                thumbnail_path,filename = generate_textbook_thumbnail(txb_object.file.url, 'media/resources/images/textbook')
                with open(thumbnail_path, 'rb') as image_file:
                    txb_object.thumbnail.save(f'{filename}.jpg', File(image_file))
                    #TODO To delete duplicate file
            except Exception:
                ...
            return JsonResponse({'status': 'success'})
            
        elif upload_type == 'prj':
            session = request.POST.get('session')
            topic = request.POST.get('projectTopic')
            author = request.POST.get('projectAuthor')
            supervisor = request.POST.get('projectSupervisor')
            file = request.FILES.get('projectFile') 
            prj_object = Project.objects.create(
                Session = Sessions.objects.get(id=session),
                Name = topic,
                Author = author,
                Supervisor = supervisor,
                file = file
            )
            try:
                thumbnail_path,filename = generate_textbook_thumbnail(prj_object.file.url, 'media/resources/images/project')
                with open(thumbnail_path, 'rb') as image_file:
                    prj_object.thumbnail.save(f'{filename}.jpg', File(image_file))
                    #TODO To delete duplicate file
            except Exception:
                ...
            return JsonResponse({'status': 'success'})
        else:
            print('error')

        return JsonResponse({'status': 'success'})

class ResourcesSearch(FilterView):
    model = PastQuestion
    template_name = 'Bibliotheca.html'
    paginate_by = 8
    filterset_class = ResourcesFilter