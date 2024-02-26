from django.urls import path
from .api_views import *

from .api_views import FileUploadAPIView

app_name = 'Huerto'
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
    path('huerto/editar/<int:huerto_id>',huerto_editar),
    path('gasto/editar/<int:gasto_id>',gasto_editar),
    path('blog/editar/<int:blog_id>',blog_editar),


    path('huerto/actualizar/ubicacion/<int:huerto_id>',huerto_editar_ubicacion),
    path('huerto/actualizar/sitio/<int:huerto_id>',huerto_editar_sitio),
    path('huerto/actualizar/sustrato/<int:huerto_id>',huerto_editar_sustrato),
    path('huerto/actualizar/abonado/<int:huerto_id>',huerto_editar_abonado),
    path('huerto/actualizar/area/<int:huerto_id>',huerto_editar_area),
    path('huerto/actualizar/acidez/<int:huerto_id>',huerto_editar_acidez),

    path('Gasto/actualizar/factura/<int:gasto_id>',gasto_editar_factura),
    path('Gasto/actualizar/descripcion/<int:gasto_id>',gasto_editar_descripcion),
    path('Gasto/actualizar/herramientas/<int:gasto_id>',gasto_editar_herramientas),
    path('Gasto/actualizar/imprevistos/<int:gasto_id>',gasto_editar_imprevistos),
    path('Gasto/actualizar/fecha/<int:gasto_id>',gasto_editar_fecha),

    path('Blog/actualizar/Fecha/<int:blog_id>',blog_editar_fecha),
    path('Blog/actualizar/etiqueta/<int:blog_id>',blog_editar_etiqueta),
    path('Blog/actualizar/publicacion/<int:blog_id>',blog_editar_publicacion),
    path('registrar/usuario',registrar.as_view()),
    path('usuario/token/<str:token>',obtener_usuario_token),

#tarea final
    #Gabriela
    path('plantas_estacion/<str:estacion>/',plantas_estacion),
    #Manuel
    path('huerto_disponible',huerto_disponible),
    #Irene
    path('recolectable/<int:id_huerto>',huerto_recolectable),
    #Álvaro

]