from django.db import models
from django.contrib.auth.models import User, Group, ContentType

# Create your models here.

class MyGroup(Group, models.Model):
	creator = models.ForeignKey(User, on_delete = models.CASCADE, default = User, editable = False)


#class MyGroupFiles(Files, models.Model):
#	belongs = models.ManyToManyField(MyGroup)

#	def __str__(self):
#		return self.belongs






