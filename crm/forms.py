from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput
from django.utils.translation import gettext_lazy as _

# Crear y registrar usuarios

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


# Autentificar a usuario



class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=TextInput(attrs={
            'class': 'form-control form-control-lg',  # Clases Bootstrap
            'placeholder': 'Usuario',
            'id': 'form2Example17'  # Opcional, para referencias en el HTML
        })
    )

    error_messages = {
        'invalid_login': _("El usuario o la contraseña son incorrectos. Inténtalo de nuevo."),
        'inactive': _("Esta cuenta está inactiva."),
    }
    password = forms.CharField(
        widget=PasswordInput(attrs={
            'class': 'form-control form-control-lg',  # Clases Bootstrap
            'placeholder': 'Contraseña',
            'id': 'form2Example27'  # Opcional, para referencias en el HTML
        })
    )
