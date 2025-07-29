import requests

def obtener_ofertas_disponibles():
    url = "https://www.iis-princesa.org/wp-json/fib/v1/ofertas"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Extraer solo las disponibles
        disponibles = data.get("disponibles", [])
        
        # Preparar para ChoiceField en formato: (valor, etiqueta visible)
        opciones = [
            (oferta["titulo"], f"{oferta['titulo']} ({oferta['referencia']})")
            for oferta in disponibles
        ]
        return opciones

    except Exception as e:
        print(f"[ERROR] Fallo al obtener ofertas: {e}")
        return []

import requests
import re
from io import BytesIO
from PyPDF2 import PdfReader
import fitz  # PyMuPDF
from PIL import Image

def extraer_datos_oferta_pdf(pdf_url):
    try:
        # Descargar PDF
        response = requests.get(pdf_url)
        response.raise_for_status()
        file_stream = BytesIO(response.content)

        # ---------- TEXTO (con PyPDF2) ----------
        reader = PdfReader(file_stream)
        texto = ""
        for page in reader.pages:
            texto += page.extract_text() + "\n"

        # IP
        ip_match = re.search(r"bajo la dirección de (.+?)[\.,\n]", texto, re.IGNORECASE)
        ip = ip_match.group(1).strip() if ip_match else None

        # Funciones / Tareas
        tareas_match = re.search(r"TAREAS A REALIZAR\s*(.*?)(?=\n[A-ZÁÉÍÓÚÜÑ]{2,}|$)", texto, re.DOTALL)
        funciones = tareas_match.group(1).strip() if tareas_match else None

        # Puesto (dos variantes posibles)
        puesto = None
        match_puesto = re.search(
            r"La Fundación de Investigación Biomédica del Hospital Universitario de la Princesa convoca (?:un )?(?:puesto|una plaza) de\s+([^\n\r]+)",
            texto
        )
        if match_puesto:
            puesto = match_puesto.group(1).strip()

        # ---------- IMÁGENES (con fitz) ----------
        logos = []
        doc = fitz.open(stream=response.content, filetype="pdf")
        for page in doc:
            if "4. PRESENTACIÓN DE SOLICITUDES" in page.get_text():
                break
            for img in page.get_images(full=True):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                image = Image.open(BytesIO(image_bytes))
                logos.append((image_ext, image))  # Puedes guardarlas o procesarlas como necesites

        return {
            "ip": ip,
            "funciones": funciones,
            "puesto": puesto,
            "logos": logos,  # lista de tuplas (ext, PIL.Image)
        }

    except Exception as e:
        return {
            "error": str(e),
            "ip": None,
            "funciones": None,
            "puesto": None,
            "logos": [],
        }

