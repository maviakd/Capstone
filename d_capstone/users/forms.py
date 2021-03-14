from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile



class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField(label="email")
#	usrname = forms.CharField(label="username")

	class Meta:
		model = User
		fields = ["username", "email"]
'''
	widgets = {
	"username":forms.TextInput(attrs={'class':'form-group'}),
	"email":forms.EmailInput(attrs={'class':'form-control'})
	}
'''


class ProfileUpdateForm(forms.ModelForm):   # Strictly for updating profile image
	class Meta:
		model = Profile
		fields = ['image']


