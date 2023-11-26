from django.db import models

# Create your models here.

class JD(models.Model):
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    
