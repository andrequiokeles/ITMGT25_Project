from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, Booking
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date
from django.core.files.storage import FileSystemStorage

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
    
    reservation_complete = request.GET.get('reservation_complete', False)

    return render(request, 'reservations/home.html', {
        'rooms': rooms,
        'room_types': room_types,
        'floors': floors_str,
        'min_price': min_price,
        'max_price': max_price,
        'start_date': start_date,
        'end_date': end_date,
        'available_floors': available_floors,
        'reservation_complete': reservation_complete
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
    available_rooms = Room.objects.all()

    room_types = request.GET.getlist('room_types')
    floors = request.GET.get('floors', '').split(',')
    if floors == ['']:
        floors = []

    #min and max price data validation as integer
    try:
        min_price = int(request.GET.get('min_price', 0))
    except ValueError:
        min_price = 0

    try:
        max_price = int(request.GET.get('max_price', 10000))
    except ValueError:
        max_price = 10000

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    #filters
    if room_types:
        available_rooms = available_rooms.filter(type__in=room_types)
    if floors:
        available_rooms = available_rooms.filter(floor__in=floors)
    if min_price:
        available_rooms = available_rooms.filter(price__gte=min_price)
    if max_price:
        available_rooms = available_rooms.filter(price__lte=max_price)
    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            booked_rooms = Booking.objects.filter(
                Q(start_date__lt=end_date) & 
                Q(end_date__gt=start_date)
            ).values_list('room_id', flat=True)

            available_rooms = available_rooms.exclude(id__in=booked_rooms)
        except ValueError:
            #date parsing error
            pass

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
    room = get_object_or_404(Room, pk=room_id)
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Validate input
        try:
            start_date_obj = parse_date(start_date)
            end_date_obj = parse_date(end_date)

            if not start_date_obj or not end_date_obj:
                raise ValidationError('Invalid date format.')

            if start_date_obj >= end_date_obj:
                raise ValidationError('End date must be after the start date.')

            nights = (end_date_obj - start_date_obj).days
            if nights <= 0:
                raise ValidationError('The number of nights must be positive.')

            # Overlapping bookings
            overlapping_bookings = Booking.objects.filter(
                room=room,
                start_date__lt=end_date_obj,
                end_date__gt=start_date_obj,
                is_canceled=False
            )

            if overlapping_bookings.exists():
                raise ValidationError('This room is already booked for the selected dates.')

            # Total price calculator
            total_price = room.price * nights

            # Create a booking
            booking = Booking(
                user=request.user,
                room=room,
                start_date=start_date_obj,
                end_date=end_date_obj,
                total_price=total_price,
                is_canceled=False  # Default
            )
            booking.save()

            # Mark room as booked
            room.is_booked = True
            room.save()

            return render(request, 'reservations/checkout.html', {
                'room': room,
                'start_date': start_date_obj,
                'end_date': end_date_obj,
                'total_price': total_price,
                'nights': nights,  # Include nights in the context
            })

        except ValidationError as e:
            return render(request, 'reservations/room_detail.html', {
                'room': room,
                'error': str(e),
            })
    return redirect('room_detail', room_id=room_id)
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

def checkout(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    total_price = 0
    nights = 0

    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        nights = (end_date - start_date).days
        total_price = room.price * nights if nights > 0 else 0

    return render(request, 'reservations/checkout.html', {
        'room': room,
        'start_date': start_date,
        'end_date': end_date,
        'total_price': total_price,
        'nights': nights,  #nights passed to template
    })

def proceed_to_next_page(request):
    return render(request, 'next_page.html')

def payment(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    total_price = 0
    nights = 0

    #used to see start and end dates retrieved
    print(f"Retrieved start_date: {start_date}")
    print(f"Retrieved end_date: {end_date}")

    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            if start_date < end_date:
                nights = (end_date - start_date).days
                total_price = room.price * nights if nights > 0 else 0
                print(f"Start Date: {start_date}, End Date: {end_date}, Nights: {nights}, Total Price: {total_price}")
            else:
                print("End date is before start date.")
                total_price = 0
                nights = 0
        except ValueError:
            print("Date conversion failed.")
            total_price = 0
            nights = 0

    return render(request, 'reservations/payment.html', {
        'room': room,
        'start_date': start_date,
        'end_date': end_date,
        'total_price': total_price,
        'nights': nights,
    })

def upload_proof_of_payment(request, room_id):
    if request.method == 'POST':
        proof_of_payment = request.FILES.get('proof_of_payment')

        if not proof_of_payment:
            return JsonResponse({'error': 'No file uploaded'}, status=400)
        
        booking = get_object_or_404(Booking, room_id=room_id)

        # Update and upload proof of payment
        booking.proof_of_payment = proof_of_payment
        booking.save()
        
        return JsonResponse({'message': 'Proof of payment uploaded successfully'}, status=200)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def building_overview(request):
    selected_date = request.GET.get('selected_date')
    if selected_date:
        try:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        except ValueError:
            selected_date = None
    else:
        selected_date = datetime.today().date()

    rooms = Room.objects.all()
    room_status = []

    for room in rooms:
        bookings = Booking.objects.filter(room=room, start_date__lte=selected_date, end_date__gte=selected_date)
        if bookings.exists():
            room_status.append({'room': room, 'status': 'booked'})
        else:
            room_status.append({'room': room, 'status': 'available'})

    return render(request, 'reservations/building_outline.html', {
        'room_status': room_status,
        'selected_date': selected_date,
    })

@login_required
def reservation_history(request):
    #getting current logged-in user
    user = request.user

    #all of user's bookings
    bookings = Booking.objects.filter(user=user).select_related('room')

    reservation_data = []
    for booking in bookings:
        room = booking.room
        nights = (booking.end_date - booking.start_date).days
        reservation_data.append({
            'id': booking.id,
            'room_number': room.unit,
            'room_type': room.type,
            'room_floor': room.floor,
            'price': room.price,
            'nights': nights,
            'start_date': booking.start_date,
            'end_date': booking.end_date,
        })

    return render(request, 'reservations/reservation_history.html', {
        'reservations': reservation_data
    })



