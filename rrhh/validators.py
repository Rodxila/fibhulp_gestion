from django.core.exceptions import ValidationError

def validar_tamano_archivo(archivo):
    limite_mb = 5  # Máximo 5 MB por archivo
    if archivo.size > limite_mb * 1024 * 1024:
        raise ValidationError(f"El archivo excede el límite de {limite_mb} MB.")
