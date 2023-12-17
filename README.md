Tarea 17 diciembre

Parte 4
6 crud: huerto, gasto, blog,  incidencia, fruto y tratamiento
También hice un crud de usuario, pero como con la parte de login y permisios cambió, lo he dejaod comentado.

Los CRUD empiezan en la linea 141 de views.py
Huerto:
    Crear: funciona
        Validacion: 
            La latitud debe estar entre -90 y 90 y la logitud entre 180 y -180
            Los campos de ubicación y sitio tienen que tener una opcion marcada
            Area debe ser un nº entero o flotante y mayor que 0
            Acidez debe estar entre 0 y 14 sin ser igual al extremo del rango
    Editar: funciona
    Borrar: funciona
    Busqueda avanzada: no funciona
        Widget: checkboxselectmultiple()
            CheckboxInput()

Gastos
        Crear: funciona
            Validacion: 
                herramientas, facturas e imprevistos deben ser float, fecha debe ser hoy o anterior a hoy
        Editar: funciona
        Borrar: borra pero no pregunta
        Busqueda avanzada: funciona
            Widget: checkboxselectmultiple(), forms.SelecDateWidget(), forms.HiddenInput()

Blog
    Crear: funciona
        Validacion: fecha solo puede ser hoy, etiqueta tiene ser estar en mayúsculas y tener al menos 2 caracteres
    Editar: no funciona
    Borrar: funciona
    Busqueda avanzada: funciona
        Widget: forms.CheckboxSelectMultiple(),
        forms.TextInput(attrs={'placeholder':'Etiqueta'})
        forms.DateInput()
        forms.Textarea


Incidencia
    Crear funciona
        Validacion descripcion entre 10 y 2000 cracteres fecha presente o pasada
    Editar funciona
    Borrar funciona
    Busqueda Avanzada no funciona
        Widget ninguno nuevo

Fruto
    Crear funciona
        Validacion no existe otro fruto con ese nombre, el nombre solo puede tener letras y la inicial ser mayúscula. En busqueda avanzada planta debe ser entero
    Editar funciona
    Borrar funciona
    Busqueda Avanzada no funciona
        Widget


Tratamiento
    Crear funciona 
        Validacion los campos deben tener una longitud entre dos rangos
    Editar funciona
    Borrar borra
    Busqueda Avanzada funciona
        Widget


PARTE 5 SESIONES Y AUTENTICACIÓN
Tengo dos tipos de usuario el normal y el premium, la diferencia entre ambos son los permisos que tienen asignados. El normal tiene permiso para ver todo y añadir un par de elementos y el premium tiene permiso de vista, añadir y cambiar















Parte del crud usuario que quité 
'''
    path('usuario/create/',views.usuario_create,name='usuario_create'),
    path('usuario/usuarios/',views.usuario_lista,name='usuario_lista'),
    path('usuario/editar/<int:id_usuario>',views.usuario_editar,name='usuario_editar'),
    path('usuario/eliminar/<int:usuario_id>',views.usuario_eliminar,name='usuario_eliminar'),
    path('usuario/buscar',views.usuario_buscar,name='usuario_buscar'),
''',

<div><a href="{% url 'usuario_create' %}">Crear usuario</a></div>
    <div><a href="{% url 'usuario_lista' %}">Lista de usuarios</a></div>
    <div><a href="{% url 'usuario_buscar'%}">Buscar usuario</a></div>