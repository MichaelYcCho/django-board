from django.urls import path
from . import views

app_name = 'board_photo'

urlpatterns = [
    path('', views.photo_list, name='list'),
    path('<int:pk>/', views.photo_detail, name='detail'),
    path('create/', views.photo_create, name='create'),
    path('<int:pk>/update/', views.photo_update, name='update'),
    path('<int:pk>/delete/', views.photo_delete, name='delete'),
]
