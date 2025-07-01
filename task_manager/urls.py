from django.contrib import admin
from django.urls import include, path

from task_manager import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('users/', include('task_manager.users.urls')),
    path('admin/', admin.site.urls),
]
