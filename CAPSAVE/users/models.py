from django.db import models
from django.contrib.auth.models import User
from PIL import Image

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




#print(f'---------------------------------------------------{str(User)}')

'''
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        User.email = models.EmailField(default = f"{User.email}")
        username = models.CharField(default = f"{User.usernname}", max_length=10)
        id = models.AutoField(primary_key=True)
        first_name = models.CharField(default = f"{User.first_name}", max_length=10)
        last_name = models.CharField(default = f"{User.last_name}", max_length=10)
        image = models.ImageField(default='default.jpg', upload_to=f"{User.username}")
'''




























