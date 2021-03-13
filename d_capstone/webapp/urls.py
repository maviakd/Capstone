from django.urls import path
from . import views

urlpatterns = [

	path('', views.home, name='webapp-home'),
	path('dashboard/', views.dashboard, name='webapp-dashboard'),
]

