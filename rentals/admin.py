from django.contrib import admin
from .models import Vehicle, Booking, VehicleType, UserProfile, Payment, VehicleRequest

# Customizing the admin interface for VehicleType model
@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Customizing the admin interface for Vehicle model
@admin.register(Vehicle)  # Use the decorator OR the register line, not both
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('vehicle_type', 'model', 'brand', 'price', 'availability', 'rating')
    list_filter = ('vehicle_type', 'brand', 'availability')
    search_fields = ('model', 'brand')

# Customizing the admin interface for UserProfile model
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username',)

# Customizing the admin interface for Booking model
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'vehicle', 'booking_date', 'return_date', 'status', 'rating')  # Add 'user' here
    list_editable = ('status',)  # Allows editing directly in the admin list view


    def user(self, obj):  # This method returns the user associated with the booking
        return obj.user.username  # or obj.user.get_full_name(), depending on what you want to show
    user.admin_order_field = 'user'  # This will allow you to order by the user field in the admin
    user.short_description = 'User'  # This will be the column header in the admin

# Customizing the admin interface for Payment model
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'payment_date', 'status', 'payment_method')
    search_fields = ('booking__user__username',)
    list_filter = ('status', 'payment_date')

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser  # Only superusers can change payments

# Customizing the admin interface for VehicleRequest model
@admin.register(VehicleRequest)
class VehicleRequestAdmin(admin.ModelAdmin):
    list_display = ('vehicle_type', 'model', 'price', 'owner_contact', 'status', 'user', 'submitted_at')
    list_filter = ('status',)
    actions = ['approve_vehicle_request']

    def approve_vehicle_request(self, request, queryset):
        for vehicle_request in queryset.filter(status='Pending'):
            # Approve the request and add it as a new Vehicle
            new_vehicle = Vehicle.objects.create(
                vehicle_type=vehicle_request.vehicle_type,
                model=vehicle_request.model,
                price=vehicle_request.price,
                availability=True  # New vehicles are available by default
            )
            # Update the VehicleRequest status to 'Approved'
            vehicle_request.status = 'Approved'
            vehicle_request.save()
            
            self.message_user(request, f"Vehicle request for {new_vehicle.model} has been approved and added.")

    approve_vehicle_request.short_description = "Approve selected requests and add to Vehicles"
