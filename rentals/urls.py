# rentals/urls.py
from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('booking_success/<int:booking_id>/', views.booking_success, name='booking_success'),
    path('download_invoice/<int:booking_id>/', views.download_invoice, name='download_invoice'),



]

urlpatterns += [
    path('profile/', views.profile, name='profile'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('profile/update/', views.update_profile, name='update_profile'),



    path('register/', views.custom_register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('home/', views.home, name='home'),  # Ensure there's a home view
    path('about/', views.about, name='about'),  # Add about page
    path('contact/', views.contact, name='contact'),

    # Vehicle-related URLs
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/<int:vehicle_id>/', views.vehicle_detail, name='vehicle_detail'),

    # Booking-related URLs
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('booking/<int:booking_id>/payment/', views.process_payment, name='process_payment'),
    path('booking_success/', views.booking_success, name='booking_success'),

    # Vehicle Request-related URLs
    path('request-vehicle/', views.vehicle_request_view, name='vehicle_request'),
    path('request-success/', views.request_success_view, name='vehicle_request_success'),
    path('vehicle-request-list/', views.vehicle_request_list_view, name='vehicle_request_list'),
    path('approve_request/<int:request_id>/', views.approve_vehicle_request, name='approve_vehicle_request'),
    path('reject_request/<int:request_id>/', views.reject_vehicle_request, name='reject_vehicle_request'),
]

urlpatterns += [
    # Other paths
    path('register/', views.custom_register, name='register'),
]


# urls.py
from django.contrib.auth import views as auth_views

urlpatterns += [
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
