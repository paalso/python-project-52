from django.contrib import admin
from django.urls import include, path

from task_manager import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', include('task_manager.users.urls')),
    path('admin/', admin.site.urls),
]
