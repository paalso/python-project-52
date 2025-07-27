from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from django.views.i18n import set_language

from task_manager import env_debug_view, views

urlpatterns = [
    path('set-language/', set_language, name='set_language'),
    path('__debug__/info/', env_debug_view.get_debug_info, name='debug-env'),
]

urlpatterns += i18n_patterns(
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('users/', include('task_manager.users.urls')),
    path('statuses/', include('task_manager.statuses.urls')),
    path('labels/', include('task_manager.labels.urls')),
    path('tasks/', include('task_manager.tasks.urls')),
    path('admin/', admin.site.urls),
)
