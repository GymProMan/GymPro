from typing import Required

from django import forms

from Aparatos.models import CategoriaAparato

class crearAparato(forms.Form):
    nombre = forms.CharField(
        label='Nombre',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
    )
    cantidad = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )
    bandera = forms.BooleanField(
        label='¿Es mancuerna?',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )
    tipo = forms.CharField(
        label='Tipo',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    ubicacion = forms.CharField(
        label='Ubicación',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    estado = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.HiddenInput(),
    )

class vincular(forms.Form):
    idAparatos = forms.IntegerField(
        widget=forms.HiddenInput()
    )
    categorias = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
class createCategoria(forms.Form):
    nombrecat = forms.CharField(
        label='Nombre',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', }),
    )
