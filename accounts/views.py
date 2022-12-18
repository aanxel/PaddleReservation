from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, logout, login, get_user_model
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.safestring import mark_safe
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .forms import LoginForm, RegisterForm
from .tokens import account_activation_token

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('reservation')
        else:
            messages.success(request, 'Ha habido un error en el inicio de sesión, pruebe de nuevo')
            form = LoginForm(request.POST)
            # redirect('login')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.success(request, 'Ha cerrado sesión correctamente')
    return redirect('reservation')

def activate_user(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Gracias por confirmar su cuenta, ya puede iniciar sesión con la misma')
        return redirect('login')
    else:
        messages.error(request, 'El link de activación es invalido')
    
    return redirect('reservation')

def activate_email(request, user, to_email):
    mail_subject = 'Activar tu cuenta en pádel Fuente de Santa Cruz.'
    message = render_to_string('activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, mark_safe(f'Por favor <b>{user}</b>, diríjase a la bandeja de entrada de su email <b>{to_email}</b> y entre en el correo de activación recibido para completar el registro. <b>Nota:</b> Si no encuentra el correo busque en la carpeta de spam'))
    else:
        messages.error(request, f'Ha habido un problema al enviar el correo de confirmación a {to_email}, por favor pruebe de nuevo')

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activate_email(request, user, form.cleaned_data.get('email'))
            # messages.success(request, 'Antes de iniciar sesión por primera vez, diríjase a su correo y confirme el registro')
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})