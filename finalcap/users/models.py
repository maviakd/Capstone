from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os, hashlib, random, string

# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default = "default.jpg")
	phone = models.CharField(max_length = 10, null = True)

	total_owned_files = models.IntegerField(default=0)
	total_given_files = models.IntegerField(default=0)
	total_uploaded_files = models.IntegerField(default=0)
	total_download_files = models.IntegerField(default=0)
	total_groups = models.IntegerField(default=0)
	space = models.IntegerField(default=0)

	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self, *args, **kwargs):
		super().save()

		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)

class IVK(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	iv = models.TextField(default = os.urandom(32), editable = True)
	def __str__(self):
		return f"{self.user.username}'s IV"
