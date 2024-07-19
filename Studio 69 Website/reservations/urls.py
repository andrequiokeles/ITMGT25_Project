from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('filter/', views.filter_rooms, name='filter_rooms'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),  # Redirect to home after logout
    path('room/<int:room_id>/', views.room_detail, name='room_detail'),
    path('room/<int:room_id>/reserve/', views.reserve_room, name='reserve_room'),
    path('rooms/', views.room_availability, name='room_availability'),
    path('room/<int:room_id>/checkout/', views.checkout, name='checkout'),
    path('room/<int:room_id>/payment/', views.payment, name='payment'),
    path('room/<int:room_id>/upload_proof/', views.upload_proof_of_payment, name='upload_proof_of_payment'),
    path('next-page/', views.proceed_to_next_page, name='proceed_to_next_page'),
    path('building-overview/', views.building_overview, name='building_overview'),
    path('reservation-history/', views.reservation_history, name='reservation_history'),
    path('cancel-reservation/<int:booking_id>/', views.cancel_reservation, name='cancel_reservation'),  
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)