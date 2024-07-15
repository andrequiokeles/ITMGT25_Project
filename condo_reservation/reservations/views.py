from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, Booking
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from datetime import datetime

def home(request):
    rooms = Room.objects.filter(is_booked=False) 
    return render(request, 'reservations/home.html', {'rooms': rooms})

def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'reservations/room_detail.html', {'room': room})

def filter_rooms(request):
    room_types = request.GET.getlist('room_types')
    floors = request.GET.get('floors', '').split(',')
    min_price = request.GET.get('min_price', 0)
    max_price = request.GET.get('max_price', 10000)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    rooms = Room.objects.all()

    if room_types:
        rooms = rooms.filter(type__in=room_types)
    if floors and floors != ['']:
        rooms = rooms.filter(floor__in=floors)
    if min_price:
        rooms = rooms.filter(price__gte=min_price)
    if max_price:
        rooms = rooms.filter(price__lte=max_price)
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        available_rooms = [room for room in rooms if room.is_available(start_date, end_date)]
        rooms = Room.objects.filter(id__in=[room.id for room in available_rooms])

    return render(request, 'reservations/home.html', {'rooms': rooms})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'reservations/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') 
    return render(request, 'reservations/login.html')

def room_availability(request):
    rooms = Room.objects.all()
    return render(request, 'reservations/room_availability.html', {'rooms': rooms})
