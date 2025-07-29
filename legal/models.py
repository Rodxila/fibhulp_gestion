from django.db import models

class Convocatoria(models.Model):
    tipo = models.CharField(max_length=100)
    nif_tercero = models.CharField(max_length=100, blank=True, null=True)
    ip = models.CharField(max_length=100)
    nombre = models.CharField(max_length=200)
    objeto = models.CharField(max_length=500, blank=True, null=True)
    pais_ccaa = models.CharField("País/CCAA", max_length=100, blank=True, null=True)
    codigo_fundanet = models.CharField(max_length=100, blank=False, null=False, unique=True)
    cantidad = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    overhead = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    ruta = models.CharField(max_length=200, blank=True, null=True)
    factura = models.CharField(max_length=20, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    estado_contabilidad = models.CharField(max_length=100, blank=True, null=True)
    contactos_fra = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.tipo} - {self.nombre}"

class Concurso(models.Model):
    EXPEDIENTE = models.CharField(
    max_length=100, blank=False, null=False, unique=True, db_column='N.º EXPED'
    )
    PROCEDIMIENTO = models.CharField(max_length=255)
    TIPOLOGÍA = models.CharField(max_length=255)
    FECHA_FIRMA = models.CharField(max_length=100, blank=True, null=True)
    DURACIÓN_CONTRATO = models.CharField(max_length=255, blank=True, null=True)
    FECHA_FIN = models.CharField(max_length=100, blank=True, null=True)
    PRORROGA = models.CharField(max_length=255, blank=True, null=True, db_column='¿PRÓRROGAS?')
    FECHA_FIN_PRORROGA = models.CharField(max_length=100, blank=True, null=True)
    CANTIDAD_ECONOMICA_MAX = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True, db_column='CANTIDAD ECONÓMICA MÁX (IVA INCLUIDO)'
    )
    ESTADO = models.CharField(max_length=100, blank=True, null=True)
    ESTADO_CONTINUACION = models.TextField(blank=True, null=True, db_column='ESTADO CONTINUACION')

    def __str__(self):
        return self.EXPEDIENTE

