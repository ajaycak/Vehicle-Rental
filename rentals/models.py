from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User  # For extending the User model
from django.test import TestCase
from datetime import date

# 1. Vehicle Type Model
class VehicleType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    


# 2. Vehicle Model
# rentals/models.py

from django.db import models

class Vehicle(models.Model):
    vehicle_type = models.ForeignKey('VehicleType', on_delete=models.CASCADE)
    model = models.CharField(max_length=100)
    brand = models.CharField(max_length=100, blank=True)
    availability = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    rating = models.IntegerField(default=0, blank=True, null=True)  # Rating out of 5
    image = models.ImageField(upload_to='vehicle_images/', blank=True, null=True)
    is_recommended = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.vehicle_type.name} - {self.model}"




# 3. User Profile Model (extending the Django User model)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username

# 4. Booking Model
from django.db import models
from django.contrib.auth.models import User
from rentals.models import Vehicle

# rentals/models.py

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    booking_date = models.DateField()
    return_date = models.DateField()
    status = models.CharField(max_length=50)
    rating = models.IntegerField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # optional field for storing the total amount

    def __str__(self):
        return f"Booking for {self.user} - {self.vehicle.model}"

    def calculate_total(self):
        # Calculate the total amount based on the vehicle price and rental duration
        rental_days = (self.return_date - self.booking_date).days
        # Use the vehicle's price field for the calculation
        total = rental_days * self.vehicle.price
        return total



# If you haven't already, run migrations to apply this change:
# python manage.py makemigrations
# python manage.py migrate


# 5. Payment Model
class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    status = models.CharField(max_length=20, default="Pending")
    payment_method = models.CharField(max_length=20, blank=True)  # E.g., Credit Card, Cash
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.booking.user.username} - {self.amount}"
    

# models.py
from django.db import models
from django.contrib.auth.models import User

class VehicleRequest(models.Model):
    vehicle_type = models.CharField(max_length=50)
    model = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    owner_contact = models.CharField(max_length=100)
    status = models.CharField(
        max_length=10,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved')],
        default='Pending'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming the requestor is a registered user
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.model} - {self.status}"



class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"




