from django import forms
import datetime
from reservation.models import Reservation

# Pretty date and time input
# https://stackoverflow.com/questions/22846048/django-form-as-p-datefield-not-showing-input-type-as-date
class DateInput(forms.DateInput):
    input_type = 'date'
class TimeInput(forms.DateInput):
    input_type = 'time'

class CreateReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('reservation_date', 'start_time', 'end_time')

        widgets = {
            # 'reservation_date': DateInput,
            'reservation_date': forms.DateInput(attrs={'type': 'date', 'onblur' : "window.location.href = '?reservation_date=' + document.getElementById('id_reservation_date').value;"}),
            'start_time': TimeInput,
            'end_time': TimeInput,
        }
        labels = {
            'reservation_date': 'Seleccionar fecha',
            'start_time': 'Hora inicio',
            'end_time': 'Hora fin',
        }