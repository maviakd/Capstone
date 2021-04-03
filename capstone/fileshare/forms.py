from django import forms
from django.contrib.auth.models import User
from .models import Files
import datetime

class FileAuthForm1(forms.Form):
	pin = forms.CharField(label="Pin", max_length = 20)

class FileAuthForm2(forms.Form):
	pass

class FileAuthForm3(forms.Form):
        pin = forms.CharField(label="Pin", max_length = 20)












