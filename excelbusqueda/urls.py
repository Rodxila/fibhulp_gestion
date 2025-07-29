from django.urls import path
from . import views

urlpatterns = [
    path('', views.buscar_en_excel, name='buscar_excel'),
    path('exportar/', views.exportar_excel, name='exportar_excel'),

]
