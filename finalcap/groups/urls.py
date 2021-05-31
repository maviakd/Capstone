from django.urls import path
from . import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from . import views as group_views
from .views import GroupCreateView, GroupUpdateView, GroupAddUser, GroupRemoveUser, GroupRemoveView
from .views import GroupAddPermission, GroupRemovePermission, GroupView, GroupAddFile, GroupRemoveFile, GroupLeaveView

urlpatterns = [
	path('', GroupView.as_view(), name='group_list'),
	path('create/', GroupCreateView.as_view(), name='group_create'),
	path('leave/<int:pk>/', GroupLeaveView.as_view(), name='group_leave'),
	path('remove/<int:pk>/', GroupRemoveView.as_view(), name='group_remove'),
	path('update/<int:pk>/', GroupUpdateView.as_view(), name = 'group_update'),
	path('update/<int:pk>/file/<int:id>/add/file', GroupAddFile.as_view(), name = 'group_add_file'),
	path('update/<int:pk>/user/<int:id>/add/user', GroupAddUser.as_view(), name = 'group_add_user'),
	path('update/<int:pk>/file/<int:id>/rem/file', GroupRemoveFile.as_view(), name = 'group_remove_file'),
	path('update/<int:pk>/user/<int:id>/rem/user', GroupRemoveUser.as_view(), name = 'group_remove_user'),
	path('update/<int:pk>/user/<int:id>/add/perm', GroupAddPermission.as_view(), name = 'group_add_permission'),
	path('update/<int:pk>/user/<int:id>/rem/perm', GroupRemovePermission.as_view(), name = 'group_remove_permission'),


]
