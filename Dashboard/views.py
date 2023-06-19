from django.shortcuts import render
from django.views import View


class Bibliotheca(View):
    def get(self, request):
        return render(request, 'Bibliotheca.html')
    
    def post(self, request):
        ...

