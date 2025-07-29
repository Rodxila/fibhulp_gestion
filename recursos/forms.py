from django import forms
from .models import DatosEnsayo

class DatosEnsayoForm(forms.ModelForm):
    class Meta:
        model = DatosEnsayo
        fields = ['mes', 'ensayos', 'observacionales', 'adendas']
