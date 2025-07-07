# task_manager/users/statuses.py
from django.urls import path

from . import views

app_name = 'statuses'

urlpatterns = [
    path('', views.StatusListView.as_view(), name='list'),
    path('<int:pk>/update/', views.StatusUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.StatusDeleteView.as_view(), name='delete'),
]
