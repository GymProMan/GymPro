from lib2to3.fixes.fix_input import context

from django.shortcuts import render, redirect
from . forms import CreateUserForm, LoginForm #Importo el modelo de usuarios custom y el de autentificaciom
from django.contrib.auth.decorators import login_required

# Modelos de autentificacion y funciones

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout

@login_required
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")

    context = {'registerform': form}

    return  render(request,'crm/register.html', context=context)

def my_login(request):
    form = LoginForm()
    errors = None  # Variable para almacenar los errores

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = auth.authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect("index")
        else:
            errors = form.non_field_errors()  # Captura los errores generales del formulario

    context = {
        'loginform': form,
        'errors': errors,  # Incluye los errores en el contexto
    }

    return render(request, 'crm/my_login.html', context=context)

def user_logout(request):
    auth.logout(request)
    return redirect('my_login') #Te redirecciona al cerrar sesion

#@login_required(login_url='my_login')
#def dashboard(request):
#    return render(request, 'crm/dashboard.html')