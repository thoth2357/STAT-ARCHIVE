from django.db import models

# Create your models here.
class Log(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    GeneratedBy = models.CharField(max_length=100)
    ExceptionMessage = models.TextField()
    
    def __str__(self) -> str:
        return f"{self.timestamp} - {self.GeneratedBy}"
    
    