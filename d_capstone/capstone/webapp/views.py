from django.shortcuts import render

# Create your views here.


def home(request):
	return render(request, 'webapp/base.html')

def dashboard(request):
	return render(request, 'webapp/dashboard.html')










