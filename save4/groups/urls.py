from django.urls import path
from . import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from . import views as group_views
from .views import GroupCreateView, GroupDetailView, GroupUpdateView


urlpatterns = [

	path('', group_views.group_list, name='group_list'),
	path('create/', GroupCreateView.as_view(), name='group_create'),
	path('detail/<int:pk>/', GroupDetailView.as_view(), name='group_detail'),
	path('update/<int:pk>/', user_views.group_update, name='group_update'),
	#path('update/<int:pk>/', GroupUpdateView.as_view(), name = 'group_update_view')

]


#if settings.DEBUG:
#        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
