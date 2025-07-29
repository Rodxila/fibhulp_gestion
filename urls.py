from django.contrib import admin
from django.urls import path, include
from ensayos_clinicos.views import bienvenida_view

urlpatterns = [
    path('', bienvenida_view, name='bienvenida'),  # 👈 esta es la página raíz
    path('admin/', admin.site.urls),
    path('ensayos-clinicos/', include('ensayos_clinicos.urls')),
    path('fundanet/', include('fundanet.urls')),  # 👈 Añadido aquí
    path('legal/', include('legal.urls')),
    path('rrhh/', include('rrhh.urls')),
]



