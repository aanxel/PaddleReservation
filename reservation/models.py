from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.contrib import admin
from datetime import datetime
from accounts.models import CustomUser

# Validator that checks if time fields have seconds equal to 0
def time_validator_seconds(value):
        if value.second != 0:
            raise ValidationError('Solo se pueden modificar las horas y los minutos, los segundos han de dejarse a 00')
        else:
            return value

class ReservationSettings(models.Model):
    # Be really careful with setting an active_date previous or equal to the actual date. It may invoque a problem with the existing reservations
    active_date = models.DateField(default=timezone.now, unique=True, verbose_name='Fecha de activación', help_text='(active_date)')
    min_time = models.TimeField(validators=[time_validator_seconds], verbose_name='Hora inicio de reservas', help_text='(min_time)')
    max_time = models.TimeField(validators=[time_validator_seconds], verbose_name='Hora finalización de reservas', help_text='(max_time)')
    interval_reservation_minutes = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(1, 'El intervalo mínimo ("interval_reservation_minutes") de reserva en minutos no puede ser inferior a 1')], verbose_name='Intervalo mínimo de reservas en minutos', help_text='(interval_reservation_minutes)')
    interval_price = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0, 'El precio del intervalo mínimo ("interval_price") de reserva no puede ser negativo')], verbose_name='Precio por intervalo de reserva', help_text='(interval_price)')

    def clean(self):
        min_time = datetime.strptime(self.min_time.strftime('%H:%M'), '%H:%M')
        max_time = datetime.strptime(self.max_time.strftime('%H:%M'), '%H:%M')
        if min_time >= max_time:
            raise ValidationError('La hora de inicio ("min_time") ha de ser anterior a la hora de finalización de reservas ("max_time") ')
        if (max_time - min_time).seconds / 60 % self.interval_reservation_minutes != 0:
            raise ValidationError('Entre la hora de inicio ("min_time") y la hora de finalización ("max_time") de las reservas han de entrar de [1, n] | n ∈ ℕ intervalos del tamaño "interval_reservation_minutes"')
    
    def __str__(self):
        return self.active_date.strftime('%Y-%m-%d') + ' (yyyy-mm-dd)'

    @admin.display(description=mark_safe(active_date.verbose_name + '<br>' + active_date.help_text))
    def active_date_admin(self):
        return self.active_date.__str__()

    @admin.display(description=mark_safe(min_time.verbose_name + '<br>' + min_time.help_text))
    def min_time_admin(self):
        return self.min_time.strftime('%H:%M')
    
    @admin.display(description=mark_safe(max_time.verbose_name + '<br>' + max_time.help_text))
    def max_time_admin(self):
        return self.max_time.strftime('%H:%M')
    
    @admin.display(description=mark_safe(interval_reservation_minutes.verbose_name + '<br>' + interval_reservation_minutes.help_text))
    def interval_reservation_minutes_admin(self):
        return str(self.interval_reservation_minutes) + ' minutes'
    
    @admin.display(description=mark_safe(interval_price.verbose_name + '<br>' + interval_price.help_text))
    def interval_price_admin(self):
        return str(self.interval_price) + ' €'

class Reservation(models.Model):
    reservation_date = models.DateField(verbose_name='Fecha de la reserva', help_text='(reservation_date)')
    start_time = models.TimeField(verbose_name='Hora de inicio de la reserva', help_text='(start_time)')
    end_time = models.TimeField(verbose_name='Hora de finalización de la reserva', help_text='(end_time)')
    duration_minutes = models.IntegerField(default=0, verbose_name='Duración de la reserva en minutos', help_text='(duration_minutes)')
    total_price = models.PositiveSmallIntegerField(default=0, verbose_name='Precio de la reserva en euros', help_text='(total_price)')

    client = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, verbose_name='Usuario', help_text='(client)')
    reservation_settings = models.ForeignKey(ReservationSettings, on_delete=models.SET_NULL, null=True, verbose_name='Configuraciones de reserva', help_text='(reservation_settings)')

    def __str__(self):
        return self.reservation_date.strftime('%b. %d, %Y') + self.start_time.strftime(' [%H:%M') + ' - ' + self.end_time.strftime('%H:%M]') + ' → ' + self.client.username + ' (' + str(self.duration_minutes) + ' minutes)'

    @admin.display(description=mark_safe(reservation_date.verbose_name + '<br>' + reservation_date.help_text))
    def reservation_date_admin(self):
        return self.reservation_date.__str__()

    @admin.display(description=mark_safe(start_time.verbose_name + '<br>' + start_time.help_text))
    def start_time_admin(self):
        return self.start_time.strftime('%H:%M')
    
    @admin.display(description=mark_safe(end_time.verbose_name + '<br>' + end_time.help_text))
    def end_time_admin(self):
        return self.end_time.strftime('%H:%M')
    
    @admin.display(description=mark_safe(duration_minutes.verbose_name + '<br>' + duration_minutes.help_text))
    def duration_minutes_admin(self):
        return str(self.duration_minutes) + ' minutos'
    
    @admin.display(description=mark_safe(total_price.verbose_name + '<br>' + total_price.help_text))
    def total_price_admin(self):
        return str(self.total_price) + ' €'
    
    @admin.display(description=mark_safe(client.verbose_name + '<br>' + client.help_text))
    def client_admin(self):
        return self.client
    
    @admin.display(description=mark_safe(reservation_settings.verbose_name + '<br>' + reservation_settings.help_text))
    def reservation_settings_admin(self):
        return self.reservation_settings

class Information(models.Model):
    TEXT_TYPE_CHOICES = [
        ('LO', 'Location'),
        ('UP', 'Use Policy'),
        ('PR', 'Prices'),
        ('DF', 'Default')
    ]

    text_type = models.CharField(max_length=2 ,choices=TEXT_TYPE_CHOICES, default='DF')
    text = models.TextField(max_length=500)
    active = models.BooleanField(default=True)
    priority = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return mark_safe(self.text)