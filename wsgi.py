import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fibhulp_gestion.settings')
application = get_wsgi_application()
