from django.contrib import admin
from .models import PastQuestion, TextBook, Project, Sessions
# Register your models here.
admin.site.register(PastQuestion)
admin.site.register(TextBook)
admin.site.register(Project)
admin.site.register(Sessions)

