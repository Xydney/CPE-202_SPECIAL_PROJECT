from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('nav/', base, name='base'),
    path('', HomePage, name='HomePage'),

    #AUTHENTICATION
    path('register/', RegisterPage, name='RegisterPage'),
    path('login/', LoginPage, name='LoginPage'),
    path('logout/', logout, name='logout'),

    #ADMIN URLS
    path('bookings/', Bookings, name='Bookings'),
    path('approve_booking/<int:booking_id>/', approve_booking, name='approve_booking'),
    path('decline_booking/<int:booking_id>/', decline_booking, name='decline_booking'),
    path('activebookings/', Active_Bookings, name='Active_Bookings'),
    path('approve_payment/<int:room_id>/', approve_payment, name='approve_payment'),
    path('rooms/', Rooms, name='Rooms'),
    path('createroom/', create_room, name='create_room'),
    path('deleteroom/<int:room_id>/', delete_room, name='delete_room'),
    path('editroom/<int:room_id>/', edit_room, name='edit_room'),
    path('users/', UserList, name='UserList'),
    path('deleteuser/<int:user_id>/', delete_user, name='delete_user'),
    path('edituser/<int:pk>/', edit_user, name='edit_user'),
    path('available-rooms/', available_rooms, name='available_rooms'),
    path('room/<int:room_id>/', room_detail, name='room_detail'),
    path('book-room/<int:room_id>/', book_room, name='book_room'),
    path('user-profile/', user_profile, name='user_profile'),
    path('edit_user_details/<int:pk>/', edit_user_details, name='edit_user_details'),
    path('cancel_booking/<int:booking_id>/', cancel_booking, name='cancel_booking'),

]