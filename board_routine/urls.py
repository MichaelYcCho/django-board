from django.urls import path
from . import views

app_name = 'board_routine'

urlpatterns = [
    path('', views.routine_list, name='list'),
    path('<int:pk>/', views.routine_detail, name='detail'),
    path('create/', views.routine_create, name='create'),
    path('<int:pk>/update/', views.routine_update, name='update'),
    path('<int:pk>/delete/', views.routine_delete, name='delete'),
]
