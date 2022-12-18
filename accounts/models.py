from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class TypeUser(models.Model):
    name = models.CharField(max_length=50, unique=True)
    max_interval_reservation_minutes = models.PositiveSmallIntegerField()
    interval_price = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.ForeignKey(TypeUser, default=lambda: TypeUser.objects.filter(name='normal').first(),on_delete=models.SET_NULL, null=True)