from django.core.management.base import BaseCommand
from ensayos_clinicos.models import FacturaDetalle
from django.core.mail import send_mail
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Envía avisos por correo si una factura no ha sido cobrada en más de 3 meses'

    def handle(self, *args, **kwargs):
        limite = date.today() - timedelta(days=90)

        facturas = FacturaDetalle.objects.filter(fecha_ultimo_cobro__lt=limite)

        if not facturas.exists():
            self.stdout.write(self.style.SUCCESS("✅ No hay facturas atrasadas."))
            return

        lista = "\n".join(
            f"- {f.descripcion} (último cobro: {f.fecha_ultimo_cobro.strftime('%d/%m/%Y')})"
            for f in facturas
        )

        mensaje = f"Las siguientes facturas no han recibido cobro en más de 3 meses:\n\n{lista}"

        send_mail(
            subject="📣 Aviso: Facturas con fecha cobro > 3 meses",
            message=mensaje,
            from_email="notificacionesfib@gmail.com",
            recipient_list=["administracion.fib.hlpr@salud.madrid.org"],  # Personaliza esto
            fail_silently=False,
        )

        self.stdout.write(self.style.SUCCESS("📬 Correo enviado correctamente."))
