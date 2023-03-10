# Generated by Django 4.1.4 on 2022-12-16 16:42

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import reservation.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reservation', '0011_reservation_total_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_type', models.CharField(choices=[('LO', 'Location'), ('UP', 'Use Policy'), ('PR', 'Prices'), ('DF', 'Default')], default='DF', max_length=2)),
                ('text', models.CharField(max_length=500)),
                ('active', models.BooleanField(default=True)),
                ('priority', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='reservation',
            name='client',
            field=models.ForeignKey(help_text='(client)', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='duration_minutes',
            field=models.IntegerField(default=0, help_text='(duration_minutes)', verbose_name='Duración de la reserva en minutos'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='end_time',
            field=models.TimeField(help_text='(end_time)', verbose_name='Hora de finalización de la reserva'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='reservation_date',
            field=models.DateField(help_text='(reservation_date)', verbose_name='Fecha de la reserva'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='reservation_settings',
            field=models.ForeignKey(help_text='(reservation_settings)', null=True, on_delete=django.db.models.deletion.SET_NULL, to='reservation.reservationsettings', verbose_name='Configuraciones de reserva'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='start_time',
            field=models.TimeField(help_text='(start_time)', verbose_name='Hora de inicio de la reserva'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='total_price',
            field=models.PositiveSmallIntegerField(default=0, help_text='(total_price)', verbose_name='Precio de la reserva en euros'),
        ),
        migrations.AlterField(
            model_name='reservationsettings',
            name='active_date',
            field=models.DateField(default=django.utils.timezone.now, help_text='(active_date)', unique=True, verbose_name='Fecha de activación'),
        ),
        migrations.AlterField(
            model_name='reservationsettings',
            name='interval_price',
            field=models.PositiveSmallIntegerField(default=0, help_text='(interval_price)', validators=[django.core.validators.MinValueValidator(0, 'El precio del intervalo mínimo ("interval_price") de reserva no puede ser negativo')], verbose_name='Precio por intervalo de reserva'),
        ),
        migrations.AlterField(
            model_name='reservationsettings',
            name='interval_reservation_minutes',
            field=models.PositiveSmallIntegerField(default=0, help_text='(interval_reservation_minutes)', validators=[django.core.validators.MinValueValidator(1, 'El intervalo mínimo ("interval_reservation_minutes") de reserva en minutos no puede ser inferior a 1')], verbose_name='Intervalo mínimo de reservas en minutos'),
        ),
        migrations.AlterField(
            model_name='reservationsettings',
            name='max_time',
            field=models.TimeField(help_text='(max_time)', validators=[reservation.models.time_validator_seconds], verbose_name='Hora finalización de reservas'),
        ),
        migrations.AlterField(
            model_name='reservationsettings',
            name='min_time',
            field=models.TimeField(help_text='(min_time)', validators=[reservation.models.time_validator_seconds], verbose_name='Hora inicio de reservas'),
        ),
    ]
