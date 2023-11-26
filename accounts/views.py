from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import auth
from django.http import HttpResponse
from django.contrib import messages
from .forms import *

@login_required(login_url='LoginPage')
def HomePage(request):
    return render(request, 'home.html')
@login_required(login_url='LoginPage')
def base(request):
    return render(request, 'base.html')

def is_admin(user):
    return user.is_authenticated and user.is_admin

def LoginPage(request):
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            return redirect('HomePage')
    context = {
        "form": form
    }
    return render(request, 'login.html', context)

def RegisterPage(request):
    form = RegisterForm(request.POST or None)

    if request.POST and form.is_valid():
        # Check if the username is already in use
        username = form.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            form.add_error('username', 'This username is already taken. Please choose a different one.')
        else:
            user = form.save()
            if user:
                # Log in the user
                login(request, user)
                return redirect('HomePage')

    context = {
        'form': form,
    }

    return render(request, "register.html", context)

@login_required(login_url='LoginPage')
def logout(request):
    auth.logout(request)
    return redirect('LoginPage')
@login_required(login_url='LoginPage')
@user_passes_test(is_admin, login_url='HomePage')
def Bookings(request):

    bookings = Booking.objects.all()

    context = {
        'bookings': bookings,
    }

    return render(request, 'admin/bookings.html', context)

@login_required(login_url='LoginPage')
@user_passes_test(is_admin, login_url='HomePage')
def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if not booking.room.is_available:
        return render(request, 'admin/error_page.html', {'error_message': 'Room is not available for booking.'})

    # Copy check-in and check-out dates from Booking to Room
    booking.room.is_available = False
    booking.room.owner = booking.user
    booking.room.check_in_date = booking.check_in_date
    booking.room.check_out_date = booking.check_out_date
    booking.room.save()

    booking.delete()
    return redirect('Bookings')

@login_required(login_url='LoginPage')
@user_passes_test(is_admin, login_url='HomePage')
def decline_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()
    return redirect('Bookings')

@login_required(login_url='LoginPage')
@user_passes_test(is_admin, login_url='HomePage')
def Active_Bookings(request):
    # Filter rooms with is_available set to False
    rooms = Room.objects.filter(is_available=False)

    context = {
        'rooms': rooms,
    }

    return render(request, 'admin/active_bookings.html', context)

@login_required(login_url='LoginPage')
@user_passes_test(is_admin, login_url='HomePage')
def approve_payment(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    # Update room details
    room.is_available = True
    room.owner = None
    room.save()

    return redirect('Active_Bookings')

@login_required(login_url='LoginPage')
@user_passes_test(is_admin, login_url='HomePage')
def Rooms(request):
    rooms = Room.objects.all()

    context = {
        'rooms': rooms,
    }

    return render(request, 'admin/rooms.html', context)
@login_required(login_url='LoginPage')
@user_passes_test(is_admin, login_url='HomePage')
def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Rooms')
    else:
        form = RoomForm()

    return render(request, 'admin/create_room.html', {'form': form})

@login_required(login_url='LoginPage')
@user_passes_test(is_admin, login_url='HomePage')
def edit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            return redirect('Rooms')  
    else:
        # Pass the initial values to the form
        form = RoomForm(initial={
            'room_number': room.room_number,
            'room_name': room.room_name,
            'details': room.details,
            'price_per_night': room.price_per_night,
            'is_available': room.is_available,
            'owner': room.owner,
        })

    return render(request, 'admin/edit_room.html', {'form': form})

@login_required(login_url='LoginPage')
@user_passes_test(is_admin, login_url='HomePage')
def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    room.delete()
    return redirect('Rooms')
    
@login_required(login_url='LoginPage')
@user_passes_test(is_admin, login_url='HomePage')
def UserList(request):
    users = CustomUser.objects.all()
    context = {
        'users': users
    }
    return render(request, 'admin/users.html', context)

@login_required(login_url='LoginPage')
@user_passes_test(is_admin, login_url='HomePage')
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('Rooms')  
    else:
        # Pass the initial values to the form
        form = UserProfileForm(instance=user)

    context = {
        'form': form,
        'user': user,
    }


    return render(request, 'admin/edit_user.html', context)

@login_required(login_url='LoginPage')
@user_passes_test(is_admin, login_url='HomePage')
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('UserList')

@login_required(login_url='LoginPage')
def available_rooms(request):
    available_rooms = Room.objects.filter(is_available=True)
    context = {
        'available_rooms': available_rooms
    }
    return render(request, 'available_rooms.html', context)

@login_required(login_url='LoginPage')
def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    form = BookingForm()

    context = {
        'room': room,
        'form': form,
    }
    return render(request, 'room_detail.html', context)

@login_required(login_url='LoginPage')
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            check_in_date = form.cleaned_data['check_in_date']
            check_out_date = form.cleaned_data['check_out_date']

            # Calculate price based on check-in and check-out dates
            # (You'll need to implement your own price calculation logic here)

            # Create a booking for the authenticated user and the selected room
            booking = Booking.objects.create(
                user=request.user,
                room=room,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
            )
            # Additional logic for booking confirmation or redirection
            return redirect('available_rooms')  # Change as per your requirement
    else:
        return HttpResponse("Invalid request method.")
    
@login_required(login_url='LoginPage')
def user_profile(request):
    pending_bookings = Booking.objects.filter(user=request.user)
    user_bookings = Room.objects.filter(owner=request.user)
    context = {
        'user_bookings': user_bookings,
        'pending_bookings':pending_bookings
    }
    return render(request, 'user_profile.html', context)

# Add/Edit User Details View
@login_required(login_url='LoginPage')
def edit_user_details(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')  # Redirect to the user profile page after saving the details
    else:
        form = UserProfileForm(instance=user)

    context = {
        'form': form,
        'user': user,
    }

    return render(request, 'edit_user_details.html', context)

@login_required(login_url='LoginPage')
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        # Delete the booking
        booking.delete()
        messages.success(request, 'Booking canceled successfully.')
        return redirect('user_profile')

    context = {'booking': booking}
    return render(request, 'cancel_booking.html', context)
