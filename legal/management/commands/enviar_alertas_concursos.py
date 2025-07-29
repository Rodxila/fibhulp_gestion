from django.core.management.base import BaseCommand
from legal.models import Concurso
from legal.views import evaluar_concurso_para_correo
from django.core.mail import send_mail
from django.utils.timezone import now

class Command(BaseCommand):
    help = 'Envía correos de notificación para concursos según la lógica de alertas'

    def handle(self, *args, **kwargs):
        hoy = now().date()
        enviados = 0

        if hoy.weekday() != 0:
            self.stdout.write(self.style.WARNING('Hoy no es lunes. No se envía nada.'))
            return

        for concurso in Concurso.objects.all():
            print(f"➡️ Revisando concurso: {concurso.EXPEDIENTE}")
            info = evaluar_concurso_para_correo(concurso)

            if not info:
                print("⛔ No se envía correo.")
                continue

            print(f"📤 Enviando correo a: {info['correo']}")
            # Aquí podrías verificar si ya se envió (si implementamos un campo de última notificación)
            send_mail(
                subject=info['asunto'],
                message=info['mensaje'],
                from_email='notificacionesfib@gmail.com',
                recipient_list=[info['correo']],
                fail_silently=False,
            )
            enviados += 1

        self.stdout.write(self.style.SUCCESS(f'{enviados} correos enviados'))


