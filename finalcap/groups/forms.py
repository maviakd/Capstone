from django import forms
from django.contrib.auth.models import User, Group, ContentType
from .models import MyGroup

class GroupUserAdd(forms.ModelForm):
	adduser = forms.BooleanField()
	class Meta:
		model = MyGroup
		fields = ['adduser']
