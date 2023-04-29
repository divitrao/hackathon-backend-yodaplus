import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class CredentialDetail(models.Model):
    credential = models.CharField(max_length=100)
    password = models.CharField(max_length=1000)
    website = models.URLField(max_length=1000)
    user = models.ForeignKey(User,on_delete=models.PROTECT)