from django.urls import path
from .views import contratos_view, facturas_view, login_view, logout_view, exportar_facturas_excel
from ensayos_clinicos.views import exportar_contratos_excel

urlpatterns = [
    path('contratos/', contratos_view, name='contratos'),
    path('facturas/', facturas_view, name='facturas'),
    path('ensayos-clinicos/login/', login_view, name='login'),
    path('ensayos-clinicos/logout/', logout_view, name='logout'),
    path('facturas/exportar/', exportar_facturas_excel, name='exportar_facturas_excel'),
    path('contratos/exportar/', exportar_contratos_excel, name='exportar_contratos_excel'),
]






