from django.contrib import admin
from .models import Reservation, ReservationSettings, Information

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('reservation_date_admin', 'start_time_admin', 'end_time_admin', 'duration_minutes_admin', 'total_price_admin', 'client_admin')

@admin.register(ReservationSettings)
class ReservationSettingsAdmin(admin.ModelAdmin):
    list_display = ('active_date_admin', 'min_time_admin', 'max_time_admin', 'interval_reservation_minutes_admin', 'interval_price_admin')
    ordering = ('-active_date', )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['active_date', 'min_time', 'max_time', 'interval_reservation_minutes', 'interval_price']
        else:
            return []

@admin.register(Information)
class InformationAdmin(admin.ModelAdmin):
    list_display = ('text_type', 'text', 'active')