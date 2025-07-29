from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('legal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Concurso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EXPEDIENTE', models.CharField(max_length=100, db_column='N.º EXPED')),
                ('PROCEDIMIENTO', models.CharField(max_length=255)),
                ('TIPOLOGÍA', models.CharField(max_length=255)),
                ('FECHA_FIRMA', models.CharField(max_length=100, blank=True, null=True)),
                ('DURACIÓN_CONTRATO', models.CharField(max_length=255, blank=True, null=True)),
                ('FECHA_FIN', models.CharField(max_length=100, blank=True, null=True)),
                ('PRORROGA', models.CharField(max_length=255, blank=True, null=True, db_column='¿PRÓRROGAS?')),
                ('FECHA_FIN_PRORROGA', models.CharField(max_length=100, blank=True, null=True)),
                ('CANTIDAD_ECONOMICA_MAX', models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, db_column='CANTIDAD ECONÓMICA MÁX (IVA INCLUIDO)')),
                ('ESTADO', models.CharField(max_length=100, blank=True, null=True)),
                ('ESTADO_CONTINUACION', models.TextField(blank=True, null=True, db_column='ESTADO CONTINUACION')),
            ],
        ),
    ]
