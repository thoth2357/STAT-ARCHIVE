import random
import string
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.http.request import QueryDict
from django.core.files import File
from urllib.parse import urlparse
from .utils import create_pastquestion_thumbnail
from .models import PastQuestion, TextBook, Project

class Bibliotheca(View):
    def get(self, request):
        context = {
            'user': request.user,
        }
        return render(request, 'Bibliotheca.html', context=context)
    
    def post(self, request):
        ...


class UploadResources(View):
    def post(self,request):
        upload_type = QueryDict(urlparse(request.get_full_path()).query).get("query","")
        print(request.POST, request.FILES)
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
                Session=session,
                Type = pq_type,
                Lecturer_name = lecturer_name,
                Course_name = course_name,
                Course_code = course_code,
                Course_file = file,
            )
            try:           
                with open(output_path, 'rb') as image_file:
                    PastQuestion.objects.get(id=pq_object.id).Course_image.save(f'{thumbnail_name}.png', File(image_file))
            except Exception as e:
                pass #TODO send log to admin
            return JsonResponse({'status': 'success'})    
        elif upload_type == 'txb':
            print('text_book')
            textbook_name = request.POST.get('textbookName')
            textbook_author = request.POST.get('textbookAuthor')
            file = request.FILES.get('textbookFileInput')
            
        elif upload_type == 'prj':
            print('project')
            session = request.POST.get('session')
            topic = request.POST.get('projectTopic')
            author = request.POST.get('projectAuthor')
            supervisor = request.POST.get('projectSupervisor')
            file = request.FILES.get('projectFileInput') 
        else:
            print('error')

        return JsonResponse({'status': 'success'})