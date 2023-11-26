from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

class CustomUser(AbstractBaseUser):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)  # able to login
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
    
class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    booking_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} booked Room {self.room.room_number} from {self.check_in_date} to {self.check_out_date}"

class Room(models.Model):
    room_img = models.ImageField(upload_to='room_img/', blank=True)
    room_number = models.CharField(max_length=10, unique=True)
    room_name = models.CharField(max_length=10, unique=True)
    details = models.TextField(max_length=500)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='owned_rooms')
    check_in_date = models.DateField(blank=True, null=True)
    check_out_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Room {self.room_number} - {self.room_name}"
    
    def calculate_fee(self):
        if self.check_in_date and self.check_out_date:
            duration = self.check_out_date - self.check_in_date
            total_fee = duration.days * self.price_per_night
            return total_fee
        return None
    def calculate_nights(self):
        if self.check_in_date and self.check_out_date:
            duration = self.check_out_date - self.check_in_date
            return duration.days
        return None

