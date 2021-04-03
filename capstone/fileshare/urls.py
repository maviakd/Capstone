from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import PostListView, PostCreateView, PostUpdateView, PostDeleteView, FileAuth

urlpatterns = [

        path('', views.home, name='fileshare-home'),
        path('dashboard/', views.dashboard, name='fileshare-dashboard'),
	path('file/new/', PostCreateView.as_view(), name='file_new'),
	path('file/<int:pk>/update/', PostUpdateView.as_view(), name='file_update'),
	path('file/<int:pk>/delete/', PostDeleteView.as_view(), name='file_delete'),
	path('file/<int:pk>/auth/', FileAuth.as_view(), name='file_auth'),
]
