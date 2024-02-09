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
    path('gasto/<int_gasto_id>',gasto_obtener),
    path('blog/<int_blog_id>',blog_obtener),
    path('blog_busqueda_avanzada',blog_buscar_avanzado),

    path('usuario',usuario_list),
    path('huertos/crear',huerto_crear),
    path('huertos/eliminar/<int:huerto_id>',huerto_eliminar),
    path('gastos/eliminar/<int:gastos_id>',gastos_eliminar),
    path('blog/eliminar/<int:blog_id>',blog_eliminar),
    path('gastos/crear',gasto_crear),
    path('blog/crear',blog_crear),
]