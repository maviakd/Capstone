from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from .models import Files

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

'''
def create_files(post_save, sender=User):
	if created:
		Files.objects.create(user=instance)
'''


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
	instance.profile.save()


#@receiver(post_save, sender=User)
#def save_files(sender, instance, **kwargs):
#	instance.files.save()










