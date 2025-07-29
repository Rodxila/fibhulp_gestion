from django.db import models
from .validators import validar_tamano_archivo
class FormularioContratacion(models.Model):
    # ------- RELACIONES -------
    proceso_codigo = models.CharField(max_length=100)  # Código de proceso de selección
    puesto = models.CharField(max_length=100)
    ip = models.CharField(max_length=255, blank=True, null=True)
    funciones = models.TextField(blank=True, null=True)
    alta = models.DateField(blank=True, null=True, verbose_name="Fecha de alta")
    seleccionado = models.BooleanField(default=False)
    token_acceso = models.CharField(max_length=100, blank=True, null=True)
    # ------- PARTE TRABAJADOR -------
    cv = models.FileField(upload_to='cvs/', null=True, blank=True)  # solo si se decide guardar
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150, blank=True, null=True)
    direccion_completa = models.CharField(max_length=255, blank=True, null=True)
    poblacion = models.CharField(max_length=100, blank=True, null=True)
    provincia = models.CharField(max_length=100, blank=True, null=True)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    nacionalidad = models.CharField(max_length=100, blank=True, null=True)
    nif = models.CharField(max_length=20, blank=True, null=True)
    nie = models.CharField(max_length=20, blank=True, null=True)
    carta_identidad = models.CharField(max_length=20, blank=True, null=True)
    pasaporte = models.CharField(max_length=20, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField()
    fecha_nacimiento = models.DateField(max_length=20, blank=True, null=True)
    sexo = models.CharField(max_length=20, blank=True, null=True)
    fotocopia_tarjeta_inem = models.FileField(
        upload_to='documentos/', null=True, blank=True,
        validators=[validar_tamano_archivo]
    )
    soporte_documental_meritos = models.FileField(
        upload_to='documentos/', null=True, blank=True,
        validators=[validar_tamano_archivo]
    )
    certificado_titularidad_bancaria = models.FileField(
        upload_to='documentos/', null=True, blank=True,
        validators=[validar_tamano_archivo]
    )
    certificado_delitos_sexuales = models.FileField(
        upload_to='documentos/', null=True, blank=True,
        validators=[validar_tamano_archivo]
    )
    curriculum = models.FileField(
        upload_to='documentos/', null=True, blank=True,
        validators=[validar_tamano_archivo]
    )
    vida_laboral =models.FileField(
        upload_to='documentos/', null=True, blank=True,
        validators=[validar_tamano_archivo]
    )
    fotocopia_master_doctorado =models.FileField(
        upload_to='documentos/', null=True, blank=True,
        validators=[validar_tamano_archivo]
    )

    ficha_firmada = models.FileField(
        upload_to='fichas_firmadas/', blank=True, null=True, validators=[validar_tamano_archivo]
    )
    nivel_estudios = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)

    inscrito_sepe = models.BooleanField(
        default=False,
        verbose_name="Inscrito/a como demandante de empleo en el SEPE"
    )
    documento_inscrito_sepe = models.FileField(
        upload_to='documentos/', blank=True, null=True, validators=[validar_tamano_archivo]
    )

    mayor_30_sepe = models.BooleanField(
        default=False,
        verbose_name="Menor de 30 años inscrito/a como demandante de empleo"
    )
    documento_mayor_30_sepe = models.FileField(
        upload_to='documentos/', blank=True, null=True, validators=[validar_tamano_archivo]
    )
    discapacitado = models.BooleanField(
        default=False,
        verbose_name="Discapacidad reconocida ≥ 33%"
    )
    documento_discapacitado = models.FileField(
        upload_to='documentos/', blank=True, null=True, validators=[validar_tamano_archivo]
    )
    excluido_social = models.BooleanField(
        default=False,
        verbose_name="Situación de exclusión social acreditada"
    )
    documento_excluido_social = models.FileField(
        upload_to='documentos/', blank=True, null=True, validators=[validar_tamano_archivo]
    )
    victima_violencia_domestica = models.BooleanField(
        default=False,
        verbose_name="Víctima de violencia de género o doméstica"
    )
    documento_victima_violencia_domestica = models.FileField(
        upload_to='documentos/', blank=True, null=True, validators=[validar_tamano_archivo]
    )
    mujer_reincorporada = models.BooleanField(
        default=False,
        verbose_name="Mujer reincorporada en los 2 años siguientes al parto"
    )
    documento_mujer_reincorporada = models.FileField(
        upload_to='documentos/', blank=True, null=True, validators=[validar_tamano_archivo]
    )
    capacidad_intelectual_limite = models.BooleanField(
        default=False,
        verbose_name="Persona con capacidad intelectual límite"
    )
    documento_capacidad_intelectual_limite = models.FileField(
        upload_to='documentos/', blank=True, null=True, validators=[validar_tamano_archivo]
    )
    contrato_temporal_6m_fibh = models.BooleanField(
        default=False,
        verbose_name="Contrato temporal de al menos 6 meses en la FIBHULP"
    )
    documento_contrato_temporal_6m_fibh = models.FileField(
        upload_to='documentos/', blank=True, null=True, validators=[validar_tamano_archivo]
    )
    contrato_indefinido_12m_fibh = models.BooleanField(
        default=False,
        verbose_name="Contrato indefinido de al menos 12 meses en la FIBHULP"
    )
    documento_contrato_indefinido_12m_fibh = models.FileField(
        upload_to='documentos/', blank=True, null=True, validators=[validar_tamano_archivo]
    )
    contrato_indefinido_3m_otra_empresa = models.BooleanField(
        default=False,
        verbose_name="Contrato indefinido de al menos 3 meses en otra empresa"
    )
    documento_contrato_indefinido_3m_otra_empresa = models.FileField(
        upload_to='documentos/', blank=True, null=True, validators=[validar_tamano_archivo]
    )


    # ------- PARTE EMPRESA (RRHH) -------
    TIPOS_CONTRATO = [
        ("Indefinido", [
            ("indefinido_ordinario", "Ordinario"),
            ("indefinido_ct", "Actividades Científico-Técnicas (Apartado 3.B)"),
            ("transformacion_ct", "Transformación Actividades Científico-Técnicas (Apartado 3.B)"),
        ]),
        ("Temporal", [
            ("temporal_fondos_europeos", "Vinculado a fondos europeos (NO competitivos)"),
            ("temporal_prtr", "Plan de Recuperación, Transformación y Resiliencia (PRTR)"),
            ("temporal_produccion_imprevisible", "Producción imprevisible (máx. 6 meses) → Causa"),
            ("temporal_produccion_previsible", "Producción previsible (empresa máx. 90 días/año) → Causa"),
            ("temporal_interinidad", "Interinidad → Causa"),
            ("temporal_practicas", "Prácticas → Titulación y fecha obtención"),
            ("predoc", "PREDOC en formación"),
            ("postdoc", "De acceso a SECTI (postdoc)"),
            ("distinguido", "Investigador distinguido"),
        ])
    ]

    DIRECCIONES = [
        ("CL Diego de León 62", "H. Princesa"),
        ("CL del Maestro Vives, 2", "H. Santa Cristina"),
        ("Av. de Menéndez Pelayo, 65", "H. N. Jesús"),
    ]

    direccion_centro = models.CharField(max_length=100, choices=DIRECCIONES, default="CL Diego de León 62")



    tipo_contrato = models.CharField(
        max_length=100,
        choices=TIPOS_CONTRATO,
        blank=True,
        null=True
    )

    duracion = models.IntegerField(blank=True, null=True, help_text="Duración del contrato en meses")
    causa_contrato = models.TextField(blank=True, null=True)  # Condicional según tipo de contrato
    titulacion_practicas = models.CharField(max_length=150, blank=True, null=True)
    titulacion_y_fecha  = models.CharField(blank=True, null=True)

    jornada = models.CharField(max_length=100, choices=[('Completa', 'Completa'), ('Parcial', 'Parcial')])
    horas_semana = models.IntegerField(blank=True, null=True)
    distribucion_jornada = models.TextField(blank=True, null=True)
    observaciones_jornada = models.CharField(max_length=500, blank=True, null=True)

    convocatoria = models.CharField(max_length=100)
    categoria_area = models.CharField(max_length=10)
    categoria_grupo = models.CharField(max_length=10)
    categoria_profesional = models.CharField(max_length=100)
    prestara_servicios_como = models.CharField(max_length=150)
    tipo_personal = models.CharField(max_length=100, choices=[
        ('PI', 'Personal Investigador (Área 1)'),
        ('SOPORTE', 'Soporte Científico-Técnico (Área 2)'),
        ('GESTION', 'Administración y Gestión (Área 3)')
    ])
    logos = models.ImageField(upload_to='logos/', null=True, blank=True)
    clausulas_adicionales_rrhh = models.TextField(
        blank=True,
        null=True,
        verbose_name="Cláusulas adicionales extraordinarias"
    )

    objeto_contrato = models.TextField()
    financiacion = models.TextField()

    aplica_tablas_convenio = models.BooleanField(default=True)
    salario_base = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    carrera_profesional = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    complementos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salario_fijo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    coste_fijado_convocatoria = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    importe_coste_empresa_anual = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    requiere_autorizacion_hacienda = models.BooleanField(null=True, blank=True)

    # ------- CONTROL DE ESTADO -------
    rellenado_por_empleado = models.BooleanField(default=False)
    rellenado_por_empresa = models.BooleanField(default=False)
    enviado_a_fundanet = models.BooleanField(default=False)
    enviado_a_gestoria = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"{self.nombre} {self.apellidos} - Proceso {self.proceso_codigo}"

import uuid
from django.db import models
# models.py
