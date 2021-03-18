from django.urls import path
from django.contrib.auth import views as auth_views
from . import views as user_views
from django.contrib.auth import login
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
#       path('login/', user_views.login, name='login'),
#	path('logout/', user_views.logout, name='logout'),
	path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name='login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
	path('profile/', user_views.profile, name='users-profile'),
	path('register/', user_views.register, name='users-register'),
        path('forgot_password/', user_views.forgot_password, name='users-forgot_password'),
	path('user_list/', user_views.user_list, name='users-user_list'),
	path('files/', user_views.files, name='users-files'),
	path('file_delete/', user_views.file_delete, name='file_delete'),


]



if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



