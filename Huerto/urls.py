from django.urls import path 
from .import views

urlpatterns =[
    path('',views.index,name='index'),

    path('planta/planta/<int:id_huerto>/',views.lista_planta_huerto,name='plantahuerto'),

    path('contrasenha/contrasenha/<int:id_usuario>/',views.ultima_modificacion,name='cambiocontrasenha'),

    path('gastos/gastos/<int:id_huerto>/<int:anho_gasto>',views.gasto_huerto,name='gasto_huerto'),

    path('usuario/usuario/<str:inicial>/',views.usuarios_parcelas,name='usuariosparcelas'),

    path('plaga/plaga/<str:plant>/',views.plaga_planta,name='plagaplanta'),

    path('tratamiento/tratamiento/',views.consejo_plaga,name='consejoplaga'),

    path('usuario/usuario/',views.usuario_noticia,name='usuarionoticia'),

    path('planta/planta/<int:mi>/<int:ma>/<int:lu>/',views.planta_phluz,name='plantaphluz'),

    path('huerto/huerto/',views.incidencia_reciente,name='incidenciareciente'),

    path('huerto/huerto/',views.sin_incidencia,name='sinincidencia'),
    
    #url examen 7 noviembre
    
    #último voto que se realizó en un huerto en concreto, mostrar comentario, votacion, e informacion del usuario que lo hizo
    path('votacion/votacion/<int:id_huerto>/',views.ultimo_voto_huerto,name='ultimovotohuerto'),
    
    #modelos con puntuacion >=3 de un usuario concreto
    path('votacion/ejercicio2/<int:id_usuario>/',views.voto_mas_tres,name='votomastres'),
    
    #Todos los usuarios o clientes que no han votado nunca y mostrar información sobre estos usuarios y clientes al completo..
    path('usuario/ejercicio3/',views.no_voto,name='novoto'),
    
    #btener las cuentas bancarias que sean de la Caixa o de Unicaja y que el propietario tenga un nombre que contenga un texto en concreto
    
    path('cuentas/cuentas/<str:nombreu>/',views.cuenta_usuario,name='cuentausuario'),
    
    #obtener modelos con media de votacion superior a 2,5
    
    path('votacion/votacion/',views.media_doscinco,name='mediadoscinco'),
    path('huerto/create/',views.huerto_create,name='huerto_create'),
    path('huerto/huertos/',views.huertos_lista,name='listahuertos'),
    path('huerto/buscar/',views.huerto_buscar,name='huerto_buscar'),
    path('huerto/buscar_avanzado/',views.huerto_buscar_avanzado,name='huerto_buscar_avanzado'),
    path('huerto/editar/<int:huerto_id>',views.huerto_editar,name='huerto_editar'),
    path('huerto/eliminar/<int:huerto_id>',views.huerto_eliminar,name='huerto_eliminar'),

    path('usuario/create/',views.usuario_create,name='usuario_create'),
    path('usuario/usuarios/',views.usuario_lista,name='usuario_lista'),
    path('usuario/editar/<int:id_usuario>',views.usuario_editar,name='usuario_editar'),
    path('usuario/eliminar/<int:usuario_id>',views.usuario_eliminar,name='usuario_eliminar'),

    path('usuario/buscar',views.usuario_buscar,name='usuario_buscar'),
    path('gastos/crear/',views.gastos_create_simple,name='gastos_create'),
    path('gastos/gastos',views.gasto_lista,name='gastos_lista'),
    path('gasto/buscar/',views.gasto_buscar,name='gasto_buscar'),
    path('gastos/editar/<int:id_gasto>',views.gastos_editar,name='gastos_editar'),
    path('gastos/eliminar/<int:id_gasto>',views.gasto_eliminar,name='gasto_eliminar'),
    
    path('blog/lista',views.blog_lista,name="blog_lista"),
    path('blog/crear',views.blog_create_simple,name='blog_crear'),
    path('blog/buscar',views.blog_buscar,name='blog_buscar'),
    path('blog/editar/<int:id_blog>',views.blog_editar,name='blog_editar'),
    path('blog/eliminar/<int:id_blog>',views.blog_eliminar,name="blog_eliminar"),

    path('incidencias/crear',views.incidencia_create_sencillo,name='incidencia_create'),
    path('incidencia/incidencia/<int:id_incidencia>',views.incidencia_mostrar,name='incidencia_mostrar'),
    path('incidencia/listar',views.incidencia_lista,name='incidencia_lista'),
    path('incidencia/buscar/',views.incidencia_buscar_avanzado,name='incidencia_buscar_avanzado'),
    path('incidencia/editar/<int:incidencia_id>',views.incidencia_editar,name="incidencia_editar"),
    path('incidencia/eliminar/<int:incidencia_id>',views.incidencia_eliminar,name="incidencia_eliminar"),

    path('fruto/listar',views.fruto_lista,name='fruto_lista'),
    path('fruto/create/',views.fruto_create,name='fruto_create'),
    path('fruto/buscar/',views.fruto_buscar,name='fruto_buscar'),
    path('fruto/editar/<int:fruto_id>',views.fruto_editar,name='fruto_editar'),
    path('fruto/eliminar/<int:fruto_id>',views.fruto_eliminar,name='fruto_eliminar'),
    
    path('tratamiento/listar',views.tratamiento_lista,name='tratamiento_lista'),
    path('tratamiento/create/',views.tratamiento_create,name='tratamiento_create'),
    path('tratamiento/buscar/',views.tratamiento_buscar,name='tratamiento_buscar'),
    path('tratamiento/editar/<int:tratamiento_id>',views.tratamiento_actualizar,name='tratamiento_actualizar'),
    path('tratamiento/eliminar/<int:tratamiento_id>',views.tratamiento_eliminar,name='tratamiento_eliminar'),


    path('registrar',views.registrar_usuario,name='registrar_usuario'),
    
    #examen 14 diciembre
    
    path('promocion/crear/',views.promocion_create,name='promocion_create'),
    path('promocion/editar/<int:id_promocion>',views.promocion_editar,name='promocion_editar'),
    path('promocion/buscar/',views.promocion_buscar,name='promocion_buscar'),
    path('promocion/eliminar/<int:id_promocion>',views.promocion_eliminar,name='promocion_eliminar'),
    path('promocion/promocion',views.promocion_lista,name='promocion_lista')
    
]