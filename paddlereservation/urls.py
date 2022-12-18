"""paddlereservation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

import django.contrib.admin.sites
from django.http import Http404
from django.shortcuts import redirect
import logging 
from inspect import getmodule

logger = logging.getLogger(__name__)


# Only allows staff accounts to access the admin site
class RestrictStaffToAdminMiddleware:
    """
    A middleware that restricts staff members access to administration panels.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        module = getmodule(view_func)
        if (module is django.contrib.admin.sites) and (not request.user.is_staff):
            ip = request.META.get('HTTP_X_REAL_IP', request.META.get('REMOTE_ADDR'))
            ua = request.META.get('HTTP_USER_AGENT')
            logger.warn(f'Non-staff user "{request.user}" attempted to access admin site at "{request.get_full_path()}". UA = "{ua}", IP = "{ip}", Method = {request.method}')
            raise Http404

urlpatterns = [
    path('', include('reservation.urls')),
    path('', include('accounts.urls')),
    path('', include('allauth.urls')),
    # path('social/signup', name='allauth_redirect'), # Problem if user already registered in app
    path('admin/logout/', lambda request: redirect('/logout/', permanent=False)),
    path('admin/', admin.site.urls, name='admin_site'),
]
