from django.contrib import admin
from .models import CustomUser, TypeUser

# Register your models here.
admin.site.register(CustomUser)

@admin.register(TypeUser)
class TypeUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_interval_reservation_minutes', 'interval_price')