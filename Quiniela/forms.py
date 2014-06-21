from django import forms
from django.contrib.auth.forms import UserCreationForm
from Quiniela.models import *
__author__ = 'anyul.rivas'


class PronosticoForm(forms.ModelForm):
    goles_equipo_a = forms.IntegerField(min_value=0, max_value=10)
    goles_equipo_b = forms.IntegerField(min_value=0, max_value=10)

    class Meta:
        model = Pronostico
        exclude = ["puntos"]
        widgets = {
            "usuario": forms.HiddenInput(),
            "partido": forms.HiddenInput()
        }


class UsuarioForm(UserCreationForm):
    pass


class PartidoForm(forms.ModelForm):

    class Meta:
        model = Partido
        exclude = ["tipo_partido", "equipo_ganador", "fecha", "equipo_a", "equipo_b"]