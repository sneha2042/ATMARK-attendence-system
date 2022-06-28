from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import os

# Create your models here.
class student(models.Model):
    
    def user_directory_path(instance, filename):
        #stringId = name
        path=''

        filename_reformat = filename

        return os.path.join(path, filename_reformat)

    name=models.CharField(max_length=300)
    branch=models.CharField(max_length=100)
    picture=models.ImageField(upload_to=user_directory_path)
    