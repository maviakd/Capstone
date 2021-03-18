from django.urls import path
from . import views as fileshare_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('files/', fileshare_views.files, name='files'),
]






