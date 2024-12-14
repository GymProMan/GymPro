from django import forms
from .models import Miembro, Membresia, MembresiaTipo

class MiembroForm(forms.ModelForm):
    class Meta:
        model = Miembro
        fields = ['nombre', 'apellido', 'genero', 'numero_contacto', 'foto']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            #'clave': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-select'}),
            'numero_contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class MembresiaForm(forms.ModelForm):
    class Meta:
        model = Membresia
        fields = ['tipo_membresia']
        widgets = {
            'tipo_membresia': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_membresia'].queryset = MembresiaTipo.objects.filter(activo=True)

class MembresiaTipoForm(forms.ModelForm):
    class Meta:
        model = MembresiaTipo
        fields = ['nombre', 'duracion', 'unidad_tiempo', 'beneficios', 'costo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'duracion': forms.NumberInput(attrs={'class': 'form-control'}),
            'unidad_tiempo': forms.Select(attrs={'class': 'form-select'}),
            'beneficios': forms.Textarea(attrs={'class': 'form-control'}),
            'costo': forms.NumberInput(attrs={'class': 'form-control'}),
        }

from django import forms

class ClaveAccesoForm(forms.Form):
    clave = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control clave-input',
                'placeholder': 'Ingresa tu clave de acceso',
                'autocomplete': 'off'  # Deshabilita el autocompletado
            }
        ),
        label="Clave de Acceso",
    )


class FiltroAsistenciaForm(forms.Form):
    fecha = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',  # Clase de Bootstrap
                'placeholder': 'Selecciona una fecha'
            }
        )
    )
    miembro = forms.ModelChoiceField(
        queryset=Miembro.objects.all(),
        required=False,
        empty_label="Todos los miembros",
        widget=forms.Select(
            attrs={
                'class': 'form-select',  # Clase de Bootstrap
            }
        )
    )