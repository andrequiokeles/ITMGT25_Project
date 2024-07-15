from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, Booking
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.decorators import login_required

def home(request):
    rooms = Room.objects.filter(is_booked=False)

    room_types = request.GET.getlist('room_types')
    floors = request.GET.get('floors', '').split(',')
    if floors == ['']:
        floors = []
        
    min_price = int(request.GET.get('min_price', 0))
    max_price = int(request.GET.get('max_price', 10000))
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if room_types:
        rooms = rooms.filter(type__in=room_types)
    if floors:
        floors = list(map(int, floors))
        rooms = rooms.filter(floor__in=floors)

    floors_str = list(map(str, floors))

    if min_price:
        rooms = rooms.filter(price__gte=min_price)
    if max_price:
        rooms = rooms.filter(price__lte=max_price)
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        available_rooms = [room for room in rooms if room.is_available(start_date, end_date)]
        rooms = Room.objects.filter(id__in=[room.id for room in available_rooms])

    available_floors = [1, 2, 3, 4, 5]

    return render(request, 'reservations/home.html', {
        'rooms': rooms,
        'room_types': room_types,
        'floors': floors_str,
        'min_price': min_price,
        'max_price': max_price,
        'start_date': start_date,
        'end_date': end_date,
        'available_floors': available_floors
    })

def filter_rooms(request):
    rooms = Room.objects.filter(is_booked=False)

    room_types = request.GET.getlist('room_types')
    floors = request.GET.get('floors', '').split(',')
    if floors == ['']:
        floors = []
        
    min_price = int(request.GET.get('min_price', 0))
    max_price = int(request.GET.get('max_price', 10000))
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if room_types:
        rooms = rooms.filter(type__in=room_types)
    if floors:
        floors = list(map(int, floors))
        rooms = rooms.filter(floor__in=floors)

    floors_str = list(map(str, floors))

    if min_price:
        rooms = rooms.filter(price__gte=min_price)
    if max_price:
        rooms = rooms.filter(price__lte=max_price)
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        available_rooms = [room for room in rooms if room.is_available(start_date, end_date)]
        rooms = Room.objects.filter(id__in=[room.id for room in available_rooms])

    available_floors = [1, 2, 3, 4, 5]

    return render(request, 'reservations/home.html', {
        'rooms': rooms,
        'room_types': room_types,
        'floors': floors_str,
        'min_price': min_price,
        'max_price': max_price,
        'start_date': start_date,
        'end_date': end_date,
        'available_floors': available_floors
    })

def room_availability(request):
    available_rooms = Room.objects.filter(is_booked=False)

    room_types = request.GET.getlist('room_types')
    floors = request.GET.get('floors', '').split(',')
    if floors == ['']:
        floors = []

    min_price = int(request.GET.get('min_price', 0))
    max_price = int(request.GET.get('max_price', 10000))
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if room_types:
        available_rooms = available_rooms.filter(type__in=room_types)
    if floors:
        available_rooms = available_rooms.filter(floor__in=floors)

    if min_price:
        available_rooms = available_rooms.filter(price__gte=min_price)
    if max_price:
        available_rooms = available_rooms.filter(price__lte=max_price)

    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        booked_rooms = Booking.objects.filter(
            Q(start_date__lt=end_date) & 
            Q(end_date__gt=start_date)
        ).values_list('room_id', flat=True)

        available_rooms = available_rooms.exclude(id__in=booked_rooms)

    available_floors = [1, 2, 3, 4, 5]

    return render(request, 'reservations/room_availability.html', {
        'rooms': available_rooms,
        'room_types': room_types,
        'floors': floors,
        'min_price': min_price,
        'max_price': max_price,
        'start_date': start_date,
        'end_date': end_date,
        'available_floors': available_floors
    })

def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    total_price = 0

    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        nights = (end_date - start_date).days
        total_price = room.price * nights if nights > 0 else 0

    return render(request, 'reservations/room_detail.html', {
        'room': room,
        'total_price': total_price,
        'start_date': start_date,
        'end_date': end_date,
    })

@login_required
def reserve_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        if start_date < end_date:
            try:
                booking = Booking.objects.create(
                    room=room,
                    user=request.user,
                    start_date=start_date,
                    end_date=end_date
                )
                return redirect('room_detail', room_id=room.id)
            except ValueError as e:
                return render(request, 'reservations/room_detail.html', {
                    'room': room,
                    'error': str(e),
                })
        else:
            return render(request, 'reservations/room_detail.html', {
                'room': room,
                'error': 'End date must be after the start date.',
            })
    return render(request, 'reservations/room_detail.html', {'room': room})

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

def user_logout(request):
    logout(request)
    return redirect('home')
