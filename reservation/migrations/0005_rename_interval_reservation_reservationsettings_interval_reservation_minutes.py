# Generated by Django 4.1.4 on 2022-12-14 17:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0004_alter_reservationsettings_active_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservationsettings',
            old_name='interval_reservation',
            new_name='interval_reservation_minutes',
        ),
    ]
