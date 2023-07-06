from django.db import models
from django.core.validators import RegexValidator


validate_year_format = RegexValidator(
    regex=r'^\d{4}/\d{4}$',
    message='Enter the year in the format YYYY/YYYY.',
)

# Create your models here.
class PastQuestion(models.Model):
    Type_choices = [
        ('Exam Question', 'Exam Question'),
        ('Test Question', 'Test Question')
    ]
    Session = models.CharField(max_length=100, validators=[validate_year_format])
    Type = models.CharField(max_length=50,choices=Type_choices,)
    Lecturer_name = models.CharField(max_length=100)
    Course_name = models.CharField(max_length=100)
    Course_code = models.CharField(max_length=100,)
    Course_file = models.FileField(upload_to='resources/past-question/')
    Course_image = models.ImageField(upload_to='resources/images', null=True)
    
    def __str__(self):
        return self.Course_name+' '+self.Course_code
    
    @property
    def start_year(self):
        return self.Session.split('/')[0]
    
    @property
    def end_year(self):
        return self.Session.split('/')[1]

class TextBook(models.Model):
    Name = models.CharField(max_length=100)
    Author  = models.CharField(max_length=100)
    TextBook_file = models.FileField(upload_to='media/resources/text-book/')
    
    def __str__(self):
        return self.Name

class Project(models.Model):
    Session = models.CharField(max_length=100, validators=[validate_year_format])
    Topic = models.CharField(max_length=100)
    Author  = models.CharField(max_length=100)
    Supervisor = models.CharField(max_length=100)
    Project_file = models.FileField(upload_to='media/resources/project/')
    
    def __str__(self):
        return self.Topic

