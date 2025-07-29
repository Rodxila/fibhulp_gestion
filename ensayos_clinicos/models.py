from django.db import models

MESES = [(mes, mes) for mes in [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
]]

class DatosEnsayo(models.Model):
    mes = models.CharField(max_length=20, choices=MESES)
    año = models.PositiveIntegerField()
    ensayos = models.PositiveIntegerField(default=0)
    observacionales = models.PositiveIntegerField(default=0)
    adendas = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.mes} {self.año}: {self.ensayos} Ensayos, {self.observacionales} Obs., {self.adendas} Adendas"

class FacturaMensual(models.Model):
    año = models.PositiveIntegerField()
    mes = models.CharField(max_length=3)  # Ej: Ene, Feb...
    cantidad = models.FloatField()
    numero_facturas = models.PositiveIntegerField(default=1)
    fecha_ultimo_cobro = models.DateField(null=True, blank=True)  # NUEVO CAMPO


    def media(self):
        if self.numero_facturas > 0:
            return round(self.cantidad / self.numero_facturas, 2)
        return 0

    def __str__(self):
        return f"{self.mes} {self.año}: €{self.cantidad} ({self.numero_facturas} facturas)"


class Usuario(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)  # Hash recomendado (ver más abajo)
    es_backup = models.BooleanField(default=False)
    secciones = models.CharField(max_length=100, default='1')  # 1 = ensayos_clinicos, 2 = legal
    def __str__(self):
        return self.username

from django.db import models

class FacturaDetalle(models.Model):
    año = models.IntegerField()
    mes = models.CharField(max_length=10)
    identificador = models.CharField(max_length=255, blank=True, null=True)
    concepto = models.TextField(blank=True, null=True)
    cantidad = models.DecimalField(max_digits=15, decimal_places=2)
    fecha_emision = models.DateField(blank=True, null=True)
    fecha_ultimo_cobro = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.identificador} - {self.mes} {self.año}"

