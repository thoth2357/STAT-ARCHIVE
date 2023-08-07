from django.db import models
from django.core.validators import RegexValidator


validate_year_format = RegexValidator(
    regex=r'^\d{4}/\d{4}$',
    message='Enter the year in the format YYYY/YYYY.',
)

# Create your models here.
class Sessions(models.Model):
    Session = models.CharField(max_length=100, validators=[validate_year_format])
    def __str__(self):
        return self.Session


class PastQuestion(models.Model):
    Type_choices = [
        ('Exam_Questions', 'Exam Questions'),
        ('Text_Questions', 'Text Questions')
    ]
    Session = models.ForeignKey(Sessions, on_delete=models.CASCADE)
    Type = models.CharField(max_length=50,choices=Type_choices,)
    Lecturer_name = models.CharField(max_length=100)
    Name = models.CharField(max_length=100)
    Course_code = models.CharField(max_length=100,)
    file = models.FileField(upload_to='resources/past-question/', null=False)
    thumbnail = models.ImageField(upload_to='resources/images/pastquestion', null=True)
    Date_uploaded = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.Name+' '+self.Course_code
    
    @property
    def start_year(self):
        return self.Session.split('/')[0]
    
    @property
    def end_year(self):
        return self.Session.split('/')[1]

class TextBook(models.Model):
    Name = models.CharField(max_length=100)
    Type = models.CharField(max_length=12, default='Textbooks', editable=False)
    Author  = models.CharField(max_length=100)
    file = models.FileField(upload_to='resources/text-book/', null=False)
    thumbnail = models.ImageField(upload_to='resources/images/textbook', null=True)
    Date_uploaded = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.Name

class Project(models.Model):
    Session = models.ForeignKey(Sessions, on_delete=models.CASCADE)
    Name = models.CharField(max_length=100)
    Type = models.CharField(max_length=12, default='Project', editable=False)
    Author  = models.CharField(max_length=100)
    Supervisor = models.CharField(max_length=100)
    file = models.FileField(upload_to='resources/project/', null=False)
    thumbnail = models.ImageField(upload_to='resources/images/project', null=True)
    Date_uploaded = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.Name


class Report(models.Model):
    Resource_name = models.CharField(max_length=50,)
    Category = models.CharField(max_length=50)
    Message = models.TextField()
    
    def __str__(self) -> str:
        return f"{self.Resource_name}- {self.Category}"
    
    
    