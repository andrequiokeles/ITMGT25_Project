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
    if request.method == 'GET':
        room_type = request.GET.get('type', '')
        floor = request.GET.get('floor', '')
        min_price = request.GET.get('min_price', 0)
        max_price = request.GET.get('max_price', 1000000)

        filters = Q(is_booked=False)

        if room_type:
            filters &= Q(type=room_type)
        if floor:
            filters &= Q(floor=floor)
        filters &= Q(price__gte=min_price, price__lte=max_price)

        rooms = Room.objects.filter(filters).distinct()
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
