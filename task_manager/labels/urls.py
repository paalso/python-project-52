from django.urls import path

from . import views

app_name = 'labels'

urlpatterns = [
    path('', views.LabelListView.as_view(), name='list'),
    path('create/', views.LabelCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.LabelUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.LabelDeleteView.as_view(), name='delete'),
]
