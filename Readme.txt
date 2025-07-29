# FIBHULP Gestión

Aplicación Django para gestionar convocatorias, ensayos clínicos, RRHH, concursos legales y estructuras de investigación.

## 🔧 Funcionalidades

### RRHH
- Formulario dinámico para contratación de personal.
- Generación de fichas en PDF basadas en plantilla Word.
- Extracción automática de información desde PDFs de convocatorias.
- Almacenamiento de documentación en carpetas por usuario.
- Envío automático de correos de confirmación.

### Ensayos Clínicos
- Registro de nuevos ensayos y detalles de facturación.
- Panel restringido a usuarios autenticados por sección.
- Procesamiento de facturas y desglose por detalles.

### Búsqueda en Excel
- Subida de ficheros `.xlsx` y búsqueda de palabras clave.
- Muestra tabla de resultados directamente en el navegador.

### Legal
- Gestión de concursos y convocatorias legales.
- Alertas por fecha límite y envío automático de correos.
- Manejo de estados de concurso.

### Fundanet
- Vista HTML estática para estructuras como proyectos, investigadores, nodos, etc.
- Normalización de nombres para comparación.

## 📁 Estructura de carpetas relevante

fibhulp_gestion/
├── rrhh/ # Gestión de recursos humanos
├── ensayos_clinicos/ # Datos y facturación de ensayos
├── excelbusqueda/ # Herramienta de búsqueda en Excel
├── legal/ # Convocatorias y concursos legales
├── fundanet/ # Información estática (terceros, nodos...)
├── static/ # Archivos estáticos
├── media/ # Archivos subidos
└── documentos/, cvs/ # Almacenamiento documental de candidatos


## 🛠 Instalación

1. Clona este repositorio.
2. Crea un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate

Instala las dependencias:

pip install -r requirements.txt


Configura variables de entorno (.env).

Aplica migraciones:

python manage.py migrate

Ejecuta el servidor:

python manage.py runserver


🔒 Notas de Seguridad
⚠️ Esta aplicación no debe usarse en producción sin una revisión profunda de seguridad. Actualmente no se almacena información real, pero se han preparado funcionalidades para el manejo de datos sensibles.

📝 Notas Finales
Este repositorio se conserva como respaldo de trabajo por si se retoma el proyecto. Actualmente se encuentra pausado.

