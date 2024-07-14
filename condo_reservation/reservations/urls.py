from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('filter/', views.filter_rooms, name='filter_rooms'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('room/<int:room_id>/', views.room_detail, name='room_detail'), 
    path('rooms/', views.room_availability, name='room_availability'),  
]
