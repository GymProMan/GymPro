# forms.py
from django import forms
from .models import Turno
from .models import Personal


class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['nombre', 'hora_inicio', 'hora_final']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_final': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }


class PersonalForm(forms.ModelForm):
    class Meta:
        model = Personal
        fields = ['turno', 'nombre', 'apellido', 'fecha_inicio', 'puesto', 'numero_contacto', 'foto']
        widgets = {
            'turno': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'puesto': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }