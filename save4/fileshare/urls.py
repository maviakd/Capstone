from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import PostListView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [

        path('', views.home, name='fileshare-home'),
        path('dashboard/', views.dashboard, name='fileshare-dashboard'),
	path('file/', PostCreateView.as_view(), name='file_new'),
	path('file/<int:pk>/update/', PostUpdateView.as_view(), name='file_update'),
	path('file/<int:pk>/delete/', PostDeleteView.as_view(), name='file_delete'),
	
]


#if settings.DEBUG:
#        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
