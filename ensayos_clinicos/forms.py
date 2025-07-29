from django import forms
from .models import DatosEnsayo

class DatosEnsayoForm(forms.ModelForm):
    class Meta:
        model = DatosEnsayo
        fields = ['mes', 'año', 'ensayos', 'observacionales', 'adendas']



class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario')
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
