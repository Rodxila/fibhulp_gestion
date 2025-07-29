from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_rrhh, name='rrhh_inicio'),
    path('contratacion/', views.contratacion_view, name='rrhh_contratacion'),
    path('nominas/', views.nominas_view, name='rrhh_nominas'),
    path('login/', views.login_view, name='login_view'),
    path('home/', views.rrhh_home, name='rrhh_home'),
    path('formulario-empleado/<int:pk>/', views.formulario_empleado, name='formulario_empleado'),
    path('formulario-empresa/<int:pk>/', views.formulario_empresa, name='formulario_empresa'),
    path('eliminar-formulario/<int:pk>/', views.eliminar_formulario, name='eliminar_formulario'),
    path('seleccion/', views.seleccion_personal, name='seleccion_view'),
    path('candidatos/', views.lista_candidatos, name='lista_candidatos'),
    path('candidatos/exportar/', views.exportar_candidatos_excel, name='exportar_candidatos_excel'),
    path('candidatos/seleccionar/<int:pk>/', views.seleccionar_candidato, name='seleccionar_candidato'),
    path('candidatos/descartar/<int:pk>/', views.descartar_candidato, name='descartar_candidato'),
    path('ficha/<str:token>/', views.subida_ficha, name='subida_ficha'),
    path('ficha/<int:pk>/editar_rrhh/', views.editar_datos_rrhh, name='editar_datos_rrhh'),
    path('descargar-documentacion/<int:pk>/', views.descargar_documentacion, name='descargar_documentacion'),
]



