from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import Files as F_files
from .models import Files as M_files

# Create your views here.

def files(request):
	if request.method == 'POST':

		f_form = F_files(request.POST,request.FILES)
		m_files = M_files.objects.all()
		if f_form.is_valid():
			f_form.save()
			messages.success(request, f'Your profile has been updated')
	else:
		f_form = F_files(request.POST,request.FILES)
		m_files = M_files.objects.all()

	context = {'f_form':f_form, 'm_files':m_files}
	return render(request, 'fileshare/files.html', context)




























