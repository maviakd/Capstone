from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	id = models.AutoField(primary_key=True)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')


	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self, *args, **kwargs):
		super().save()

		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)



class Files(models.Model):
	doc = models.FileField(upload_to=f'files/{User}', default="")
	date_posted = models.DateField(default = timezone.now, editable=False)
	visibility = models.BooleanField()
	user = models.ForeignKey(User, on_delete=models.CASCADE, editable = False, null=True)
#	user_id = models.AutoField(User, null = True)

#	def __str__(self):
#		return  self.user.username




























