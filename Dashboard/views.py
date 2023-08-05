import random
import string
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponseServerError
from django.http.request import QueryDict
from django.core.files import File
from urllib.parse import urlparse
from .utils import create_pastquestion_thumbnail, generate_textbook_thumbnail, remove_duplicate_file_from_path
from .models import PastQuestion, TextBook, Project, Sessions, Report
from .filters import ResourcesFilter
from django_filters.views import FilterView
from django.views.generic import ListView
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from Log.models import Log

class Bibliotheca(LoginRequiredMixin, View):
    login_url = '/'
    redirect_field_name = 'redirect_to'
    def get(self, request):
        all_resources = list(PastQuestion.objects.all()) + list(TextBook.objects.all()) + list(Project.objects.all())
        sorted_resources = sorted(all_resources, key=lambda resource: resource.Date_uploaded,reverse=True)
        filtering = ResourcesFilter(request.GET, queryset=PastQuestion.objects.all())
        paginator = Paginator(sorted_resources, 8)  # Change 8 to the desired number of items per page
        
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        # print(page_number, page_obj, page_obj.number, page_obj.paginator.num_pages)
        context = {
            'user': request.user,
            'sessions':Sessions.objects.all(),
            'resources':page_obj,
            'filter':filtering,
            'type':"home"
        }
        return render(request, 'Bibliotheca.html', context=context)

class UploadResources(LoginRequiredMixin, View):
    login_url = '/'
    redirect_field_name = 'redirect_to'
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
            
            if file.content_type == 'application/pdf':
                # Check if a similar PastQuestion object already exists
                try:
                    if pq_type != 'Exam_Questions' and pq_type != 'Text_Questions':
                        return HttpResponseServerError("😠😠😠..Choose the Type of the Past Questions ,Please.")
                    similar_pq = PastQuestion.objects.filter(
                        Session=Sessions.objects.get(id=session),
                        Type=pq_type,
                        Lecturer_name=lecturer_name,
                        Name=course_name,
                        Course_code=course_code
                    )
                except Exception:
                    return HttpResponseServerError("😭😭..You might have missed a detail of your PQ, check again")
                
                if similar_pq:
                    return HttpResponseServerError("A similar PastQuestion already exists.")

                
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
                        remove_duplicate_file_from_path(output_path)
                except Exception as e:
                    Log.objects.create(GeneratedBy="UploadResourcesView", ExceptionMessage=e)

                return JsonResponse({'status': 'success'})
            else:
                return HttpResponseServerError("🗃️ Only PDF files are allowed")

        
        
        elif upload_type == 'txb':
            textbook_name = request.POST.get('textbookName')
            textbook_author = request.POST.get('textbookAuthor')
            file = request.FILES.get('textbookFile')
            
            print("TYpe", file.content_type)
            
            if file.content_type == 'application/pdf':
                # Check if a similar TextBook object already exists
                try:
                    similar_txb = TextBook.objects.filter(
                        Name=textbook_name,
                        Author=textbook_author
                    )
                except Exception:
                    return HttpResponseServerError("😭😭..You might have missed a detail of your Textbook, check again")
                    
                if similar_txb:
                    return HttpResponseServerError("A similar Textbook already exists.")

                
                txb_object = TextBook.objects.create(
                    Name = textbook_name,
                    Author = textbook_author,
                    file = file,
                )
                
                try:
                    thumbnail_path,filename = generate_textbook_thumbnail(txb_object.file.url, 'media/resources/images/textbook')
                    with open(thumbnail_path, 'rb') as image_file:
                        txb_object.thumbnail.save(f'{filename}.jpg', File(image_file))
                        remove_duplicate_file_from_path(thumbnail_path)
                except Exception as e:
                    Log.objects.create(GeneratedBy="UploadResourcesView", ExceptionMessage=e)
                    ... 
                return JsonResponse({'status': 'success'})
            else:
                return HttpResponseServerError("🗃️ Only PDF files are allowed")

        elif upload_type == 'prj':
            session = request.POST.get('session')
            topic = request.POST.get('projectTopic')
            author = request.POST.get('projectAuthor')
            supervisor = request.POST.get('projectSupervisor')
            file = request.FILES.get('projectFile') 
            
            if file.content_type == 'application/pdf':

                # Check if a similar Project object already exists
                try:
                    similar_prj = Project.objects.filter(
                        Session=session,
                        Name=topic,
                        Author=author,
                        Supervisor=supervisor
                    )
                except Exception:
                    return HttpResponseServerError("😭😭..You might have missed a detail of your Project, check again")
                if similar_prj:
                    return HttpResponseServerError("A similar Project already exists.")
                else:
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
                            remove_duplicate_file_from_path(thumbnail_path)
                    except Exception as e:
                        Log.objects.create(GeneratedBy="UploadResourcesView", ExceptionMessage=e)
                        
                    return JsonResponse({'status': 'success'})
            else:
                return HttpResponseServerError("🗃️ Only PDF files are allowed")

        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid upload_type.'})

        # return JsonResponse({'status': 'success'})

class ResourcesSearch(LoginRequiredMixin, FilterView):
    login_url = '/'
    redirect_field_name = 'redirect_to'
    model = PastQuestion
    template_name = 'Bibliotheca.html'
    paginate_by = 8
    filterset_class = ResourcesFilter

    def render_to_response(self, context, **response_kwargs):
        # Get the filtered queryset from the context
        # print("got to here")
        filtered_queryset = context['filter'].qs
        # print('\n\n\n',filtered_queryset)
        # Create a list to store the serialized data
        serialized_data = []
        try:
            for resource in filtered_queryset:
                try:
                # Serialize each resource object into a dictionary
                    serialized_resource = {
                        'id': resource.id,
                        'Name': resource.Name,
                        'file': resource.file.url,
                        'thumbnail': resource.thumbnail.url,
                        'date-uploaded': resource.Date_uploaded
                        # Add other fields you want to include in the JSON response
                    }
                    # Append the serialized resource to the list
                    serialized_data.append(serialized_resource)
                    serialized_data = sorted(serialized_data, key=lambda x: x['date-uploaded'],reverse=True)
                except ValueError:
                    serialized_resource = {
                        'id': resource['id'],
                        'Name': resource['Name'],
                        'file': f"{settings.MEDIA_URL}{resource['file']}",
                        'thumbnail': f"{settings.MEDIA_URL}{resource['thumbnail']}",
                        'date-uploaded':resource['Date_uploaded']
                        # Add other fields you want to include in the JSON response
                    }
                    # Append the serialized resource to the list
                    serialized_data.append(serialized_resource)
                    serialized_data = sorted(serialized_data, key=lambda x: x['date-uploaded'],reverse=True)
                    Log.objects.create(
                        GeneratedBy="ResourcesSearch",
                        ExceptionMessage=ValueError
                    )
                # print("\n\n",serialized_data, "seeeeeeeeeeeee2")
        except AttributeError:
            serialized_data = []
            try:
                for resource in filtered_queryset:
                    serialized_resource = {
                        'id': resource['id'],
                        'Name': resource['Name'],
                        'file': f"{settings.MEDIA_URL}{resource['file']}",
                        'thumbnail': f"{settings.MEDIA_URL}{resource['thumbnail']}",
                        'date-uploaded':resource['Date_uploaded']
                        # Add other fields you want to include in the serialized dictionary
                    }
                    # Append the serialized resource to the list
                    serialized_data.append(serialized_resource)
                    # print(serialized_data, "seeeeeeeeeeeee")
                    serialized_data = sorted(serialized_data, key=lambda x: x['date-uploaded'],reverse=True)
                    # print("\n\nserialized_data", serialized_data)
            except Exception as e:
                # Handle any exceptions that may occur during serialization
                Log.objects.create(GeneratedBy="ResourcesSearchView->AttributeError", ExceptionMessage=e)                

        # Return the JSON response with the serialized data
        return JsonResponse(serialized_data, safe=False)


class ResourcesReportView(LoginRequiredMixin, View):
    login_url = '/'
    redirect_field_name = 'redirect_to'
    def post(self,request):
        category = request.POST.get('cagetory')
        name = request.POST.get('name')
        message = request.POST.get('message')
        
        try:
            report_object = Report.objects.create(
                Name = name,
                Category = category,
                Message = message
            )
            report_object.save()
            return JsonResponse({"status":"success"})
        except Exception as e:
            Log.objects.create(GeneratedBy="ResourcesReportView", ExceptionMessage=e)
            return HttpResponseServerError("Error in saving Report")

def custom_404(request, exception):
        return render(request, '404.html',status=404)

def custom_500(request):
        return render(request, '500.html',status=500)
