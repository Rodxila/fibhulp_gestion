from django import forms
from .models import Convocatoria

class ConvocatoriaForm(forms.ModelForm):
    class Meta:
        model = Convocatoria
        fields = '__all__'  # o especificar uno a uno si quieres personalizar
    def clean_codigo_fundanet(self):
        codigo = self.cleaned_data.get('codigo_fundanet', '').strip()
        if not codigo:
            raise forms.ValidationError("Este campo es obligatorio.")
        return codigo


class ConcursoExcelForm(forms.Form):
    archivo_excel = forms.FileField(label="Archivo Excel (.xlsx)")


from django import forms
from .models import Concurso

class ConcursoForm(forms.ModelForm):
    TIPOS_TIPOLOGIA = [
        ('MIXTO', 'MIXTO'),
        ('SUMINISTRO', 'SUMINISTRO'),
        ('SERVICIO', 'SERVICIO'),
    ]
    TIPOS_PRORROGA = [
        ('NO', 'NO'),
        ('SI - 1 AÑO', 'SI - 1 AÑO'),
        ('SI - 18 MESES', 'SI - 18 MESES'),
        ('SI - 2 AÑOS', 'SI - 2 AÑOS'),
        ('SI - 1 AÑO - 2 VECES', 'SI - 1 AÑO - 2 VECES'),
    ]
    TIPOS_ESTADO = [
        ('FINALIZADO', 'FINALIZADO'),
        ('DESIERTO', 'DESIERTO'),
        ('ACTIVO', 'ACTIVO'),
        ('PARALIZADO', 'PARALIZADO'),
        ('CANCELADO', 'CANCELADO'),
        ('DESIERTO Y FINALIZADO', 'DESIERTO Y FINALIZADO'),
        ('EN GESTION', 'EN GESTION'),
    ]

    TIPOLOGÍA = forms.ChoiceField(choices=TIPOS_TIPOLOGIA)
    PRORROGA = forms.ChoiceField(choices=TIPOS_PRORROGA)
    ESTADO = forms.ChoiceField(choices=TIPOS_ESTADO)

    class Meta:
        model = Concurso
        fields = '__all__'
        widgets = {
            'FECHA_FIRMA': forms.TextInput(attrs={'placeholder': 'DD.MM.AAAA'}),
            'FECHA_FIN': forms.TextInput(attrs={'placeholder': 'DD.MM.AAAA'}),
            'FECHA_FIN_PRORROGA': forms.TextInput(attrs={'placeholder': 'DD.MM.AAAA'}),
            'ESTADO_CONTINUACION': forms.Textarea(attrs={'rows': 2}),
        }

    def clean_TIPOLOGÍA(self):
        return self.cleaned_data['TIPOLOGÍA'].upper()

    def clean_PRORROGA(self):
        return self.cleaned_data['PRORROGA'].upper()

    def clean_ESTADO(self):
        return self.cleaned_data['ESTADO'].upper()
