from django import forms
from ensayos_clinicos.models import Usuario
from .models import FormularioContratacion
from .utils import obtener_ofertas_disponibles

def generar_choices_ofertas():
    try:
        ofertas = obtener_ofertas_disponibles()
        print("OFERTAS DESPLEGABLE -->", ofertas)
        return ofertas
    except Exception as e:
        print("Error generando choices:", e)
        return []


class FormularioRRHHForm(forms.ModelForm):
    jornada_dia_inicio = forms.CharField(required=False)
    jornada_dia_fin = forms.CharField(required=False)
    jornada_hora_fin = forms.CharField(required=False)

    class Meta:
        model = FormularioContratacion
        fields = [
            'alta',
            'direccion_centro',
            'tipo_contrato',
            'causa_contrato',
            'titulacion_y_fecha',
            'jornada',
            'horas_semana',
            'distribucion_jornada',
            'duracion',
            'observaciones_jornada',
            'clausulas_adicionales_rrhh',
            'prestara_servicios_como',
        ]
        widgets = {
            'alta': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['horas_semana'].required = False
        self.fields['distribucion_jornada'].required = False
        self.fields['causa_contrato'].required = False
        self.fields['titulacion_y_fecha'].required = False
        self.fields['duracion'].required = False
    def clean(self):
        cleaned_data = super().clean()
        # reconstruir y guardar la frase completa
        dia_inicio = cleaned_data.get('jornada_dia_inicio', '')
        dia_fin = cleaned_data.get('jornada_dia_fin', '')
        hora_inicio = cleaned_data.get('jornada_hora_inicio', '')
        hora_fin = cleaned_data.get('jornada_hora_fin', '')

        if dia_inicio and dia_fin and hora_inicio and hora_fin:
            cleaned_data['distribucion_jornada'] = (
                f"De {dia_inicio} a {dia_fin}, en horario de {hora_inicio} h a {hora_fin} h"
            )
        return cleaned_data

class EmpleadoForm(forms.ModelForm):
    convocatoria = forms.ChoiceField(choices=[], label="Oferta a la que postula")

    class Meta:
        model = FormularioContratacion
        fields = [
            'convocatoria',
            'nombre', 'apellidos', 'direccion_completa', 'poblacion', 'provincia', 'codigo_postal',
            'nacionalidad', 'nif', 'nie', 'carta_identidad', 'pasaporte', 'telefono', 'email',
            'fecha_nacimiento', 'sexo', 'fotocopia_tarjeta_inem', 'soporte_documental_meritos',
            'certificado_titularidad_bancaria', 'certificado_delitos_sexuales',
            'cv', 'vida_laboral', 'fotocopia_master_doctorado'
        ]
        widgets = {
            'fecha_nacimiento': forms.TextInput(attrs={'placeholder': 'DD/MM/AAAA'}),
            'sexo': forms.TextInput(attrs={'placeholder': 'Hombre / Mujer / Otro'}),
        }
        help_texts = {
            'nif': 'Rellenar solo uno de los campos de identificación.',
            'nie': 'Rellenar solo uno de los campos de identificación.',
            'carta_identidad': 'Rellenar solo uno de los campos de identificación.',
            'pasaporte': 'Rellenar solo uno de los campos de identificación.',
        }

    def __init__(self, *args, **kwargs):
        ofertas = kwargs.pop('ofertas_disponibles', None)
        super().__init__(*args, **kwargs)
        if ofertas:
            self.fields['convocatoria'].choices = ofertas
        else:
            self.fields['convocatoria'].choices = []

# forms.py
from django import forms
from .models import FormularioContratacion

class SubidaFichaForm(forms.ModelForm):
    class Meta:
        model = FormularioContratacion
        fields = [
            # Datos personales
            'nombre', 'apellidos', 'direccion_completa', 'poblacion', 'provincia',
            'codigo_postal', 'nacionalidad', 'nif', 'nie', 'carta_identidad', 'pasaporte',
            'telefono', 'email', 'fecha_nacimiento', 'sexo','nivel_estudios', 'especialidad',
            'inscrito_sepe', 'mayor_30_sepe', 'discapacitado', 'excluido_social', 'victima_violencia_domestica', 'mujer_reincorporada' , 'capacidad_intelectual_limite', 'contrato_temporal_6m_fibh', 'contrato_indefinido_12m_fibh', 'contrato_indefinido_3m_otra_empresa',

            # Documentos
            'fotocopia_tarjeta_inem',
            'soporte_documental_meritos',
            'certificado_titularidad_bancaria',
            'certificado_delitos_sexuales',
            'curriculum',
            'vida_laboral',
            'fotocopia_master_doctorado',
            'ficha_firmada',
            'documento_inscrito_sepe',
            'documento_mayor_30_sepe',
            'documento_discapacitado',
            'documento_excluido_social',
            'documento_victima_violencia_domestica',
            'documento_mujer_reincorporada',
            'documento_capacidad_intelectual_limite',
            'documento_contrato_temporal_6m_fibh',
            'documento_contrato_indefinido_12m_fibh',
            'documento_contrato_indefinido_3m_otra_empresa',
        ]

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = FormularioContratacion
        fields = '__all__'  # O especifica todos los campos necesarios si prefieres más control

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['horas_semana'].required = False
        self.fields['distribucion_jornada'].required = False
        self.fields['causa_contrato'].required = False
        self.fields['titulacion_y_fecha'].required = False
        self.fields['duracion'].required = False





