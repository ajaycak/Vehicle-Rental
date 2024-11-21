# vehicle_rental/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  # Use default User model
from .models import VehicleRequest, Booking
from django.core.exceptions import ValidationError
import re
from django import forms
from django.contrib.auth.models import User

class CustomUserRegistrationForm(forms.ModelForm):

    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.set_password(self.cleaned_data['password1'])
            user.save()
        return user

# rentals/forms.py

from django import forms
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']  # Add other fields as needed

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # Customize form if needed (e.g., add placeholders, set initial values)

from django import forms
from .models import Booking


class RatingForm(forms.Form):
    rating = forms.IntegerField(
        min_value=1, 
        max_value=5,
        widget=forms.NumberInput(attrs={'class': 'star-rating'}),  # You can customize this or use a third-party widget for stars
        label="Rate your booking"
    )


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_date', 'return_date']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
        }


class VehicleRequestForm(forms.ModelForm):
    class Meta:
        model = VehicleRequest
        fields = ['vehicle_type', 'model', 'price', 'owner_contact']
