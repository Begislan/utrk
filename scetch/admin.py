from django.contrib import admin
from .models import QueueSlot, Booking



class BookingAdmin(admin.ModelAdmin):
    list_display = ["user", "slot", 'created_at']
    list_filter = ["created_at"]


admin.site.register( Booking, BookingAdmin)
admin.site.register(QueueSlot)