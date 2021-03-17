from django import forms
from django.contrib.auth.models import User
from .models import Files

class Files(forms.ModelForm):
	class Meta:
		model = Files
		fields = "__all__"










