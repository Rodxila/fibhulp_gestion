from .forms import SubidaFichaForm
from .forms import FormularioRRHHForm
from .forms import EmpleadoForm
from .models import FormularioContratacion
from ensayos_clinicos.models import Usuario
from ensayos_clinicos.views import restringir_seccion
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
from django.utils.crypto import get_random_string
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import PageBreak
from reportlab.platypus import Image
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader

import os
from io import BytesIO
from weasyprint import HTML
import uuid
from openpyxl import Workbook
from zipfile import ZipFile
import requests
from bs4 import BeautifulSoup
from .utils import obtener_ofertas_disponibles, extraer_datos_oferta_pdf
from rrhh.forms import EmpresaForm

def login_view(request):
    print("Entro en login")
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password_input = request.POST.get('password', '').strip()

        try:
            user = Usuario.objects.get(username=username)

            # Validación dual: hash o texto plano
            password_valida = (
                check_password(password_input, user.password) or
                user.password == password_input
            )

            if not password_valida:
                raise Usuario.DoesNotExist

            request.session['user_id'] = user.id
            request.session['username'] = user.username
            request.session['secciones'] = user.secciones
            return redirect('rrhh:rrhh_inicio')

        except Usuario.DoesNotExist:
            messages.set_level(request, messages.ERROR)
            storage = messages.get_messages(request)
            storage.used = True
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'rrhh/login.html')

def inicio_rrhh(request):
    print("Entro en inicio")
    return render(request, 'rrhh/inicio.html')



def seleccion_view(request):
    print("Entro en seleccion_view")
    return render(request, 'rrhh/seleccion.html')



#@restringir_seccion('3')
#def seleccionar_candidato(request, pk):
#    candidato = get_object_or_404(Candidato, pk=pk)
#
#    if request.method == 'POST':
#        if request.method == 'POST':
#            reenviar = request.POST.get('reenviar', False)
#
#        if candidato.seleccionado and not reenviar:
#            messages.info(request, "Este candidato ya ha sido seleccionado.")
#            return redirect('rrhh:lista_candidatos')
#
#        if not candidato.seleccionado:
#            candidato.seleccionado = True
#            candidato.token_acceso = uuid.uuid4().hex
#            candidato.save()
#

 #       candidato.seleccionado = True
  #      candidato.token_acceso = uuid.uuid4().hex
  #      candidato.save()



  #      ruta_pdf = os.path.join(settings.MEDIA_ROOT, f"ficha_candidato_{candidato.pk}.pdf")
   #     doc = SimpleDocTemplate(ruta_pdf, pagesize=A4)

    #    story = []
     #   styles = getSampleStyleSheet()

        # Logo
      #  logo_path = os.path.join(settings.BASE_DIR, 'rrhh', 'static', 'logo_fib.png')
       # if os.path.exists(logo_path):
        #    from reportlab.platypus import Image
         #   logo = Image(logo_path, width=4*cm, height=2*cm)
          #  logo.hAlign = 'LEFT'
           # story.append(logo)


        # Título
    #    story.append(Spacer(1, 12))
     #   story.append(Paragraph("FICHA DE DATOS PERSONALES", styles['Title']))

        # Campos personales
      #  story.append(Spacer(1, 12))
      #  fields = [
       #     "NOMBRE", "APELLIDOS", "DIRECCIÓN", "POBLACIÓN", "CÓDIGO POSTAL",
        #    "PROVINCIA", "TELÉFONO MÓVIL", "N.I.F. / N.I.E / PASAPORTE", "FECHA NACIMIENTO", "LUGAR",
        #    "E-MAIL personal"
        #]
    #    for field in fields:
    #        story.append(Paragraph(f"{field}: ............................................................", styles['Normal']))

        # Tabla bancaria
     #   story.append(Spacer(1, 12))
     #   story.append(Paragraph("Nº CTA. BANCARIA PARA REALIZAR EL PAGO DE EMOLUMENTOS DERIVADOS DE LA RELACIÓN LABORAL:", styles['Normal']))

      #  headers = ["IBAN (4 dígitos)", "ENTIDAD (4 dígitos)", "OFICINA (4 dígitos)", "D.C. (2 dígitos)", "Nº CUENTA (10 dígitos)"]
       # values = ["................", "................", "................", "................", "................"]
    #    col_widths = [3*cm, 3*cm, 3*cm, 2*cm, 5*cm]

     #   table_data = [headers, values]
     #   table = Table(table_data, colWidths=col_widths)
      #  table.setStyle(TableStyle([
      #      ('GRID', (0,0), (-1,-1), 1, colors.black),
       #     ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
    #        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    #    ]))
     #   story.append(table)

        # Texto adicional
     #   story.append(Spacer(1, 12))
      #  story.append(Paragraph(
      #      "Con el fin de mejorar la comunicación entre La Fundación y sus trabajadores, "
      #      "se autoriza expresamente el uso de la cuenta de e-mail y teléfono indicado para recibir comunicaciones "
       #     "de la fundación (nóminas, certificados, informes, y demás comunicados oficiales). "
    #        "De este modo se agilizará la información.", styles['Normal']
    #    ))

        # Firma y fecha
    #    story.append(Spacer(1, 24))
     #   story.append(Paragraph("FDO: .........................................................     FECHA: .......................................", styles['Normal']))

        # Protección de datos
      #  story.append(Spacer(1, 12))
       # story.append(Paragraph("PROTECCIÓN DE DATOS:", styles['Heading4']))

        #texto1 = (
         #   "En cumplimiento de la normativa de protección de datos aplicable, la Fundación de Investigación "
        #    "Biomédica del Hospital Universitario de la Princesa (en adelante, “la Fundación”) le informa de que "
        #    "tratará los datos de carácter personal que facilite en el presente formulario con la finalidad de gestión "
         #   "administrativa de la Fundación, amparándose esta en su consentimiento al rellenar el presente formulario, "
          #  "o bien en la ejecución del contrato suscrito entre las partes."
        #)

        #texto2 = (
         #   "Sus datos serán conservados durante el tiempo estrictamente necesario, mientras persista la relación jurídica "
          #  "o mientras no se produzca la revocación de su consentimiento, y sin perjuicio del plazo durante el cual los datos "
          #  "deberán conservarse por cumplimiento con las obligaciones legales aplicables a la Fundación. "
          #  "La Fundación no cederá sus datos a terceros, salvo por obligación legal."
        #)

        #texto3 = (
         #   "Usted cuenta con los derechos de acceso, rectificación, supresión, oposición, limitación al tratamiento, "
         #   "portabilidad, así como posibilidad de la revocación del consentimiento otorgado, pudiendo ejercitarlos por escrito "
         #   "dirigiéndose a las oficinas de la Fundación de Investigación Biomédica del Hospital Universitario de la Princesa "
#            "en C/ Diego de León, 62, 28006 Madrid."
#        )

#        texto4 = (
#            "Finalmente, especialmente cuando Usted no haya obtenido satisfacción en el ejercicio de sus derechos, "
#            "tiene derecho a presentar reclamación ante la autoridad nacional de control, a estos efectos debe dirigirse "
##            "a la Agencia Española de Protección de Datos."
#        )
#
#        for texto in [texto1, texto2, texto3, texto4]:
 #           story.append(Paragraph(texto, styles['Normal']))
 #           story.append(Spacer(1, 6))


        # Generar PDF
#        doc.build(story)




#        url_subida_ficha = request.build_absolute_uri(reverse('rrhh:subida_ficha', args=[candidato.token_acceso]))

 #       body = (
  #          f"Adjunto encontrarás la ficha que debes completar y firmar.\n\n"
  #          f"Una vez firmada, por favor súbela aquí:\n{url_subida_ficha}"
  #      )
#
#        try:
###            email = EmailMessage(
 #               subject="¡Enhorabuena! Has sido seleccionado",
  #              body=body,
   #             from_email="notificacionesfib@gmail.com",
    ##            to=[candidato.email],
    #        )
    #        email.attach_file(ruta_pdf)
    #        email.send()
#
#            email.send()
#            messages.success(request, f"Candidato {candidato.nombre} seleccionado con éxito.")
#            return redirect('rrhh:lista_candidatos')
#        except Exception as e:
#            logger.error(f"Error al enviar el correo al candidato {candidato.email}: {e}")
#            messages.error(request, "Ocurrió un error al enviar el correo electrónico al candidato.")
 #           return redirect('rrhh:lista_candidatos')



@restringir_seccion('3')
def seleccionar_candidato(request, pk):
    print("Entro en seleccionar candidato")
    candidato = get_object_or_404(FormularioContratacion, pk=pk)

    if request.method == 'POST':
        reenviar = request.POST.get('reenviar', False)

        if candidato.seleccionado and not reenviar:
            messages.info(request, "Este candidato ya ha sido seleccionado.")
            return redirect('rrhh:lista_candidatos')

        candidato.seleccionado = True
        candidato.token_acceso = str(uuid.uuid4())
        candidato.save()

        # Generar PDF con ReportLab
        ruta_pdf = os.path.join(settings.MEDIA_ROOT, f"ficha_candidato_{candidato.pk}.pdf")
        doc = SimpleDocTemplate(ruta_pdf, pagesize=A4)

        story = []
        styles = getSampleStyleSheet()

        styles.add(ParagraphStyle(name='SmallNormal', parent=styles['Normal'], fontSize=9, leading=11))
        styles.add(ParagraphStyle(name='SmallTitle', parent=styles['Title'], fontSize=12, leading=14))
        styles.add(ParagraphStyle(name='SmallHeading4', parent=styles['Heading4'], fontSize=10, leading=12))

        logo_path = os.path.join(settings.BASE_DIR, 'rrhh', 'static', 'logo_fib.png')
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=4*cm, height=2*cm)
            logo.hAlign = 'LEFT'
            story.append(logo)

        story.append(Spacer(1, 12))
        story.append(Paragraph("FICHA DE DATOS PERSONALES", styles['Title']))
        story.append(Spacer(1, 12))

        campos = [
            "NOMBRE", "APELLIDOS", "DIRECCIÓN", "POBLACIÓN", "CÓDIGO POSTAL",
            "PROVINCIA", "TELÉFONO MÓVIL", "N.I.F. / N.I.E / PASAPORTE", "FECHA NACIMIENTO", "LUGAR",
            "E-MAIL personal"
        ]
        for campo in campos:
            story.append(Paragraph(f"{campo}: ............................................................", styles['SmallNormal']))

        story.append(Spacer(1, 12))
        story.append(Paragraph("Nº CTA. BANCARIA PARA REALIZAR EL PAGO DE EMOLUMENTOS DERIVADOS DE LA RELACIÓN LABORAL:", styles['SmallNormal']))

        headers = [
            Paragraph("IBAN (4 dígitos)", ParagraphStyle(name="TableHeader", fontSize=8)),
            Paragraph("ENTIDAD (4 dígitos)", ParagraphStyle(name="TableHeader", fontSize=8)),
            Paragraph("OFICINA (4 dígitos)", ParagraphStyle(name="TableHeader", fontSize=8)),
            Paragraph("D.C. (2 dígitos)", ParagraphStyle(name="TableHeader", fontSize=8)),
            Paragraph("Nº CUENTA (10 dígitos)", ParagraphStyle(name="TableHeader", fontSize=8)),
        ]
        values = ["................", "................", "................", "................", "................"]
        col_widths = [3*cm, 3*cm, 3*cm, 2*cm, 5*cm]

        table = Table([headers, values], colWidths=col_widths)
        table.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ]))
        story.append(table)

        story.append(Spacer(1, 12))
        story.append(Paragraph(
            "Con el fin de mejorar la comunicación entre La Fundación y sus trabajadores, "
            "se autoriza expresamente el uso de la cuenta de e-mail y teléfono indicado para recibir comunicaciones "
            "de la fundación (nóminas, certificados, informes, y demás comunicados oficiales). "
            "De este modo se agilizará la información.", styles['Normal']
        ))

        story.append(Spacer(1, 24))
        story.append(Paragraph("FDO: .........................................................     FECHA: .......................................", styles['Normal']))

        story.append(Spacer(1, 12))
        story.append(Paragraph("PROTECCIÓN DE DATOS:", styles['Heading4']))

        textos = [
            "En cumplimiento de la normativa de protección de datos aplicable, la Fundación de Investigación "
            "Biomédica del Hospital Universitario de la Princesa (en adelante, “la Fundación”) le informa de que "
            "tratará los datos de carácter personal que facilite en el presente formulario con la finalidad de gestión "
            "administrativa de la Fundación, amparándose esta en su consentimiento al rellenar el presente formulario, "
            "o bien en la ejecución del contrato suscrito entre las partes.",

            "Sus datos serán conservados durante el tiempo estrictamente necesario, mientras persista la relación jurídica "
            "o mientras no se produzca la revocación de su consentimiento, y sin perjuicio del plazo durante el cual los datos "
            "deberán conservarse por cumplimiento con las obligaciones legales aplicables a la Fundación. "
            "La Fundación no cederá sus datos a terceros, salvo por obligación legal.",

            "Usted cuenta con los derechos de acceso, rectificación, supresión, oposición, limitación al tratamiento, "
            "portabilidad, así como posibilidad de la revocación del consentimiento otorgado, pudiendo ejercitarlos por escrito "
            "dirigiéndose a las oficinas de la Fundación de Investigación Biomédica del Hospital Universitario de la Princesa "
            "en C/ Diego de León, 62, 28006 Madrid.",

            "Finalmente, especialmente cuando Usted no haya obtenido satisfacción en el ejercicio de sus derechos, "
            "tiene derecho a presentar reclamación ante la autoridad nacional de control, a estos efectos debe dirigirse "
            "a la Agencia Española de Protección de Datos."
        ]

        for txt in textos:
            story.append(Paragraph(txt, styles['Normal']))
            story.append(Spacer(1, 6))

        doc.build(story)

        # Enlace para subir la ficha y documentos
        url_subida_ficha = request.build_absolute_uri(reverse('rrhh:subida_ficha', args=[candidato.token_acceso]))
        body = (
            f"Adjunto encontrarás la ficha que debes completar y firmar.\n\n"
            f"Una vez firmada, por favor súbela junto con la documentación adicional solicitada (vida laboral, titulaciones, etc.) "
            f"en el siguiente enlace:\n{url_subida_ficha}\n\n"
            "Gracias por tu colaboración."
        )

        try:
            email = EmailMessage(
                subject="¡Enhorabuena! Has sido seleccionado",
                body=body,
                from_email="notificacionesfib@gmail.com",
                to=[candidato.email],
            )
            email.attach_file(ruta_pdf)
            email.send()
            messages.success(request, f"Candidato {candidato.nombre} seleccionado con éxito.")
            return redirect('rrhh:lista_candidatos')
        except Exception as e:
            logger.error(f"Error al enviar el correo al candidato {candidato.email}: {e}")
            messages.error(request, "Ocurrió un error al enviar el correo electrónico al candidato.")
            return redirect('rrhh:lista_candidatos')


def clean(self):
    cleaned_data = super().clean()

    requeridos = [
        ('inscrito_sepe', 'fotocopia_tarjeta_inem'),
        ('soporte_documental_meritos', 'soporte_documental_meritos'),  # Si añades un campo tipo booleano aquí, lo ligas
        ('discapacitado', 'soporte_documental_meritos'),
        ('excluido_social', 'soporte_documental_meritos'),
        ('victima_violencia_domestica', 'soporte_documental_meritos'),
        ('mujer_reincorporada', 'soporte_documental_meritos'),
        ('capacidad_intelectual_limite', 'soporte_documental_meritos'),
        ('contrato_temporal_6m_fibh', 'soporte_documental_meritos'),
        ('contrato_indefinido_12m_fibh', 'soporte_documental_meritos'),
        ('contrato_indefinido_3m_otra_empresa', 'soporte_documental_meritos'),
    ]

    for campo_checkbox, campo_justificante in requeridos:
        if cleaned_data.get(campo_checkbox) and not cleaned_data.get(campo_justificante):
            self.add_error(campo_justificante, "Debe subir un documento justificativo para esta bonificación.")





@restringir_seccion('3')
def descartar_candidato(request, pk):
    print("Entro en descartar_candidato")
    formulario = get_object_or_404(FormularioContratacion, pk=pk)

    if request.method == 'POST':
        if formulario.cv:
            formulario.cv.delete(save=False)
        formulario.delete()
        messages.success(request, "Formulario de candidato eliminado correctamente.")
        return redirect('rrhh:lista_candidatos')


@restringir_seccion('3')
def contratacion_view(request):
    print("Entro en contratacion_view")
    usuario = request.session.get('username')
    if not usuario:
        messages.error(request, "Debe iniciar sesión.")
        return redirect('rrhh:login_view')  # Asegúrate de tener esta vista

    datos_usuario = Usuario.objects.filter(username=usuario).first()

    if not datos_usuario:
        messages.error(request, "Usuario no válido.")
        print(usuario)
        return redirect('rrhh:login_view')

    es_rrhh = datos_usuario.secciones == '3'
    es_empleado = datos_usuario.secciones == '4'

    if es_rrhh:
        contrataciones = FormularioContratacion.objects.all()
        return render(request, 'rrhh/contratacion_rrhh.html', {'contrataciones': contrataciones})

    elif es_empleado:
        contratacion = get_object_or_404(FormularioContratacion, empleado=usuario)
        if contratacion.rellenado_por_empleado:
            messages.info(request, "Ya ha completado su parte del formulario.")
            return redirect('rrhh:login_view')
        if request.method == 'POST':
            form = EmpleadoForm(request.POST, request.FILES, instance=contratacion)
            if form.is_valid():
                instancia = form.save(commit=False)
                instancia.rellenado_por_empleado = True
                instancia.save()
                messages.success(request, "Formulario enviado correctamente.")
                return redirect('rrhh:login_view')
        else:
            form = EmpleadoForm(instance=contratacion)
        return render(request, 'rrhh/formulario_empleado.html', {'form': form})

    else:
        messages.error(request, "No tiene permisos para acceder a esta sección.")
        return redirect('rrhh:login_view')






def nominas_view(request):
    print("Entro en nominas_views")
    return render(request, 'rrhh/nominas.html')


def rrhh_home(request):
    print("Entro en rrhh_home")
    if request.session.get('secciones') != '3':
        return redirect('rrhh:login_view')

    # renderiza la página principal con tabla de empleados y botón de crear nuevo
    return render(request, 'rrhh/rrhh_home.html')

def formulario_empleado(request, pk):
    print("Entro en formulario_empleado")
    secciones = request.session.get('secciones', '')
    if '4' not in secciones and '3' not in secciones:
        messages.error(request, "No tienes permisos para ver este formulario.")
        return redirect('rrhh:login_view')

    formulario = get_object_or_404(FormularioContratacion, pk=pk)

    # ⚠ Validación de acceso:
    usuario = Usuario.objects.filter(id=request.session.get('user_id')).first()
    if not usuario:
        messages.error(request, "Sesión no válida.")
        return redirect('rrhh:login_view')

    if '4' in usuario.secciones and formulario.empleado != usuario:
        messages.error(request, "No tienes permiso para ver este formulario.")
        return redirect('rrhh:login_view')

    if formulario.rellenado_por_empleado and '4' in usuario.secciones:
        messages.info(request, "Ya has completado el formulario.")
        return redirect('rrhh:login_view')

    if request.method == 'POST':
        form = EmpleadoForm(request.POST, request.FILES, instance=formulario)
        if form.is_valid():
            instance = form.save(commit=False)
            if '4' in usuario.secciones:
                instance.rellenado_por_empleado = True
            instance.save()
            messages.success(request, "Formulario enviado correctamente.")
            return redirect('rrhh:login_view' if '4' in usuario.secciones else 'rrhh:rrhh_contratacion')
    else:
        form = EmpleadoForm(instance=formulario)

    context = {
        'form': form,
        'campos_id': ['nif', 'nie', 'carta_identidad', 'pasaporte']
    }
    return render(request, 'rrhh/formulario_empleado.html', context)






@restringir_seccion('3')
def formulario_empresa(request, pk):
    print("entro al formulario_empresa")
    formulario = get_object_or_404(FormularioContratacion, pk=pk)

    campos_trabajador = [
        'nombre', 'apellidos', 'direccion_completa', 'poblacion', 'provincia',
        'codigo_postal', 'nacionalidad', 'telefono', 'email', 'fecha_nacimiento',
        'sexo', 'nif', 'nie', 'carta_identidad', 'pasaporte'
    ]

    campos_documentos = [
        'fotocopia_tarjeta_inem',
        'soporte_documental_meritos',
        'certificado_titularidad_bancaria',
        'certificado_delitos_sexuales',
        'cv',
        'vida_laboral',
        'fotocopia_master_doctorado'
    ]


    campos_rrhh = [
        'nivel_estudios', 'especialidad', 'inscrito_sepe', 'mayor_30_sepe',
        'discapacitado', 'excluido_social', 'victima_violencia_domestica',
        'mujer_reincorporada', 'capacidad_intelectual_limite',
        'contrato_temporal_6m_fibh', 'contrato_indefinido_12m_fibh',
        'contrato_indefinido_3m_otra_empresa', 'tipo_contrato',
        'contrato_duracion', 'causa_contrato', 'titulacion_practicas',
        'fecha_obtencion_titulacion', 'jornada', 'horas_semana',
        'distribucion_jornada', 'convocatoria', 'categoria_area',
        'categoria_grupo', 'categoria_profesional', 'prestara_servicios_como',
        'tipo_personal', 'funciones', 'logos', 'clausulas_adicionales',
        'objeto_contrato', 'financiacion', 'aplica_tablas_convenio',
        'salario_base', 'carrera_profesional', 'complementos', 'salario_fijo',
        'coste_fijado_convocatoria', 'importe_coste_empresa_anual',
        'requiere_autorizacion_hacienda'
    ]


    if formulario.rellenado_por_empresa and request.method != 'POST':
        messages.info(request, "Este formulario ya ha sido completado.")


    if request.method == 'POST':
        form = EmpresaForm(request.POST, request.FILES, instance=formulario)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.rellenado_por_empresa = True
            instance.save()
            messages.success(request, "Formulario completado con éxito.")
            return descargar_documentacion(request, formulario.pk)
        else:
            print("FORMULARIO NO VÁLIDO")
            print(form.errors.as_json())
    else:
        form = EmpresaForm(instance=formulario)

    print(type(campos_trabajador), campos_trabajador)
    print(type(campos_documentos), campos_documentos)
    print(type(campos_rrhh), campos_rrhh)

    return render(request, 'rrhh/formulario_empresa.html', {
        'form': form,
        'campos_trabajador': campos_trabajador,
        'campos_documentos': campos_documentos,
        'campos_rrhh': campos_rrhh
    })



@restringir_seccion('3')
def eliminar_formulario(request, pk):
    print("Entro en eliminar_formulario")
    formulario = get_object_or_404(FormularioContratacion, pk=pk)

    # Eliminar archivos asociados
    campos_archivos = [
        'fotocopia_tarjeta_inem',
        'soporte_documental_meritos',
        'certificado_titularidad_bancaria',
        'certificado_delitos_sexuales',
        'cv',
        'vida_laboral',
        'fotocopia_master_doctorado',
        'ficha_firmada',
        'logos'
    ]

    for campo in campos_archivos:
        archivo = getattr(formulario, campo, None)
        if archivo and hasattr(archivo, 'path') and os.path.exists(archivo.path):
            os.remove(archivo.path)

    # Finalmente eliminar el objeto del formulario
    formulario.delete()

    messages.success(request, "Formulario y archivos eliminados correctamente.")
    return redirect('rrhh:rrhh_contratacion')


# views.py


import logging

logger = logging.getLogger(__name__)  # Por si quieres registrar en logs


# utils.py (u otro sitio compartido)
logos_extraidos_temporales = {}  # Diccionario global: {formulario.pk: [tuplas de imágenes]}

def seleccion_personal(request):
    print("Entro en seleccion_personal")
    ofertas = obtener_ofertas_disponibles()
    print("[DEBUG] Ofertas obtenidas:", ofertas)

    if request.method == 'POST':
        form = EmpleadoForm(request.POST, request.FILES, ofertas_disponibles=ofertas)
        if form.is_valid():
            formulario = form.save()

            referencia_seleccionada = formulario.convocatoria.split("(")[-1].replace(")", "").strip()
            print("Referencia seleccionada:", referencia_seleccionada)

            oferta_seleccionada = next(
                (oferta for oferta in ofertas if oferta[1] == referencia_seleccionada),
                None
            )

            formulario.proceso_codigo = referencia_seleccionada

            if oferta_seleccionada:
                documento_pdf = oferta_seleccionada.get("documento")
                if documento_pdf and documento_pdf.lower().endswith(".pdf"):
                    try:
                        datos_pdf = extraer_datos_oferta_pdf(documento_pdf)
                        formulario.ip = datos_pdf.get("ip")
                        formulario.funciones = datos_pdf.get("funciones")
                        formulario.prestara_servicios_como = datos_pdf.get("puesto")
                        formulario.save()
                        logos = datos_pdf.get("logos", [])
                        logos_extraidos_temporales[formulario.pk] = logos

                        print("[🧠] IP extraído:", formulario.ip)
                        print("[🛠️] Funciones extraídas:\n", formulario.funciones)
                        print(f"[🖼️] Logos extraídos: {len(logos)}")

                    except Exception as e:
                        logger.warning(f"[❌] Error al procesar el PDF: {e}")
                        print("[❌] No se pudo extraer datos del PDF")
                else:
                    print("[⚠️] La oferta sí existe, pero no tiene documento PDF válido.")
            else:
                print(f"[⚠️] Oferta con código {referencia_seleccionada} no disponible (probablemente caducada)")

            # Enviar correo de confirmación
            send_mail(
                subject='Gracias por tu postulación',
                message=f"Hola {formulario.nombre}, gracias por postularte a la oferta: {formulario.convocatoria}.",
                from_email='notificacionesfib@gmail.com',
                recipient_list=[formulario.email],
            )

            messages.success(request, "Tu postulación se ha enviado correctamente.")
            return redirect('rrhh:seleccion_view')

    else:
        form = EmpleadoForm(ofertas_disponibles=ofertas)

    return render(request, 'rrhh/seleccion_form.html', {'form': form})

@restringir_seccion('3')
def lista_candidatos(request):
    print("Entro en lista_candidatos")
    candidatos = FormularioContratacion.objects.all().order_by('-creado')
    return render(request, 'rrhh/candidatos_list.html', {'candidatos': candidatos})


@restringir_seccion('3')
def exportar_candidatos_excel(request):
    print("Entro en exportar_candidatos_excel")
    wb = Workbook()
    ws = wb.active
    ws.title = "Candidatos"

    ws.append(['Nombre', 'Apellidos', 'Email', 'Fecha'])

    for c in FormularioContratacion.objects.filter(rellenado_por_empleado=True):
        ws.append([
            c.nombre,
            c.apellidos,
            c.email,
            c.creado.strftime("%Y-%m-%d %H:%M") if c.creado else ""
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="candidatos.xlsx"'
    wb.save(response)
    return response

@csrf_exempt
def subida_ficha(request, token):
    print("Entro en subida_ficha")
    formulario = get_object_or_404(FormularioContratacion, token_acceso=token)

    mensaje_exito = None

    if request.method == 'POST':
        form = SubidaFichaForm(request.POST, request.FILES, instance=formulario)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.rellenado_por_empleado = True
            instancia.save()

            mensaje_exito = "¡Datos y documentos subidos correctamente!"

            send_mail(
                subject="Documentación completa recibida",
                message=f"El candidato {instancia.nombre} {instancia.apellidos} ha completado su parte del formulario.",
                from_email="notificacionesfib@gmail.com",
                recipient_list=["rodrigo.martinez.externo@salud.madrid.org"],
            )
    else:
        form = SubidaFichaForm(instance=formulario)

    return render(request, 'rrhh/subida_ficha.html', {
        'form': form,
        'candidato': formulario,  # el objeto formulario ya contiene nombre/apellidos/email
        'mensaje_exito': mensaje_exito,
    })


def editar_datos_rrhh(request, pk):
    print("Entro en editar datos")
    formulario = get_object_or_404(FormularioContratacion, pk=pk)

    if request.method == 'POST':
        print("Entro en editar datos 1")
        form = FormularioRRHHForm(request.POST, instance=formulario)
        try:
            if form.is_valid():
                print("Entro en editar datos 2")
                dia_inicio = form.cleaned_data.get('jornada_dia_inicio')
                dia_fin = form.cleaned_data.get('jornada_dia_fin')
                hora_inicio = form.cleaned_data.get('jornada_hora_inicio')
                hora_fin = form.cleaned_data.get('jornada_hora_fin')

                frase_distribucion = f"De {dia_inicio} a {dia_fin}, en horario de {hora_inicio}h a {hora_fin}h"
                formulario.distribucion_jornada = frase_distribucion
                formulario.save()
                form.save()
                print(f"DEBUG — Redirigiendo con pk={formulario.pk} (tipo: {type(formulario.pk)})")
                print("Datos del formulario:", form.cleaned_data)
                return descargar_documentacion(request, pk=formulario.pk)
            else:
                print("Entro en editar datos 3")
                print("Errores del formulario:")
                for field, errors in form.errors.items():
                    for error in errors:
                        print(f" - {field}: {error}")
        except Exception as e:
            print("EXCEPCIÓN EN VALIDACIÓN:", e)
    else:
        form = FormularioRRHHForm(instance=formulario)
        print("Entro en editar datos 4")

    return render(request, 'rrhh/formulario_rrhh.html', {'form': form, 'formulario': formulario})



def descargar_documentacion(request, pk):
    print(">>> ENTRANDO EN descargar_documentacion")
    formulario = get_object_or_404(FormularioContratacion, pk=pk)
    print(f">>> Formulario cargado: {formulario.nombre} ({formulario.pk})")
    zip_buffer = BytesIO()

    with ZipFile(zip_buffer, 'w') as zip_file:
        print(">>> Añadiendo archivos al ZIP...")
        # Archivos subidos
        campos_archivo = [
            ('ficha_firmada', 'Ficha_firmada'),
            ('vida_laboral', 'Vida_laboral'),
            ('certificado_penales', 'Certificado_penales'),
            ('titulacion', 'Titulacion'),
            ('cv', 'cv'),
            ('certificado_titularidad_bancaria', 'Titularidad_bancaria'),
            ('fotocopia_tarjeta_inem', 'Tarjeta_INEM'),
            ('fotocopia_master_doctorado', 'Master_Doctorado'),
            ('soporte_documental_meritos', 'Meritos'),

            # Archivos opcionales por checkbox
            ('documento_inscrito_sepe', 'Doc_Inscrito_SEPE'),
            ('documento_mayor_30_sepe', 'Doc_Mayor30_SEPE'),
            ('documento_discapacitado', 'Doc_Discapacidad'),
            ('documento_excluido_social', 'Doc_Exclusion_Social'),
            ('documento_victima_violencia_domestica', 'Doc_Violencia_Domestica'),
            ('documento_mujer_reincorporada', 'Doc_Mujer_Reincorporada'),
            ('documento_capacidad_intelectual_limite', 'Doc_Capacidad_Limite'),
            ('documento_contrato_temporal_6m_fibh', 'Doc_Contrato_Temporal_FIB'),
            ('documento_contrato_indefinido_12m_fibh', 'Doc_Contrato_12m_FIB'),
            ('documento_contrato_indefinido_3m_otra_empresa', 'Doc_Contrato_3m_OtraEmpresa'),
        ]


        for campo, nombre_archivo in campos_archivo:
            archivo = getattr(formulario, campo, None)
            if archivo and hasattr(archivo, 'path') and archivo.path:
                print(f">>> Añadiendo archivo: {campo} => {archivo.path}")
                zip_file.write(archivo.path, f"{nombre_archivo}_{formulario.nombre}.pdf")
            else:
                print(f">>> No se encontró archivo para: {campo}")

        # Agrega la ficha personalizada generada
        ficha_pdf = generar_ficha_pdf_tablas(formulario)
        print(">>> Ficha generada, añadiéndola al ZIP")
        zip_file.writestr(f"Ficha_Completa_{formulario.nombre}.pdf", ficha_pdf.getvalue())

    zip_buffer.seek(0)
    print(">>> ZIP preparado, devolviendo respuesta")
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename=documentacion_{formulario.nombre}.zip'
    return response

def parrafo_multilinea(c, texto, x, y, max_width=16*cm):
    print("Entro en parrafo_multilinea")

    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]

    p = Paragraph(texto, normal_style)
    w, h = p.wrap(max_width, 1000)
    p.drawOn(c, x, y - h)
    return h

from reportlab.platypus import Image as RLImage

def convertir_logos_a_rlimages(logos, max_height=40):
    print("Entro en convertir_logos_a_rlimages")
    """
    Convierte una lista de tuplas (ext, PIL.Image) en objetos Image de ReportLab.

    :param logos: Lista de tuplas (ext, PIL.Image) extraídas del PDF con PyMuPDF.
    :param max_height: Altura máxima deseada para los logos en puntos (default=40).
    :return: Lista de objetos reportlab.platypus.Image
    """
    rl_images = []
    for ext, pil_image in logos:
        # Escalado proporcional
        ratio = max_height / pil_image.height
        new_width = int(pil_image.width * ratio)
        resized_image = pil_image.resize((new_width, max_height))

        img_buffer = BytesIO()
        resized_image.save(img_buffer, format='PNG')
        img_buffer.seek(0)

        rl_img = RLImage(img_buffer, width=new_width, height=max_height)
        rl_images.append(rl_img)

    return rl_images




def generar_ficha_pdf_tablas(formulario):
    print("Entro en generar_ficha_pdf_tablas")
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=20, leftMargin=20, topMargin=10, bottomMargin=10)
    elements = []

    ofertas = obtener_ofertas_disponibles()
    oferta_seleccionada = next(
        (oferta for oferta in ofertas if oferta[1] == formulario.proceso_codigo),
        None
    )
    logos = []
    if oferta_seleccionada:
        datos_pdf = extraer_datos_oferta_pdf(oferta_seleccionada.get("documento"))
        logos = datos_pdf.get("logos", [])
        print(f"[🧠] Logos reextraídos: {len(logos)}")
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'static/fonts/DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'static/fonts/DejaVuSans-Bold.ttf'))
    normal = ParagraphStyle(name='Normal', fontName='DejaVuSans', fontSize=9, spaceAfter=5)
    bold = ParagraphStyle(name='Bold', parent=normal, fontName='DejaVuSans-Bold', fontSize=9)


    styles = getSampleStyleSheet()

    # Estilo rojo y centrado para el título principal
    estilo_titulo_rojo = ParagraphStyle(
        name='TituloRojo',
        parent=styles['Normal'],
        fontName='DejaVuSans-Bold',
        fontSize=12,
        alignment=1,  # centrado
        spaceAfter=6
    )

    # Fila superior: 3 columnas
    fila_superior = [
        [
            Paragraph(f"<b>Proceso:</b> {formulario.proceso_codigo or ''}<br/><br/><b>Alta:</b> {formulario.alta or ''}", normal),
            Paragraph("FICHA PERSONAL FIB LA PRINCESA", estilo_titulo_rojo),
            Paragraph("<b>Baja:</b><br/><br/><b>Causa:</b>", normal)
        ]
    ]

    tabla_encabezado = Table(fila_superior, colWidths=[150, 250, 150])
    tabla_encabezado.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.8, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
    ]))

    # Fila inferior: Fecha de Alta (1 celda grande)
    fila_fecha = [[Paragraph("<b>Fecha de Alta:</b>", normal)]]
    tabla_fecha = Table(fila_fecha, colWidths=[550])
    tabla_fecha.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.8, colors.black),
    ]))

    # Añadir al documento
    elements.append(tabla_encabezado)
    elements.append(Spacer(1, 4))
    elements.append(tabla_fecha)
    elements.append(Spacer(1, 12))


    # ===== BLOQUE 1. TRABAJADOR =====
    elements.append(Paragraph("<b>1. TRABAJADOR</b>", bold))
    elements.append(Spacer(0.5, 6))

    def c(label, val):  # Crea celda con etiqueta + valor
        return Paragraph(f"<b>{label}</b> {val or ''}", normal)

    def checkbox(valor):
        return "☑" if valor else "☐"

    print("Contrato temporal 6m FIB:", formulario.contrato_temporal_6m_fibh)

    # Lista de filas con estructura fija: (contenido, colWidths, optional span)
    filas_configuradas = [
        # 0. Apellidos y Nombre (2 columnas)
        ([c("Apellidos:", formulario.apellidos), c("Nombre:", formulario.nombre)], [275, 275]),

        # 1. Fecha nacimiento, NIF, Nacionalidad (3 columnas)
        ([c("Fecha Nacimiento:", formulario.fecha_nacimiento),
          c("NIF/NIE (1):", formulario.nif),
          c("Nacionalidad:", formulario.nacionalidad)], [180, 180, 190]),

        # 2. Identidad: 3 campos
        ([c("Para los casos que no tengan NIF ó NIE:", ''),
          c("Carta Identidad:", formulario.carta_identidad),
          c("Pasaporte:", formulario.pasaporte)], [180, 180, 190]),

        # 3. Nº Seguridad Social (una sola celda, que ocupe toda la tabla)
        ([c("Nº Afil. Seguridad Social (2):", '')], [550]),

        # 4. Estudios y Especialidad (2 columnas)
        ([c("Nivel de estudios:", formulario.nivel_estudios),
          c("Especialidad:", formulario.especialidad)], [275, 275]),

        # 5. Domicilio completo (1 columna)
        ([c("Domicilio Completo Actual:", formulario.direccion_completa)], [550]),

        # 6. Población, Provincia, CP (3 columnas)
        ([c("Población:", formulario.poblacion),
          c("Provincia:", formulario.provincia),
          c("C. Postal:", formulario.codigo_postal)], [183, 183, 184]),

        # 7. Teléfono y Email (2 columnas)
        ([c("Teléfonos:", formulario.telefono),
          c("e-mail:", formulario.email)], [275, 275]),

        # 8. IBAN (1 celda)
        ([c("Domiciliación Cuenta Bancaria (IBAN):", '')], [550]),

        # 9. SEPE (2 columnas)
        ([c(f"{checkbox(formulario.inscrito_sepe)} Inscrito en el SEPE", ""),
          c(f"{checkbox(formulario.mayor_30_sepe)} EDAD <30 inscrito en el SEPE", "")], [275, 275]),

        # 10. Discapacidad, Exclusión, Violencia (3 columnas)
        ([c(f"{checkbox(formulario.discapacitado)} Discapacitado => 33%. Grado:", ""),
          c(f"{checkbox(formulario.excluido_social)} Excluido Social", ""),
          c(f"{checkbox(formulario.victima_violencia_domestica)} Victima Violencia Doméstica", "")], [183, 183, 184]),

        # 11. Mujer reincorporada y Capacidad Intelectual (2 columnas)
        ([c(f"{checkbox(formulario.mujer_reincorporada)} Mujer reincorporada en 2 años siguientes al parto.", ""),
          c(f"{checkbox(formulario.capacidad_intelectual_limite)} Capacidad Intelectual Límite", "")], [275, 275]),

        # 12. Contrato 6 meses FIB
        ([c(f"{checkbox(formulario.contrato_temporal_6m_fibh)} Contrato temporal o formativo en los 6 meses anteriores con la FIB", "")], [550]),

        # 13. Contrato 12 meses FIB
        ([c(f"{checkbox(formulario.contrato_indefinido_12m_fibh)} Contrato indefinido en los 12 meses anteriores con la FIB", "")], [550]),

        # 14. Contrato 3 meses otra empresa
        ([c(f"{checkbox(formulario.contrato_indefinido_3m_otra_empresa)} Contrato indefinido bonificado en los 3 meses anteriores con otra empresa", "")], [550]),

        # 15. Nota final en cursiva
        ([c("<i>La marca de cualquiera de estas casillas no supone el derecho a la aplicación de bonificaciones, esta quedará supeditada a la concesión de la misma por parte de la Tesorería General de la Seguridad Social.</i>", styles['Italic'])], [550]),
    ]

    # Añadir tablas una a una
    for fila, widths in filas_configuradas:
        tabla_fila = Table([fila], colWidths=widths)
        tabla_fila.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ]))
        elements.append(tabla_fila)


   # -------- CENTRO DE TRABAJO --------
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("<b>2. CENTRO DE TRABAJO</b>", bold))
    elements.append(Spacer(1, 6))
    # Diccionario para asignar C.P. según la dirección
    cp_por_direccion = {
        "CL Diego de León 62": "28006",  # H. Princesa
        "CL del Maestro Vives, 2": "28009",  # H. Santa Cristina
        "Av. de Menéndez Pelayo, 65": "28009",  # H. Niño Jesús
    }

    codigo_postal_centro = cp_por_direccion.get(formulario.direccion_centro, "")

    # Fila 1: Nombre y Dirección (2 columnas iguales)
    fila1 = [c("Nombre FIB:", "FIBHLPR"), c("Dirección:", formulario.direccion_centro)]
    tabla_f1 = Table([fila1], colWidths=[275, 275])
    tabla_f1.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))
    elements.append(tabla_f1)

    # Fila 2: CCC (una celda completa)
    fila2 = [c("CCC:", "28/146742301")]
    tabla_f2 = Table([fila2], colWidths=[550])
    tabla_f2.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))
    elements.append(tabla_f2)

    # Fila 3: 4 columnas (25% cada una)
    fila3 = [
        c("Población:", "MADRID"),
        c("C.P.:", codigo_postal_centro),
        c("I. P.:", formulario.ip),
        c("Convocatoria nº:", "")
    ]
    tabla_f3 = Table([fila3], colWidths=[137.5, 137.5, 137.5, 137.5])
    tabla_f3.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))
    elements.append(tabla_f3)
    elements.append(Spacer(1, 6))
    # ------------ 3. TIPO DE CONTRATO ---------
    elements.append(Paragraph("<b>3. TIPO DE CONTRATO</b>", bold))
    elements.append(Spacer(1, 6))
    def construir_tabla_tipo_contrato(formulario):
        tipo = formulario.tipo_contrato or ''
        causa = formulario.causa_contrato or ''
        titulacion = formulario.titulacion_y_fecha or ''
        jornada = formulario.jornada or ''
        horas = formulario.horas_semana or ''
        distrib = formulario.distribucion_jornada or ''
        duracion = formulario.duracion or ''

        def checkbox(valor):
            return "☑" if valor else "☐"

        # Bloque de contratos (izquierda)
        contenido_tipo_contrato = Paragraph(
            f"""
            <b>Indefinido:</b><br/>
            {checkbox(tipo == 'indefinido_ordinario')} Indefinido ordinario<br/>
            {checkbox(tipo == 'indefinido_actividad_cientifica')} Indefinido de Actividades Científico-Técnicas. (Rellenar Apartado 3.B)<br/>
            {checkbox(tipo == 'indefinido_transformacion')} Transformación Indefinido de Actividades Científico-Técnicas. (Rellenar Apartado 3.B)<br/><br/>

            <b>Temporal:</b><br/>
            {checkbox(tipo == 'temporal_fondos_europeos')} Vinculado a programa financiado con Fondos Europeos NO competitivos<br/>
            {checkbox(tipo == 'temporal_prtr')} Plan de Recuperación, transformación y resiliencia (PRTR)<br/>
            <b>Circunstancias de la Producción:</b><br/>
            {checkbox(tipo == 'temporal_produccion_imprevisible')} Imprevisible (máx. 6 meses) → Causa: {causa if tipo == 'temporal_produccion_imprevisible' else ''}<br/>
            {checkbox(tipo == 'temporal_produccion_previsible')} Previsible (máx. empresa 90 días/año) → Causa: {causa if tipo == 'temporal_produccion_previsible' else ''}<br/>
            {checkbox(tipo == 'temporal_interinidad')} Interinidad → Causa: {causa if tipo == 'temporal_interinidad' else ''}<br/>
            {checkbox(tipo == 'temporal_practicas')} Prácticas → Titulación y fecha: {titulacion if tipo == 'temporal_practicas' else ''}<br/>
            {checkbox(tipo == 'pre_doc')} PREDOC en formación<br/>
            {checkbox(tipo == 'postdoc')} De acceso a SECTI (postdoc)<br/>
            {checkbox(tipo == 'distinguido')} De investigador distinguido<br/>
            """,
            normal
        )

        # Bloque de duración (derecha)
        contenido_duracion = Paragraph(
            f"Duración del contrato:<br/>{f'{duracion} meses' if duracion else ''}",
            normal
        )
        tabla_contrato = Table(
            [[contenido_tipo_contrato, contenido_duracion]],
            colWidths=[400, 150]
        )
        tabla_contrato.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))

        # Bloque de jornada en fila aparte

        contenido_jornada_izquierda = Paragraph(
            f"""
            <b>Jornada:</b><br/>
            {checkbox(jornada == 'Completa')} Completa<br/>
            {checkbox(jornada == 'Parcial')} Parcial*
            """,
            normal
        )

        # Parte derecha (solo aparece si es parcial)
        contenido_jornada_derecha = Paragraph(
            f"""
            <font size="8">*Si es a tiempo parcial es obligatorio detallar la parcialidad y el horario en que prestara sus servicios el trabajador</font><br/>
            Nº Horas: {horas or '______'} a la semana.<br/>
            Distribución jornada: {distrib or 'De ______ a ______, en horario de ______h a ______h'}<br/>
            {('<b>Observaciones:</b> ' + formulario.observaciones_jornada) if jornada == 'Parcial' and formulario.observaciones_jornada else ''}
            """,
            normal
        )

        tabla_jornada = Table(
            [[contenido_jornada_izquierda, contenido_jornada_derecha]],
            colWidths=[150, 400]
        )
        tabla_jornada.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        return [tabla_contrato, Spacer(1, 6), tabla_jornada]


    for bloque in construir_tabla_tipo_contrato(formulario):
        elements.append(bloque)
    elements.append(Spacer(1, 6))

    # ------------ 4. TITULACIÓN, FUNCIONES Y CATEGORÍA (AL FINAL) ---------
    # Fila 1: Título a la izquierda, texto explicativo a la derecha
    fila1_izq = Paragraph("<b>TITULACIÓN REQUERIDA EN CONVOCATORIA FIB:</b>", normal)
    fila1_der = Paragraph(
        "De ser necesario indicarlo en el contrato, indique aquí la descripción de las tareas, los logos a incluir, y cualquier otra cláusula adicional extraordinaria que sea necesaria.",
        normal
    )

    # Fila 2 izquierda: categoría y servicios
    col2_izq = [
        Paragraph("<b>Categoría, de acuerdo con el CONVENIO COLECTIVO:</b>", normal),
        Paragraph(f"• ÁREA: {formulario.categoria_area or ''}", normal),
        Paragraph(f"• GRUPO: {formulario.categoria_grupo or ''}", normal),
        Paragraph(f"• CATEGORÍA PROFESIONAL: {formulario.categoria_profesional or ''}", normal),
        Spacer(1, 4),
        Paragraph(f"<b>Prestará sus servicios como:</b> {formulario.prestara_servicios_como or ''}", normal),
        Paragraph(f"{'☑' if formulario.tipo_personal == 'PI' else '☐'} PERSONAL INVESTIGADOR (ÁREA 1)", normal),
        Paragraph(f"{'☑' if formulario.tipo_personal == 'SOPORTE' else '☐'} PERSONAL DE SOPORTE CIENTÍFICO/TÉCNICO (ÁREA 2)", normal),
        Paragraph(f"{'☑' if formulario.tipo_personal == 'GESTION' else '☐'} PERSONAL DE ADMINISTRACIÓN Y GESTIÓN (ÁREA 3)", normal),
    ]
    col2_izq_cell = [c for c in col2_izq]

    # Fila 2 derecha: funciones + logos + cláusulas

    # Convertimos PIL.Image a ImageReader para usar en ReportLab

    col2_der = [
        Paragraph("<b>Funciones:</b>", normal),
        Paragraph(formulario.funciones or '', normal),
        Spacer(1, 4),
        Paragraph("<b>Logos:</b>", normal),
    ]

    for ext, pil_img in logos:
        image_io = BytesIO()
        pil_img.save(image_io, format=ext.upper())
        image_io.seek(0)
        img_reader = ImageReader(image_io)
        img = Image(img_reader, width=4*cm, height=4*cm)
        col2_der.append(img)
        col2_der.append(Spacer(1, 2))

    print(f"Logos para {formulario.pk}:", logos)
    print(f"[🧪] Número de logos recibidos: {len(logos)}")
    for ext, pil_img in logos:
        print(f"[🧪] Logo formato: {ext}, tamaño: {pil_img.size}, modo: {pil_img.mode}")


    col2_der.extend([
        Spacer(1, 4),
        Paragraph("<b>Cláusulas adicionales extraordinarias:</b>", normal),
        Paragraph(formulario.clausulas_adicionales_rrhh or '', normal)
    ])

    col2_der_cell = [c for c in col2_der]

    # Crear tabla combinada con dos filas
    tabla_fusionada = Table(
        [
            [fila1_izq, fila1_der],
            [col2_izq_cell, col2_der_cell]
        ],
        colWidths=[275, 275]
    )

    tabla_fusionada.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ]))



    elements.append(tabla_fusionada)
    elements.append(Spacer(1, 6))

    # --- SECCIÓN 3.B CONTRATO DE ACTIVIDADES CIENTÍFICO-TÉCNICAS ---
    bloque_3b_titulo = Paragraph(
        '<font color="black"><b>3.B CONTRATO DE ACTIVIDADES CIENTÍFICO-TÉCNICAS</b></font>',
        ParagraphStyle('titulo3b', parent=normal, textColor=colors.black, fontName='DejaVuSans-Bold')
    )

    # Párrafo explicativo cláusula séptima
    parrafo_7 = Paragraph(
        'Indique la Información necesaria PARA LA CLÁUSULA SÉPTIMA DEL CONTRATO INDEFINIDO PARA LA '
        'REALIZACIÓN DE ACTIVIDADES CIENTÍFICO-TÉCNICAS, que tiene la siguiente redacción:',
        bold
    )

    texto_clausula_7 = Paragraph(
        '<b>SÉPTIMA:</b>La actividad del presente contrato se desarrollará en el marco de la línea de investigación /del proyecto/ de los servicios'
        'científico-técnicos: __________________________________________________________________________ conforme a lo'
        'establecido en las bases de la convocatoria del proceso selectivo nº____________.  El contrato se financiará con cargo a la financiación'
        'indicada en la Cláusula Decimocuarta',
        normal
    )

    # OBJETO DEL CONTRATO
    subtitulo_objeto = Paragraph(
        '<font color="black"><b>1) OBJETO DEL CONTRATO.</b></font> En este apartado se indicará el motivo de la contratación. '
        'Cumplimentar sólo una de las 3 opciones, en función del nivel de vinculación del trabajador a la Fundación.<br/>'
        '<u>Línea Investigación:</u><br/><u>Proyecto:</u><br/><u>Servicios científico/técnicos:</u>',
        normal
    )

    objeto = Paragraph(formulario.objeto_contrato or '', normal)

    # Clausula 14
    parrafo_14 = Paragraph(
        'Indique la Información necesaria PARA LA CLÁUSULA DECIMOCUARTA DEL CONTRATO INDEFINIDO PARA LA '
        'REALIZACIÓN DE ACTIVIDADES CIENTÍFICO-TÉCNICA, que tiene la siguiente redacción:',
        bold
    )

    texto_clausula_14 = Paragraph(
        '<b>DECIMOCUARTA:</b> Para la ejecución de este contrato se cuenta inicialmente con la financiación de la Entidad/ de la Ayuda/ del '
        'Programa/ de la partida presupuestaria asignada por el Grupo de Investigación, con los siguientes códigos internos:<br/>'
        'Todo ello para el desarrollo de la Línea de Investigación/ del Proyecto/ o de los Servicios científico-técnicos establecidos para '
        'la ejecución de las funciones descritas en la convocatoria de la FIBH.<br/>Referencia: (en su caso los proyectos de I+D+i que '
        'sean recogidos en Adendas al presente contrato).',
        normal
    )

    # FINANCIACIÓN DEL CONTRATO
    subtitulo_financiacion = Paragraph(
        '<font color="black"><b>2) FINANCIACIÓN DEL CONTRATO.</b></font> En este apartado se indicará la Entidad, programa de financiación, '
        'código o identificación de la partida presupuestaria contra la que se cargarán los costes del contrato.',
        normal
    )

    financiacion = Paragraph(formulario.financiacion or '', normal)

    # Montamos el bloque en una tabla de 1 columna para mantener formato unificado
    bloque_3b = Table([
        [bloque_3b_titulo],
        [parrafo_7],
        [texto_clausula_7],
        [subtitulo_objeto],
        [objeto],
        [parrafo_14],
        [texto_clausula_14],
        [subtitulo_financiacion],
        [financiacion]
    ], colWidths=[550])

    bloque_3b.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))

    elements.append(bloque_3b)
    elements.append(Spacer(1, 6))


    elements.append(PageBreak())

    # -------- NUEVA PÁGINA: CONDICIONES ECONÓMICAS --------

    # Título
    titulo_condiciones = Paragraph(
        '<font color="black"><b>CONDICIONES ECONÓMICAS</b></font>',
        ParagraphStyle('condiciones', parent=normal, fontName='DejaVuSans-Bold', textColor=colors.black)
    )

    # Subtabla de condiciones económicas
    tabla_economicas = Table([
        [
            titulo_condiciones,
            Paragraph("<b>APLICA TABLAS CONVENIO</b>", normal)
        ],
        [
            Paragraph("<b>Retribución Bruta Anual:</b>", normal),
            Table([
                [Paragraph(f"{'☑' if formulario.aplica_tablas_convenio else '☐'} SI", normal)],
                [Paragraph(
                    '☐ NO<br/>(Art. 2.2 del Convenio. Cuando el importe de la convocatoria externa coincida con el coste o la retribución que vaya a percibir.)',
                    normal)],
                [Paragraph(f"☐ Salario ____________ €", normal)],
                [Paragraph(f"☐ Coste fijado en convocatoria ____________ €", normal)]
            ], colWidths=[250])
        ],
        [
            Paragraph("<b>¿Requiere autorización de Hacienda?</b>", normal),
            Paragraph(
                f"{'☑' if formulario.requiere_autorizacion_hacienda else '☐'} SI &nbsp;&nbsp;&nbsp;&nbsp;"
                f"{'☐' if formulario.requiere_autorizacion_hacienda else '☑'} NO",
                normal
            )
        ],
        [
            Paragraph("<b>Importe Coste Empresa Anual:</b>", normal),
            Paragraph(f"{formulario.importe_coste_empresa_anual or ''} €", normal)
        ],
        [
            Paragraph("<b>Nota 1:</b> Se entiende como Coste Empresa = Retribución bruta del trabajador + S.S. empresa + Provisión para indemnización."
                      "<br/>(En los contratos de actividades científico/técnicas la provisión de la indemnización se calculará, por defecto, a 20 días/año)", normal),
            ""
        ],
        [
            Paragraph("<b>Nota 2:</b> Para el caso que, el presupuesto disponible sólo cubra la retribución bruta y la S.S de la empresa indíquelo expresamente.", normal),
            ""
        ],

    ], colWidths=[275, 275])

    tabla_economicas.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))

    elements.append(tabla_economicas)

    # Notas aclaratorias
    elements.append(Spacer(1, 4))


    # DOCUMENTACIÓN A ADJUNTAR
    titulo_doc = Paragraph(
        '<font color="black"><b>DOCUMENTACIÓN A ADJUNTAR</b></font>',
        ParagraphStyle('doc_titulo', parent=normal, fontName='DejaVuSans-Bold', textColor=colors.black)
    )

    documentacion_texto = Paragraph(
        "- Fotocopia DNI o<br/>"
        "- Fotocopia compulsada por la Policía del NIE/Pasaporte<br/>"
        "- Fotocopia Nº de afiliación de la Seguridad Social<br/>"
        "- Copia compulsada del <u>Título Académico</u><br/>"
        "- Fotocopia Tarjeta del INEM (en caso de estar en paro)<br/>"
        "- Soporte documental de méritos requeridos en la convocatoria.",
        normal
    )

    # Tabla con 1 columna para mantener consistencia
    tabla_doc = Table([
        [titulo_doc],
        [documentacion_texto],
    ], colWidths=[550])

    tabla_doc.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))

    elements.append(tabla_doc)
    elements.append(Paragraph(
        'Esta ficha se subirá en el enlace generado que se especifíca en el correo: '
        'junto con la documentación que sea necesario aportar, escaneada.',
        normal
    ))

    elements.append(Paragraph(
        '① Los trabajadores nacionales de la comunidad europea que no estén en posesión de un Número de Identificación de Extranjeros en España, '
        'o N.I.E, aportarán provisionalmente un número de pasaporte o carta de identidad, pero deberán solicitar en el plazo más breve posible, '
        'anterior al contrato de trabajo, ese Número de Identificación de Extranjeros, o N.I.E. ante la Dirección General de la Policía. '
        'Los trabajadores extranjeros no comunitarios deberán aportar necesariamente copia compulsada de su NIE.', normal
    ))


    elements.append(Paragraph(
        '② En cuanto al número de afiliación es necesario que el trabajador esté en posesión de un número como trabajador, '
        'esto es, que el número que aparece en la tarjeta nunca debe de acabar con la letra B (Beneficiario). '
        'Si el trabajador no está en posesión de este número, deberá acudir a la Administración más cercana de la Seguridad Social. '
        'En el caso de no estar en ese momento en posesión del dato del trabajador/a en la Fundación.', normal
    ))

    # ---- Finalizamos el documento ----
    doc.build(elements)
    buffer.seek(0)
    return buffer



