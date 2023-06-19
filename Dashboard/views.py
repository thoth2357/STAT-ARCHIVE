from django.shortcuts import render
from django.views import View


class Bibliotheca(View):
    def get(self, request):
        context = {
            'user': request.user,
        }
        return render(request, 'Bibliotheca.html', context=context)
    
    def post(self, request):
        ...

