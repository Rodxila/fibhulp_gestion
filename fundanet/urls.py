from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='fundanet_index'),
    path('terceros/', views.terceros_inicio, name='fundanet_terceros'),
    path('terceros/duplicados/', views.buscar_terceros_duplicados, name='fundanet_terceros_duplicados'),
    path('proyectos/', views.proyectos, name='fundanet_proyectos'),
    path('investigadores/', views.investigadores, name='fundanet_investigadores'),
    path('grupos/', views.grupos, name='fundanet_grupos'),
    path('nodos/', views.nodos, name='fundanet_nodos'),

]


