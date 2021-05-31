from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import PostListView, PostCreateView, PostUpdateView, PostDeleteView, FileAuth, VPN, ResetView

urlpatterns = [
	path('VPN', VPN.as_view() , name='VPN'),
        path('blank', views.blank, name='fileshare_blank'),
        #path('dashboard/', views.dashboard, name='fileshare_dashboard'),
	path('', views.dashboard, name='fileshare_dashboard'),
	path('files', PostListView.as_view(), name='files'),
	path('reset', ResetView.as_view(), name='reset'),
	path('file/new/', PostCreateView.as_view(), name='file_new'),
	path('file/<int:pk>/update/', PostUpdateView.as_view(), name='file_update'),
	path('file/<int:pk>/delete/', PostDeleteView.as_view(), name='file_delete'),
	path('file/<int:pk>/auth/', FileAuth.as_view(), name='file_auth'),
]
