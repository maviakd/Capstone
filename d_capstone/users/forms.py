from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .models import Files

class UserRegisterForm(UserCreationForm):
        email = forms.EmailField()
        class Meta:
                model = User
                fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
        email = forms.EmailField(label="email")
        first_name = forms.CharField(label="firstname")
        last_name = forms.CharField(label="lastname")

        class Meta:
                model = User
                fields = ["username", "email", "first_name", "last_name"]

class ProfileUpdateForm(forms.ModelForm):   # Strictly for updating profile image
	class Meta:
		model = Profile
		fields = ['image']

class Files(forms.ModelForm):
	class Meta:
		model = Files
		fields = "__all__"

