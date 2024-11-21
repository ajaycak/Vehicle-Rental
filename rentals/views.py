from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db import models
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import Booking, Payment, Vehicle, VehicleRequest, ContactMessage
from .forms import CustomUserRegistrationForm, BookingForm, VehicleRequestForm

# View to display vehicle details and handle bookings

from django.shortcuts import render, get_object_or_404, redirect
from .models import Vehicle, Booking
from .forms import BookingForm
from datetime import timedelta

def vehicle_detail(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    form = BookingForm(request.POST or None)
    error = None

    if request.method == 'POST':
        if form.is_valid():
            booking_date = form.cleaned_data['booking_date']
            return_date = form.cleaned_data['return_date']

            # Check if the vehicle is already booked during the selected dates
            existing_bookings = Booking.objects.filter(vehicle=vehicle)
            for booking in existing_bookings:
                if not (return_date < booking.booking_date or booking_date > booking.return_date):
                    error = "The vehicle is not available during these dates."
                    break

            if not error:
                # Create the booking if available
                Booking.objects.create(
                    vehicle=vehicle,
                    user=request.user,
                    booking_date=booking_date,
                    return_date=return_date
                )
                return redirect('booking_success', booking_id=booking.id)

    # Display the vehicle details and the booking form
    return render(request, 'rentals/vehicle_detail.html', {
        'vehicle': vehicle,
        'form': form,
        'error': error
    })

# Helper function to check vehicle availability
def is_vehicle_available(vehicle, start_date, end_date):
    bookings = Booking.objects.filter(vehicle=vehicle)
    for booking in bookings:
        if (start_date <= booking.return_date and end_date >= booking.booking_date):
            return False
    return True

# Home page showing all vehicles and user bookings
def home(request):
    vehicles = Vehicle.objects.all()
    bookings = Booking.objects.filter(user=request.user) if request.user.is_authenticated else []
    return render(request, 'home.html', {'vehicles': vehicles, 'bookings': bookings})

def about(request):
    return render(request, 'rentals/about.html')


# User registration view
from .forms import CustomUserRegistrationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserRegistrationForm


# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Booking
from django.shortcuts import render, redirect, get_object_or_404
from .models import Booking
from .forms import RatingForm




@login_required
def profile(request):
    bookings = Booking.objects.filter(user=request.user)
    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            booking_id = request.POST.get('booking_id')
            rating = form.cleaned_data['rating']
            booking = Booking.objects.get(id=booking_id)
            booking.rating = rating
            booking.save()
            return redirect('profile')
    else:
        form = RatingForm()
    
    return render(request, 'rentals/profile.html', {'bookings': bookings, 'rating_form': form})


# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.status == 'Pending':  # Allow cancellation only for pending bookings
        booking.status = 'Cancelled'
        booking.save()
    return redirect('profile')  # Redirect back to the profile page




def custom_register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Make sure this is called correctly
            return redirect('login')  # Or whatever page you want to redirect to after successful registration
    else:
        form = CustomUserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})


# User login view
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'rentals/login.html', {'form': form})

# User logout view
def custom_logout(request):
    logout(request)
    return redirect('home')

# Booking detail view
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'booking_detail.html', {'booking': booking})

from django.shortcuts import render, get_object_or_404
from .models import Booking

def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Pass the booking object to the template
    context = {
        'booking': booking,
    }
    
    return render(request, 'rentals/booking_success.html', context)
# Vehicle request view (for adding new vehicle requests)
@login_required
def vehicle_request_view(request):
    if request.method == 'POST':
        form = VehicleRequestForm(request.POST)
        if form.is_valid():
            vehicle_request = form.save(commit=False)
            vehicle_request.user = request.user
            vehicle_request.save()
            return redirect('vehicle_request_success')
    else:
        form = VehicleRequestForm()
    return render(request, 'rentals/vehicle_request_form.html', {'form': form})

# Success page for vehicle request submission
def request_success_view(request):
    return render(request, 'rentals/request_success.html')

# View to list all vehicle requests
def vehicle_request_list_view(request):
    vehicle_requests = VehicleRequest.objects.all()
    return render(request, 'rentals/vehicle_request_list.html', {'vehicle_requests': vehicle_requests})

# View to handle vehicle list, including recommended vehicles
# rentals/views.py
from django.shortcuts import render
from .models import Vehicle, VehicleType

def vehicle_list(request):
    # Get vehicle type filter from query parameters
    vehicle_type_id = request.GET.get('type', None)
    
    # Filter by vehicle type if provided
    if vehicle_type_id:
        filtered_vehicles = Vehicle.objects.filter(vehicle_type_id=vehicle_type_id)
    else:
        filtered_vehicles = Vehicle.objects.all()

    # Identify recommended vehicle
    recommended_vehicle = filtered_vehicles.filter(is_recommended=True).first()

    # Get other vehicles excluding the recommended one
    if recommended_vehicle:
        other_vehicles = filtered_vehicles.exclude(id=recommended_vehicle.id)
    else:
        other_vehicles = filtered_vehicles

    # Fetch all vehicle types for the dropdown
    vehicle_types = VehicleType.objects.all()

    context = {
        'recommended_vehicle': recommended_vehicle,
        'other_vehicles': other_vehicles,
        'vehicle_types': vehicle_types
    }
    return render(request, 'rentals/vehicles_list.html', context)



@login_required
def process_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        # Assuming the payment form has fields for amount, payment_method, etc.
        payment_method = request.POST.get('payment_method', 'Card')  # example default
        payment = Payment.objects.create(
            booking=booking,
            amount=booking.vehicle.price,
            payment_date=date.today(),
            status="Paid",
            payment_method=payment_method,
        )
        booking.status = "Paid"
        booking.save()
        messages.success(request, "Payment successful and booking updated.")
        return redirect('booking_detail', booking_id=booking.id)  # Redirect to a booking detail view
    
    return render(request, 'rentals/payment_form.html', {'booking': booking})

# Handle vehicle request approval
@require_POST
def approve_vehicle_request(request, request_id):
    vehicle_request = get_object_or_404(VehicleRequest, id=request_id)
    Vehicle.objects.create(
        vehicle_type=vehicle_request.vehicle_type,
        model=vehicle_request.model,
        price=vehicle_request.price,
    )
    vehicle_request.status = 'Approved'
    vehicle_request.save()

    messages.success(request, "Vehicle request approved and added to the site.")
    return HttpResponseRedirect(reverse('vehicle_request_list'))

# Handle vehicle request rejection
@require_POST
def reject_vehicle_request(request, request_id):
    vehicle_request = get_object_or_404(VehicleRequest, id=request_id)
    vehicle_request.delete()

    messages.success(request, "Vehicle request rejected and removed.")
    return HttpResponseRedirect(reverse('vehicle_request_list'))

# Contact page to send messages
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        ContactMessage.objects.create(name=name, email=email, message=message)
        messages.success(request, "Your message has been sent!")
        return redirect('contact')
    return render(request, 'rentals/contact.html')


# In your views.py
from django.shortcuts import render, redirect
from .forms import ProfileForm  # Assuming you have a form for updating the profile
from django.contrib.auth.decorators import login_required

@login_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        form = ProfileForm(instance=user)
    
    return render(request, 'rentals/update_profile.html', {'form': form})

from django.utils import timezone
from .models import Booking

def update_booking_status():
    # Get the current date and time
    now = timezone.now()

    # Update bookings where return_date has passed and status is not yet 'Completed'
    bookings_to_update = Booking.objects.filter(return_date__lte=now, status='Approved')

    # Update status to 'Completed'
    for booking in bookings_to_update:
        booking.status = 'Completed'
        booking.save()

# You can call this function after the user completes a booking, or set it to run periodically
from celery import shared_task
from django.utils import timezone
from .models import Booking

@shared_task
def update_booking_status_task():
    now = timezone.now()
    bookings = Booking.objects.filter(return_date__lte=now, status='Approved')
    for booking in bookings:
        booking.status = 'Completed'
        booking.save()


from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from io import BytesIO

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Booking

def download_invoice(request, booking_id):
    # Retrieve the booking based on the booking_id
    booking = get_object_or_404(Booking, id=booking_id)

    # Generate and return the invoice PDF
    return generate_invoice_pdf(booking)


def generate_invoice_pdf(booking):
    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()

    # Create a PDF object
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Add content to the PDF
    c.drawString(100, 750, f"Invoice for Booking ID: {booking.id}")
    c.drawString(100, 730, f"User: {booking.user.username}")
    c.drawString(100, 710, f"Vehicle: {booking.vehicle.model}")
    c.drawString(100, 690, f"Booking Date: {booking.booking_date}")
    c.drawString(100, 670, f"Return Date: {booking.return_date}")
    c.drawString(100, 650, f"Status: {booking.status}")
    
    # If total_amount is not set, calculate it
    total_amount = booking.total_amount if booking.total_amount else booking.calculate_total()
    c.drawString(100, 630, f"Total Amount: Rs. {total_amount}")

    # Save the PDF
    c.showPage()
    c.save()

    # Get the value of the BytesIO buffer and return it as an HttpResponse
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{booking.id}.pdf"'

    return response

