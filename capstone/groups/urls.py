from django.urls import path
from . import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from . import views as group_views
from .views import GroupCreateView, GroupUpdateView, GroupAddUser, GroupRemoveUser
from .views import GroupAddPermission, GroupRemovePermission
urlpatterns = [

	path('', group_views.group_list, name='group_list'),
	path('create/', GroupCreateView.as_view(), name='group_create'),
	path('update/<int:pk>/', GroupUpdateView.as_view(), name = 'group_update'),
	path('update/<int:pk>/user/<int:id>/add', GroupAddUser.as_view(), name = 'group_add_user'),
	path('update/<int:pk>/user/<int:id>/remove', GroupRemoveUser.as_view(), name = 'group_remove_user'),
	path('update/<int:pk>/user/<int:id>/add/perm', GroupAddPermission.as_view(), name = 'group_add_permission'),
	path('update/<int:pk>/user/<int:id>/remove/perm', GroupRemovePermission.as_view(), name = 'group_remove_permission'),


]
