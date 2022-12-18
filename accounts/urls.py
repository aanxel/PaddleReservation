from django.urls import path
from accounts.views import login_user, logout_user, register_user, activate_user

urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('activate/<uidb64>/<token>', activate_user, name='activate_user'),
]