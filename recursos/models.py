from django.db import models

MESES = [
    ('Enero', 'Enero'), ('Febrero', 'Febrero'), ('Marzo', 'Marzo'), ('Abril', 'Abril'),
    ('Mayo', 'Mayo'), ('Junio', 'Junio'), ('Julio', 'Julio'), ('Agosto', 'Agosto'),
    ('Septiembre', 'Septiembre'), ('Octubre', 'Octubre'), ('Noviembre', 'Noviembre'), ('Diciembre', 'Diciembre'),
]

class DatosEnsayo(models.Model):
    mes = models.CharField(max_length=20, choices=MESES)
    ensayos = models.PositiveIntegerField(default=0)
    observacionales = models.PositiveIntegerField(default=0)
    adendas = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.mes}: {self.ensayos} Ensayos, {self.observacionales} Obs., {self.adendas} Adendas"
