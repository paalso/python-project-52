from django.contrib import admin
from django.urls import include, path

from task_manager import env_debug_view, views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('users/', include('task_manager.users.urls')),
    path('statuses/', include('task_manager.statuses.urls')),
    path('labels/', include('task_manager.labels.urls')),
    path('tasks/', include('task_manager.tasks.urls')),
    path('admin/', admin.site.urls),
    path('env/', env_debug_view.EnvDebugView.as_view(), name='debug-env'),
]
