from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
#, UserUpdateForm, ProfileUpdateForm

# Create your views here.

def login(request):
	return render(request, 'users/login.html')

def logout(request):
	return render(request, 'users/logout.html')

@login_required
def profile(request):

	

	return render(request, 'users/profile.html')

def register(request):
#	form = UserCreationForm()
#	return render(request, 'users/register.html', {'form':form})

	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Your account has been created! You are now able to log in')
			return redirect('webapp-home')
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html', {'form': form})

def forgot_password(request):
	return render(request, 'users/forgot_password.html')

































