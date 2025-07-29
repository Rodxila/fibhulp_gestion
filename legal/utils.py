from datetime import date
from datetime import datetime

def extraer_fecha(fecha_raw):
    if not fecha_raw:
        return None
    if isinstance(fecha_raw, datetime):
        return fecha_raw.date()
    if isinstance(fecha_raw, str):
        try:
            return datetime.strptime(fecha_raw, "%Y-%m-%d").date()
        except ValueError:
            try:
                return datetime.strptime(fecha_raw, "%d/%m/%Y").date()
            except ValueError:
                return None
    return fecha_raw  # si ya es tipo date


def evaluar_concurso_para_correo(concurso):
    estado = (concurso.ESTADO or '').strip().upper()
    if estado in ['FINALIZADO', 'PARALIZADO', 'CANCELADO', 'DESIERTO Y FINALIZADO', 'EN GESTIÓN']:
        return None

    prorroga = (concurso.PRORROGA or '').strip().lower()
    fecha_objetivo = extraer_fecha(concurso.FECHA_FIN_PRORROGA if 'si' in prorroga else concurso.FECHA_FIN)
    hoy = date.today()

    if not fecha_objetivo:
        return None

    dias_restantes = (fecha_objetivo - hoy).days
    asunto = mensaje = frecuencia = None

    if 'si' in prorroga:
        if 60 < dias_restantes <= 90:
            asunto = "📅 Fin de prórroga cercano"
            mensaje = f"El concurso '{concurso.EXPEDIENTE}' tiene una prórroga que finaliza en {dias_restantes} días."
            frecuencia = "semanal"
        elif 7 < dias_restantes <= 60:
            asunto = "✍️ Se requiere firma de contrato por prórroga"
            mensaje = f"Debe firmarse el contrato del concurso '{concurso.EXPEDIENTE}'. Quedan {dias_restantes} días para el fin de la prórroga."
            frecuencia = "semanal"
        elif 0 < dias_restantes <= 7:
            asunto = "⚠️ URGENTE: Prórroga termina en breve"
            mensaje = f"La prórroga del concurso '{concurso.EXPEDIENTE}' finaliza en menos de una semana."
            frecuencia = "diaria"
    else:
        if 60 < dias_restantes <= 120:
            asunto = "📝 Iniciar redacción del pliego"
            mensaje = f"El contrato '{concurso.EXPEDIENTE}' finaliza en {dias_restantes} días. Debe iniciarse la redacción del pliego."
            frecuencia = "semanal"
        elif 0 < dias_restantes <= 60:
            asunto = "📌 Finalización de contrato próxima"
            mensaje = f"El contrato '{concurso.EXPEDIENTE}' finaliza pronto. Quedan {dias_restantes} días."
            frecuencia = "semanal"

    if asunto and mensaje:
        return {
            'asunto': asunto,
            'mensaje': mensaje,
            'frecuencia': frecuencia,
            'correo': "legal.fib.hlpr@salud.madrid.org"
        }
    return None
