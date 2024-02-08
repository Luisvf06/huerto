from django.urls import path
from .api_views import *

urlpatterns = [
    
    path('huertos',huerto_list),
    path('huertos_mejorada',huerto_lista_mejorada),
    path('huerto_busqueda_simple',huerto_buscar),#huerto_busqueda_simple es la direccion de la api cliente en la linea response... http...api/v1. huerto_buscar es el nombre de la api_view.py
    path('huerto_busqueda_avanzada',huerto_buscar_avanzado),

    path('gastos',gasto_list),
    path('gastos_busqueda_avanzada',gastos_buscar_avanzado),
    
    path('blogs',blog_list),
    path('huerto/<int_huerto_id>',huerto_obtener),
    path('blog_busqueda_avanzada',blog_buscar_avanzado),

    path('usuario',usuario_list),
    path('huertos/crear',huerto_crear),
    
    path('gastos/crear',gasto_crear),
    path('blog/crear',blog_crear),
]