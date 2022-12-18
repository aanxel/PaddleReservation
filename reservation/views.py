from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, date, time
from .forms import CreateReservationForm
from .models import Reservation, ReservationSettings, Information

# default_settings = {
#     'min_time': {
#         'hour': '09',
#         'minute': '00',
#     },
#     'max_time': {
#         'hour': '15',
#         'minute': '00',
#     },
#     'max_interval_reservation': 60,
#     'interval_reservation': 30
# }
# MAX_INTERVAL_RESERVATION = 60


# Create your views here.
def index(request):
    def get_filter_date(request):
        if 'reservation_date' in request.POST:
            return date.fromisoformat(request.POST['reservation_date'])
        elif 'reservation_date' in request.GET:
            return date.fromisoformat(request.GET['reservation_date'])
        else:
            return date.today()

    def get_intervals(filter_date, reservation_settings):
        min_time = reservation_settings['min_time']
        max_time = reservation_settings['max_time']

        intervals = [[(min_time + timedelta(minutes=interval)).strftime('%H:%M'), (min_time + timedelta(minutes=interval+reservation_settings['interval_reservation_minutes'])).strftime('%H:%M'), False] for interval in range(0, (max_time - min_time).seconds // 60, reservation_settings['interval_reservation_minutes'])]

        reservations = Reservation.objects.filter(reservation_date=filter_date).order_by('start_time')
        
        idx = 0
        for reservation in reservations:
            for i in range(idx, len(intervals)):
                if intervals[i][0] == reservation.start_time.strftime('%H:%M'):
                    for j in range(i, i + (datetime.strptime(reservation.end_time.strftime('%H:%M:%S'), '%H:%M:%S') - datetime.strptime(reservation.start_time.strftime('%H:%M:%S'), '%H:%M:%S')).seconds // 60 // reservation_settings['interval_reservation_minutes']):
                        intervals[j][2] = True
                        idx+=1
                    break
                idx+=1

        return intervals

    def get_reservation_settings(request, filter_date):
        reservation_settings = {}
        reservation_settings_tmp = None
        reservations = Reservation.objects.filter(reservation_date=filter_date)

        if len(reservations) > 0 and reservations.first().reservation_settings:
            reservation_settings_tmp = reservations.first().reservation_settings
        else:
            settings = ReservationSettings.objects.order_by('-active_date')
            for setting in settings:
                if datetime.strptime(setting.active_date.strftime('%Y-%m-%d'), '%Y-%m-%d') <= datetime.strptime(filter_date.strftime('%Y-%m-%d'), '%Y-%m-%d'):
                    reservation_settings_tmp = setting
                    break
        
        reservation_settings['min_time'] = datetime.strptime(reservation_settings_tmp.min_time.strftime('%H:%M'), '%H:%M')
        reservation_settings['max_time'] = datetime.strptime(reservation_settings_tmp.max_time.strftime('%H:%M'), '%H:%M')
        reservation_settings['interval_reservation_minutes'] = reservation_settings_tmp.interval_reservation_minutes
        reservation_settings['interval_price'] = reservation_settings_tmp.interval_price
        if request.user.is_authenticated:
            reservation_settings['max_interval_reservation_minutes'] = request.user.user_type.max_interval_reservation_minutes
            reservation_settings['interval_price'] = request.user.user_type.interval_price
        
        return reservation_settings


    def check_intervals(request, reservation_date, start_time, end_time, reservation_settings):
        reservation_date = datetime(year=int(reservation_date.split('-')[0]), month=int(reservation_date.split('-')[1]), day=int(reservation_date.split('-')[2]), hour=int(start_time.split(':')[0]), minute=int(start_time.split(':')[1]))
        start_time = datetime.strptime(start_time, '%H:%M')
        end_time = datetime.strptime(end_time, '%H:%M')
        min_time = reservation_settings['min_time']
        max_time = reservation_settings['max_time']
        flag = True

        # Basic time and date checkers
        if reservation_date < datetime.today():
            messages.success(request, 'La reserva ha de ser posterior al momento actual')
            flag = False
        if start_time >= end_time:
            messages.success(request, 'La hora de finalización de la reserva ha de ser posterior a la de inicio')
            flag = False
        if start_time < min_time:
            messages.success(request, 'La hora de inicio de la reserva ha de ser posterior a las ' + min_time.strftime('%H:%M'))
            flag = False
        if end_time > max_time:
            messages.success(request, 'La hora de finalización de la reserva ha de ser posterior a las ' + max_time.strftime('%H:%M'))
            flag = False
        if (end_time - start_time).seconds / 60 > reservation_settings['max_interval_reservation_minutes']:
            messages.success(request, 'El intervalo de la reserva no puede superar los ' + str(reservation_settings['max_interval_reservation_minutes']) + ' minutos')
            flag = False
        if ((end_time - start_time).seconds / 60) % reservation_settings['interval_reservation_minutes'] != 0:
            messages.success(request, 'El tiempo de la reserva ha de incrementarse en intervalos de ' + str(reservation_settings['interval_reservation_minutes']) + ' minutos [' + str(reservation_settings['interval_reservation_minutes']) + ', ' + str(reservation_settings['interval_reservation_minutes']*2) + ', ' + str(reservation_settings['interval_reservation_minutes']*3) + '...]')
        if ((start_time - min_time).seconds / 60) % reservation_settings['interval_reservation_minutes'] != 0:
            messages.success(request, 'La hora de inicio de la reserva ha de avanzar en intervalos de ' + str(reservation_settings['interval_reservation_minutes']) + ' minutos desde la hora de inicio [' + (min_time + timedelta(minutes=reservation_settings['interval_reservation_minutes'])).strftime('%H:%M, ') + (min_time + timedelta(minutes=reservation_settings['interval_reservation_minutes']*2)).strftime('%H:%M, ') + (min_time + timedelta(minutes=reservation_settings['interval_reservation_minutes']*3)).strftime('%H:%M') + '...]')
            flag = False
        if ((end_time - min_time).seconds / 60) % reservation_settings['interval_reservation_minutes'] != 0:
            messages.success(request, 'La hora de finalización de la reserva ha de avanzar en intervalos de ' + str(reservation_settings['interval_reservation_minutes']) + ' minutos desde la hora de inicio [' + (min_time + timedelta(minutes=reservation_settings['interval_reservation_minutes'])).strftime('%H:%M, ') + (min_time + timedelta(minutes=reservation_settings['interval_reservation_minutes']*2)).strftime('%H:%M, ') + (min_time + timedelta(minutes=reservation_settings['interval_reservation_minutes']*3)).strftime('%H:%M') + '...]')
            flag = False

        # Collision time checker
        reservations = Reservation.objects.filter(reservation_date=reservation_date).order_by('start_time')
        for reservation in reservations:
            if not (start_time < datetime.strptime(reservation.start_time.strftime('%H:%M'), '%H:%M') and end_time <= datetime.strptime(reservation.start_time.strftime('%H:%M'), '%H:%M')) and not (start_time >= datetime.strptime(reservation.end_time.strftime('%H:%M'), '%H:%M') and end_time > datetime.strptime(reservation.end_time.strftime('%H:%M'), '%H:%M')) :
                messages.success(request, 'La reserva presenta una colisión con otra reserva existente, por favor seleccione otra fecha')
                return False

        return flag

    filter_date = get_filter_date(request)
    reservation_settings = get_reservation_settings(request, filter_date)

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CreateReservationForm(request.POST)
            if form.is_valid():
                if not check_intervals(request, request.POST['reservation_date'], request.POST['start_time'], request.POST['end_time'], reservation_settings):
                    return render(request, 'reservation.html', {'form': form, 'intervals': get_intervals(filter_date, reservation_settings)})
                
                new_reservation = form.save(commit=False)
                new_reservation.client = request.user
                new_reservation.duration_minutes = (datetime.strptime(request.POST['end_time'], '%H:%M') - datetime.strptime(request.POST['start_time'], '%H:%M')).seconds // 60
                new_reservation.save()

                return redirect('user_reservations')
            messages.success(request, 'Error al procesar el formulario, inténtelo de nuevo')
            return render(request, 'reservation.html', {'form': form, 'intervals': get_intervals(filter_date, reservation_settings)})
        else:
            messages.success(request, 'Ha de estar registrado y con la sesión iniciada para hacer una reserva')

    return render(request, 'reservation.html', {'form': CreateReservationForm({'reservation_date': filter_date, 'start_time': '09:00', 'end_time': '10:00'}), 'intervals': get_intervals(filter_date, reservation_settings)})

@login_required
def user_reservations(request):
    current_user = request.user

    all_reservations = Reservation.objects.filter(client=current_user).order_by('-reservation_date', 'start_time')
    active_reservations = all_reservations.filter(reservation_date__gte=date.today()).exclude(reservation_date=date.today(), end_time__lte=time(hour=datetime.today().hour, minute=datetime.today().minute))
    past_reservations = all_reservations.exclude(pk__in=active_reservations.values_list('pk', flat=True))

    return render(request, 'user_reservations.html', {'active_reservations': active_reservations, 'past_reservations': past_reservations})

def information(request):
    information = Information.objects.filter(active = True)
    return render(request, 'information.html', {'information_location': information.filter(text_type='LO').order_by('priority'), 'information_use_policy': information.filter(text_type='UP').order_by('priority'), 'information_price': information.filter(text_type='PR').order_by('priority')})