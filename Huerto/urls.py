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

    path('huerto/huerto/',views.sin_incidencia,name='sinincidencia')
]