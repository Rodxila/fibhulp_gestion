# legal/urls.py
from django.urls import path
from .views import (
    convocatorias_view,
    concursos_view,
    calendario_concursos_view,
    exportar_concursos_excel,
    borrar_concurso,
    borrar_convocatoria,
    editar_convocatoria,
)

urlpatterns = [
    path('convocatorias/', convocatorias_view, name='legal_convocatorias'),
    path('concursos/', concursos_view, name='legal_concursos'),
    path('calendario/', calendario_concursos_view, name='legal_calendario'),
    path('exportar-concursos/', exportar_concursos_excel, name='exportar_concursos_excel'),
    path('borrar-concurso/<int:pk>/', borrar_concurso, name='borrar_concurso'),
    path('convocatoria/<int:pk>/editar/', editar_convocatoria, name='editar_convocatoria'),
    path('convocatoria/<int:pk>/borrar/', borrar_convocatoria, name='borrar_convocatoria'),
]