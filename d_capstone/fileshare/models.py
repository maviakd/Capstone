0from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from os import path

# Create your models here.

class Files(models.Model):
	doc = models.FileField(upload_to=f'files/')
	date_posted = models.DateField(default = timezone.now, editable=False)
	visibility = models.BooleanField()
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, editable = False)



















