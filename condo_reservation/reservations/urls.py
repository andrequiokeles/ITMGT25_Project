from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'), 
    path('filter/', views.filter_rooms, name='filter_rooms'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),  # Redirect to home after logout
    path('room/<int:room_id>/', views.room_detail, name='room_detail'),
    path('room/<int:room_id>/reserve/', views.reserve_room, name='reserve_room'),
    # Ensure the function room_availability exists in views.py
    path('rooms/', views.room_availability, name='room_availability'),
]
