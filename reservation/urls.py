from django.urls import path
from reservation import views

urlpatterns = [
    path('', views.index, name='reservation'),
    path('reservations', views.user_reservations, name='user_reservations'),
    path('information', views.information, name='information'),
]