from django.shortcuts import render,redirect
from .models import *
from django.views.defaults import page_not_found
from django.views.defaults import bad_request
from django.views.defaults import server_error
from django.views.defaults import permission_denied
from django.db.models import Q, Prefetch, Avg
from django.contrib import messages
from .forms import *
from django.forms import modelform_factory
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group

# Create your views here.
def index(request):
    if (not "fecha_inicio" in request.session):
        request.session["fecha_inicio"] =datetime.now().strftime('d/%m/%Y %H:%M')
    return render(request,'index.html')

def huertos_lista(request):
    huertos=Huerto.objects.prefetch_related(Prefetch('huerto_incidencia')).prefetch_related('usuario')
    return render(request,'huerto/listahuerto.html',{'huertos_lista',huertos})

#devuelve las plantas que se encuentran en un huerto determinado
@permission_required('Huerto.view_planta')
def lista_planta_huerto(request,id_huerto):
    plantas=Planta.objects.select_related('huerto')
    plantas=plantas.filter(huerto=id_huerto)
    return render(request,'planta/listaplanta.html',{'plantas_huerto':plantas})

#devuelve la fecha de la ultima modificacion de la contraseña, de un usuario. La idea original era sacar sólo la última contraseña porque pensaba que el campo era fecha_modificacion y no ultima_... he intentado cambiarlo pero no he encontrado ningún field de tipo lista en la documentación, por eso añado id_usuario
'''def ultima_modificacion(request,id_usuario):
    contras=Contrasenha.objects.select_related('usuario')
    contras=contras.filter(usuario=id_usuario)#.order_by('-ultima_modificacion')[:1].get()
    return render(request,'contrasenha/listacontra.html',{'modificaciones':contras})
'''
#devuelve el gasto que ha supuesto un determinado huerto en un año
@permission_required('Huerto.view_gastos')
def gasto_huerto(request,id_huerto,anho_gasto):
    gastos=Gastos.objects.select_related('usuario')
    gastos=gastos.filter(Q(usuario__usuario_huerto=id_huerto) & Q(fecha__year=anho_gasto))
    return render(request,'gastos/listagasto.html',{'gastos':gastos})

#devuelve los usuarios que tengan un huerto de tipo parcela y cuyo apellido empiece por una letra concreto
@permission_required('Huerto.view_usuario')
def usuarios_parcelas(request,inicial):
    usuarios=Usuario.objects.prefetch_related(Prefetch('usuario_huerto'))
    usuarios=usuarios.filter(Q(usuario_huerto__sitio='P') & Q(apellidos__startswith=inicial))
    return render(request, 'usuario/listausuario.html',{'usuarios_parcelas':usuarios})

#devuelve las plagas de una planta junto a su fecha y descripcion
@permission_required('Huerto.view_plaga')
def plaga_planta(request,plant):
    plagas=Plaga.objects.select_related('planta').prefetch_related(Prefetch('plaga_plant'))
    plagas=plagas.filter(planta__nombre_comun=plant)
    return render(request,'plaga/listaplaga.html',{'histo_plaga':plagas})

#devuelve los consejos de tratamiento para cada planta cuando la infeccion es por hongo
@permission_required('Huerto.view_tratamiento')
def consejo_plaga(request):
    consejos=Tratamiento.objects.prefetch_related('plaga')
    consejos=consejos.filter(plaga__origen='F')
    return render(request,'tratamiento/listatratamiento.html',{'infeccionhongos':consejos})

#devuelve la ciudad y los gastos de los usuarios que han estito noticias (N) en el blog y no han usado etiquetas
@permission_required('Huerto.view_usuario')
def usuario_noticia(request):
    usuarios=Usuario.objects.prefetch_related(Prefetch('usuario_gasto')).prefetch_related(Prefetch('usuario_blog'))
    usuarios=usuarios.filter(Q(usuario_blog__etiqueta=None)&Q(usuario_blog__publicacion='N'))
    return render(request,'usuario/listausuario.html',{'usuario_noticias':usuarios})

#devuelve las plantas que crecen en ph entre 4 y 8 y necesitan mas de 6 horas de luz al dia
@permission_required('Huerto.view_planta')
def planta_phluz(request,mi,ma,lu):
    plantas=Planta.objects.prefetch_related('huerto')
    plantas=plantas.filter(Q(phmax__lte=ma)& Q(phmin__gte=mi) &Q(horas_luz__gt=lu))
    return render(request,'planta/listaplanta2.html',{'requisitos':plantas})

#devuelve la indicencia mas reciente
@permission_required('Huerto.view_incidencia')
def incidencia_reciente(request):
    incidencias=Incidencia.objects.prefetch_related('huerto')
    incidencias=incidencias.order_by("fecha_incidencia")[:1].get()
    return render(request,'huerto/mostrar_incidencia.html',{'incidenciahuerto':incidencias})

#devuelve los huertos que no han tenido incidencias
@permission_required('Huerto.view_huerto')
def sin_incidencia(request):
    huerto=Huerto.objects.prefetch_related(Prefetch('huerto_incidencia')).prefetch_related('usuario')
    huerto=huerto.filter(huerto_incidencia__huerto=None)
    return render(request,'huerto/listahuerto.html',{'sinincidencia':huerto})

def mi_error_400(request,exception=None):
    return render(request,'errores/400.html',None,None,400)#solicitud incorrecta

def mi_error_403(request,exception=None):
    return render(request,'errores/403.html',None,None,403)#permiso denegado

def mi_error_404(request,exception=None):
    return render(request,'errores/404.html',None,None,404)#not found

def mi_error_500(request,exception=None):
    return render(request,'errores/500.html',None,None,500)#error del servidor

#vistas del examen
#Ejercicio 1
@permission_required('Huerto.view_votacion')
def ultimo_voto_huerto(request,id_huerto):
    voto=Votacion.objects.select_related('huerto','usuario')
    voto=voto.filter(huerto=id_huerto).order_by('fecha_voto')[:1].get
    return render(request,'votacion/votacion.html',{'voto':voto})
#Ejercicio 2
@permission_required('Huerto.view_votacion')
def voto_mas_tres(request, id_usuario):
    votos=Votacion.objects.select_related('huerto','usuario')
    votos=votos.filter(Q(usuario=id_usuario) &Q(puntuacion__gte=3))
    return render(request,'votacion/ejercicio2.html',{'totalvotos':votos})
#Ejercicio 3
@permission_required('Huerto.view_votacion')
def no_voto(request):
    usuarios=Usuario.objects.prefetch_related(Prefetch('usuario_voto'))
    usuarios=usuarios.filter(usuario_voto=None)
    return render (request, 'usuario/ejercicio3.html',{'sin_votos':usuarios})

#Ejercicio 4
@permission_required('Huerto.view_votacion')
def cuenta_usuario(request,nombreu):
    cuentas=Banco.objects.select_related('usuario')
    cuentas=cuentas.filter(Q(usuario__nombre__contains=nombreu) | Q(banco='C')| Q(banco='U'))
    return render(request,'cuenta/listacuenta.html',{'cuentas_usu':cuentas})

#Ejercicio 5
@permission_required('Huerto.view_votacion')
def media_doscinco(request):
    Huerto.objects.aggregate(Avg('huerto_voto',default=0))
    huertos=Huerto.objects.prefetch_related(Prefetch('huerto_voto'))

    huertos=huertos.filter(huerto_voto__gte=2.5)
    return render(request,'votacion/ejercicio5.html',{'nombre':huertos})
    

#Formularios
@permission_required('Huerto.add_huerto')
def huerto_create(request):
    datosFormulario= None
    if request.method =="POST":
        datosFormulario = request.POST
    formulario = HuertoModelForm(datosFormulario)

    if (request.method == "POST"):
        huerto_creado = crear_huerto_modelo(formulario)
        if (huerto_creado):
            messages.success(request, 'Se ha creado el huerto')
            return redirect("listahuertos")
    return render(request, 'huerto/create.html',{"formulario":formulario})

@permission_required('Huerto.add_huerto')
def crear_huerto_modelo(request):
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
    formulario = HuertoModelForm(datosFormulario)
    if (request.method == "POST"):
        if formulario.is_valid():
            try:
                # Guarda el libro en la base de datos
                formulario.save()
                return redirect("huertos_lista")
            except Exception as error:
                print(error)
    return render(request, 'huerto/create.html',{"formulario":formulario})  

@permission_required('Huerto.view_huerto')
def huertos_lista(request):
    huertos = Huerto.objects.prefetch_related("usuario")
    huertos = huertos.all()
    return render(request, 'huerto/listahuerto.html',{"huertos_mostrar":huertos})

def huerto_buscar(request):
    formulario=BusquedaHuerto(request.GET)

    if formulario.is_valid():
        texto= formulario.cleaned_data.get('textoBusqueda')
        huertos = Huerto.objects.prefetch_related("usuario")
        huertos = huertos.filter(sitio__startswith=texto)
        mensaje_devuelto= "se busca por textos que empiezan la letra: " + texto
        return render(request, 'huerto/lista_busqueda.html',{"huertos_mostrar":huertos,"texto_busqueda":texto})
    if ("HTTP_REFERER"in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index.html")
@permission_required('Huerto.view_huerto')
def huerto_buscar_avanzado(request):
    
    if (len(request.GET)>0):
        formulario=BusquedaAvanzadaHuerto(request.GET)
        if formulario.is_valid():
            mensaje_busqueda="Se ha buscado por:\n"
            QShuerto=Huerto.objects.prefetch_related("usuario")

            area_maxima=formulario.cleaned_data.get("area_maxima")
            area_minima=formulario.cleaned_data.get("area_minima")

            #if(textoBusqueda!=""):
            #    QShuerto=QShuerto.filter(Q(ubicacion__startswith=texto) | Q(usuario__nombre_usuario__contains=texto))
            #    mensaje_busqueda+="contenido de la localizacion o nombre de usuario"
            #if not sitio is None:
            #    mensaje_busqueda+='Sitio: '+sitio
            #if not sustrato is None:
            #    mensaje_busqueda+='Sustrato: '+sustrato
            if not area_minima is None:
                mensaje_busqueda += "El área mínima será igual o mayor  a"+ str(area_minima)+"\n"
                QShuerto=QShuerto.filter(area__gte=float(area_minima))
            if not area_maxima is None:
                mensaje_busqueda +="El área máxima será igual o menor a "+ str(area_maxima)+"\n"
                QShuerto=QShuerto.filter(area__lte=float(area_maxima))
            
            huertos=QShuerto.all()

            return render(request,'huerto/busqueda_avanzada.html',{"huerto_mostrar":huertos,
                                                                "texto_busqueda":mensaje_busqueda})
    else:
        formulario=BusquedaAvanzadaHuerto(None)
    
    return render(request,'huerto/busqueda_avanzada.html',{'formulario':formulario})

@permission_required('Huerto.change_huerto')
def huerto_editar(request,huerto_id):
    huerto= Huerto.objects.get(id=huerto_id)
    
    datosFormulario=None
    if request.method =="POST":
        datosFormulario = request.POST
        
    formulario = HuertoModelForm(datosFormulario,instance=huerto)
    
    if (request.method=="POST"):
        if formulario.is_valid():
            formulario.save()
            try:
                formulario.save()
                return redirect('huertos_lista')
            except Exception as e:
                pass
    return render(request,'huerto/actualizar.html',{'formulario':formulario,'huerto':huerto})
@permission_required('Huerto.delete_huerto')
def huerto_eliminar(request,huerto_id):
    huerto=Huerto.objects.get(id=huerto_id)
    try:
        huerto.delete()
        messages.success(request,"se ha eliminado el huerto"+huerto.id)
    except Exception as error:
        print(error)
    return redirect('huertos_lista')

'''
def usuario_lista(request):
    usuarios = Usuario.objects.prefetch_related(Prefetch('usuario_huerto'))
    usuarios = usuarios.all()
    return render(request, 'usuario/usuario_lista.html',{"usuarios_mostrar":usuarios})

def crear_usuario_modelo(formulario):
    usuario_creado=False
    if formulario.is_valid():
        try:
            formulario.save()
            usuario_creado = True
        except Exception as error:
            pass
    return usuario_creado

def usuario_create(request):
    datosFormulario= None
    if request.method =="POST":
        datosFormulario = request.POST
    
    formulario = UsuarioModelForm(datosFormulario)

    if (request.method =="POST"):
        usuario_creado= crear_usuario_modelo(formulario)
        if (usuario_creado):
            messages.success(request, 'se ha creado el usuario'+formulario.cleaned_data.get('nombre_usuario')+"correctamente")
            return redirect("usuario_lista")
    return render(request, 'usuario/crearusuario.html',{"formulario":formulario})

def usuario_editar(request,id_usuario):
    usuario=Usuario.objects.get(id=id_usuario)

    datosFormulario=None

    if request.method =="POST":
        datosFormulario = request.POST
    
    formulario = UsuarioModelForm(datosFormulario,instance=usuario)

    if (request.method =="POST"):
        if formulario.is_valid():
            try:
                formulario.save()
                return redirect('usuario_lista')
            except Exception as error:
                print(error)
    return render(request,'usuario/actualizar.html',{"formulario":formulario,"usuario":usuario})

def usuario_eliminar(request,id_usuario):
    usuario= Usuario.objects.get(id=id_usuario)
    try:
        usuario.delete()
        messages.success(request,"se ha eliminado el usuario"+usuario+' '+usuario.nombre_usuario)
    except Exception as error:
        print(error)
    return redirect('usuario_lista')

def usuario_buscar(request):
    if(len(request.GET)>0):
        formulario= BusquedaAvanzadaUsuario(request.GET)
        if formulario.is_valid():
            mensaje="Se ha buscado por:\n"
            QSusuarios=Usuario.objects.all()

            textoBusqueda=formulario.cleaned_data.get('textoBusqueda')
            usuariotelefono=formulario.cleaned_data.get('usuariotelefono')

            if textoBusqueda is not None:
                QSusuarios = QSusuarios.filter(Q(nombre_usuario__contains=textoBusqueda) | Q(ciudad__contains=textoBusqueda) | Q(email__contains=textoBusqueda) | Q(apellidos__contains=textoBusqueda))
                mensaje+=" Contiene: "+ textoBusqueda+"\n"
            if usuariotelefono is not None:
                QSusuarios= QSusuarios.filter(telefono__startswith=usuariotelefono)
                mensaje+= str(usuariotelefono)+"\n"
            usuarios=QSusuarios.all()

            return render(request,'usuario/lista_busqueda.html',{"usuarios_mostrar":usuarios})
    else:
        formulario = BusquedaAvanzadaUsuario(None)
    return render(request,'usuario/busqueda.html',{"formulario":formulario})


'''
@permission_required('Huerto.view_gastos')
def gasto_lista(request):
    gastos=Gastos.objects.select_related('usuario')
    gastos=gastos.all()
    return render(request,'gastos/gastolista.html',{'gastos':gastos})
@permission_required('Huerto.add_gastos')
def gastos_create_simple(request):
    datosFormulario = None
    if request.method=="POST":
        datosFormulario = request.POST
    
    formulario = GastoModelForm(datosFormulario)
    if (request.method == "POST"):
        if formulario.is_valid():
            try:
                formulario.save()
                return redirect("gasto_lista") 
            except Exception as error:
                print(error)

    return render(request,'gastos/create.html',{'formulario':formulario})
@permission_required('Huerto.view_gastos')
def gasto_buscar(request):
    if(len(request.GET)>0):
        formulario= BusquedaAvanzadaGasto(request.GET)
        if formulario.is_valid():
            mensaje="Se ha buscado por:\n"
            QSgastos=Gastos.objects.select_related('usuario')
#cuando busco por gasto_busqueda si recibo resultados, pero con texto no
            gasto_busqueda=formulario.cleaned_data.get('gasto_busqueda')
            texto_busqueda=formulario.cleaned_data.get('texto_busqueda')

            if str(gasto_busqueda) !="":
                QSgastos = QSgastos.filter(Q(herramientas=gasto_busqueda) | Q(facturas=gasto_busqueda) | Q(imprevistos=gasto_busqueda))
                mensaje+=" Contiene: "+ str(gasto_busqueda)+"\n"
            if texto_busqueda != "":
                QSgastos = QSgastos.filter(Descripcion__contains=texto_busqueda)
                mensaje+= texto_busqueda+"\n"
            gastos=QSgastos.all()

            return render(request,'gastos/lista_busqueda.html',{"gastos_mostrar":gastos})
    else:
        formulario = BusquedaAvanzadaGasto(None)
    return render(request,'gastos/busqueda.html',{"formulario":formulario})
@permission_required('Huerto.change_gastos')
def gastos_editar(request,id_gasto):
    gasto=Gastos.objects.get(id=id_gasto)

    datosFormulario=None

    if request.method =="POST":
        datosFormulario = request.POST
    
    formulario = GastoModelForm(datosFormulario,instance=gasto)

    if (request.method =="POST"):
        if formulario.is_valid():
            try:
                formulario.save()
                return redirect('gasto_lista')
            except Exception as error:
                print(error)
    return render(request, 'gastos/actualizar.html', {"formulario": formulario, "gasto": gasto})
@permission_required('Huerto.delete_gastos')
def gasto_eliminar(request,id_gasto):
    gasto= Gastos.objects.get(id=id_gasto)
    try:
        gasto.delete()
        messages.success(request,"se ha eliminado el gasto: "+gasto+' '+gasto.id)
    except Exception as error:
        print(error)
    return redirect('gasto_lista')

@permission_required('Huerto.view_blog')
def blog_lista(request):
    blogs=Blog.objects.select_related('usuario')
    blogs=blogs.all()
    return render(request,'blog/listablog.html',{'blogs':blogs})
@permission_required('Huerto.add_blog')
def blog_create_simple(request):
    datosFormulario = None
    if request.method=="POST":
        datosFormulario = request.POST
    
    formulario = BlogModelForm(datosFormulario,initial={"usuario":request.user.Usuario})
    if (request.method == "POST"):
        if formulario.is_valid():
            try:
                formulario.save()
                return redirect("blog_lista") 
            except Exception as error:
                print(error)

    return render(request,'blog/create.html',{'formulario':formulario})
@permission_required('Huerto.view_blog')
def blog_buscar(request):

    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaBlogForm(request.GET)
        if formulario.is_valid():
            
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            
            QSblog = Blog.objects.select_related("usuario")
            
            
            etiqueta = formulario.cleaned_data.get('etiqueta')
            publicacion = formulario.cleaned_data.get('publicacion')
            fecha_desde = formulario.cleaned_data.get('fecha_desde')
            fecha_hasta = formulario.cleaned_data.get('fecha_hasta')
            
        
            if(etiqueta != ""):
                QSblog = QSblog.filter(etiqueta__contains=etiqueta)
                mensaje_busqueda +=" Nombre o contenido que contengan la palabra "+etiqueta+"\n"
            
            if(len(publicacion) > 0):
                mensaje_busqueda +=" La etiqueta sea "+publicacion[0]
                filtroOR = Q(publicacion=publicacion[0])
                for publi in publicacion[1:]:
                    mensaje_busqueda += " o "+publicacion[1]
                    filtroOR |= Q(publi=publi)
                mensaje_busqueda += "\n"
                QSblog =  QSblog.filter(filtroOR)

            #Comprobamos fechas
            if(not fecha_desde is None):
                mensaje_busqueda +=" La fecha sea mayor a "+datetime.strftime(fecha_desde,'%d-%m-%Y')+"\n"
                QSblog = QSblog.filter(fecha__gte=fecha_desde)

            if(not fecha_hasta is None):
                mensaje_busqueda +=" La fecha sea menor a "+datetime.strftime(fecha_hasta,'%d-%m-%Y')+"\n"
                QSblog = QSblog.filter(fecha__lte=fecha_hasta)
            
            blogs = QSblog.all()
    
            return render(request, 'blog/lista_busqueda.html',{"blog_mostrar":blogs,"texto_busqueda":mensaje_busqueda})
    else:
        formulario = BusquedaAvanzadaBlogForm(None)
    return render(request, 'blog/busqueda_avanzada.html',{"formulario":formulario})
@permission_required('Huerto.change_blog')


def blog_editar(request,id_blog):
    blog=Blog.objects.get(id=id_blog)

    datosFormulario=None

    if request.method =="POST":
        datosFormulario = request.POST
    
    formulario = BlogModelForm(datosFormulario,instance=blog)

    if (request.method =="POST"):
        if formulario.is_valid():
            try:
                formulario.save()
                return redirect('blog_lista')
            except Exception as error:
                print(error)
    return render(request, 'blog/actualizar.html', {"formulario": formulario, "blog": blog})




@permission_required('Huerto.delete_blog')
def blog_eliminar(request,id_blog):
    blog= Blog.objects.get(id=id_blog)
    try:
        blog.delete()
        messages.success(request,"se ha eliminado el gasto: "+blog+' '+blog.id)
    except Exception as error:
        print(error)
    return redirect('blog_lista')

@permission_required('Huerto.view_incidencia')
def incidencia_lista(request):
    incidencias=Incidencia.objects.select_related('huerto')
    incidencias=incidencias.all()
    return render(request,'incidencia/lista.html',{'incidencias_mostrar':incidencias})
@permission_required('Huerto.view_incidencia')
def incidencia_mostrar(request,id_incidencia):
    incidencia=Incidencia.objects.select_related('huerto')
    incidencia=incidencia.get(id=id_incidencia)
    return render(request,'incidencia/incidencia_mostrar.html',{'incidencia':incidencia})
@permission_required('Huerto.add_incidencia')
def incidencia_create_sencillo(request):
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
        
    formulario = IncidenciaModelForm(datosFormulario)
    if (request.method == "POST"):
        if formulario.is_valid():
            try:
                
                formulario.save()
                return redirect("incidencia_lista")
            except Exception as error:
                print(error)
    
    return render(request, 'incidencia/create.html',{"formulario":formulario})
@permission_required('Huerto.view_incidencia')
def incidencia_buscar_avanzado(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaIncidenciaForm(request.GET)
        if formulario.is_valid():
            
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            
            QSinc = Incidencia.objects.select_related("huerto")
            
    
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            fechaDesde = formulario.cleaned_data.get('fecha_desde')
            fechaHasta = formulario.cleaned_data.get('fecha_hasta')
            
            
            if(textoBusqueda != ""):
                QSinc = QSinc.filter(descripcion__contains=textoBusqueda)
                mensaje_busqueda +=" Contenido que contengan la palabra "+textoBusqueda+"\n"
            
            #Comprobamos fechas

            if(not fechaDesde is None):
                mensaje_busqueda +=" La fecha sea mayor a "+datetime.strftime(fechaDesde,'%d-%m-%Y')+"\n"
                QSinc = QSinc.filter(fecha_incidencia__gte=fechaDesde)
            

            if(not fechaHasta is None):
                mensaje_busqueda +=" La fecha sea menor a "+datetime.strftime(fechaHasta,'%d-%m-%Y')+"\n"
                QSinc = QSinc.filter(fecha_incidencia__lte=fechaHasta)
            
            incidencias = QSinc.all()
    
            return render(request, 'incidencia/lista_busqueda.html',
                            {"incidencia_mostrar":incidencias,
                            "texto_busqueda":mensaje_busqueda})
    else:
        formulario = BusquedaAvanzadaIncidenciaForm(None)
    return render(request, 'incidencia/busqueda_avanzada.html',{"formulario":formulario})
@permission_required('Huerto.change_incidencia')
def incidencia_editar(request,incidencia_id):
    incidencia = Incidencia.objects.get(id=incidencia_id)
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    formulario = IncidenciaModelForm(datosFormulario,instance = incidencia)
    if (request.method == "POST"):
        if formulario.is_valid():
            try:  
                formulario.save()
                messages.success(request, 'Se ha editado la incidencia correctamente')
                return redirect('incidencia_lista')  
            except Exception as error:
                print(error)
    return render(request, 'incidencia/actualizar.html',{"formulario":formulario,"incidencia":incidencia})
    
@permission_required('Huerto.delete_incidencia')
def incidencia_eliminar(request,incidencia_id):
    incidencia = Incidencia.objects.get(id=incidencia_id)
    try:
        incidencia.delete()
        messages.success(request, "Se ha elimnado el libro "+incidencia.id+" correctamente")
    except Exception as error:
        print(error)
    return redirect('incidencia_lista')

@permission_required('Huerto.view_fruto')
def fruto_lista(request):
    frutos=Fruto.objects.select_related('planta')
    frutos=frutos.all()
    return render(request,'fruto/lista.html',{'fruto_mostrar':frutos})
def fruto_create(request):
    
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
        
    formulario = FrutoModelForm(datosFormulario)
    if (request.method == "POST"):
        if formulario.is_valid():
            try:
                
                formulario.save()
                return redirect("fruto_lista")
            except Exception as error:
                print(error)
    
    return render(request, 'fruto/create.html',{"formulario":formulario})
@permission_required('Huerto.view_fruto')
def fruto_buscar(request):

    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaFrutoForm(request.GET)
        if formulario.is_valid():
            
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            
            QSfruto = Fruto.objects.select_related("fruto")
            
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            plant = formulario.cleaned_data.get('plant')
            
            if(textoBusqueda != ""):
                QSfruto = QSfruto.filter(Q(nombre__contains=textoBusqueda) | Q(tipo=textoBusqueda))
                mensaje_busqueda +=" Nombre o tipo que contengan la palabra "+textoBusqueda+"\n"
            if (plant != None):
                QSfruto=QSfruto.filter(planta=plant)
                mensaje_busqueda += "Id de la planta"

            
            frutos = QSfruto.all()
    
            return render(request, 'fruto/fruto_busqueda.html',
                            {"frutos_mostrar":frutos,
                            "texto_busqueda":mensaje_busqueda})
    else:
        formulario = BusquedaAvanzadaFrutoForm(None)
    return render(request, 'fruto/busqueda_avanzada.html',{"formulario":formulario})
@permission_required('Huerto.change_fruto')
def fruto_editar(request,fruto_id):
    fruto = Fruto.objects.get(id=fruto_id)
    
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    
    formulario = FrutoModelForm(datosFormulario,instance = fruto)
    
    if (request.method == "POST"):
    
        if formulario.is_valid():
            try:  
                formulario.save()
                messages.success(request, 'Se ha editado el registro')
                return redirect('fruto_lista')  
            except Exception as error:
                print(error)
        else:
            print(formulario.errors)
    return render(request, 'fruto/actualizar.html',{"formulario":formulario,"fruto":fruto})
    
@permission_required('Huerto.delete_fruto')
def fruto_eliminar(request,fruto_id):
    fruto = Fruto.objects.get(id=fruto_id)
    try:
        fruto.delete()
        messages.success(request, "Se ha elimnado el registro correctamente")
    except Exception as error:
        print(error)
    return redirect('fruto_lista')
@permission_required('Huerto.view_tratamiento')
def tratamiento_lista(request):
    tratamientos=Tratamiento.objects.prefetch_related('plaga')
    tratamientos=tratamientos.all()
    return render(request,'tratamiento/lista.html',{'tratamiento_mostrar':tratamientos})
@permission_required('Huerto.view_tratamiento')
def tratamiento_mostrar(request,tratamiento_id):
    tratamientos = Tratamiento.objects.prefetch_related("plaga")
    tratamientos = tratamientos.get(id=tratamiento_id)
    return render(request, 'tratamiento/tratamiento_mostrar.html',{"tratamientos":tratamientos})
@permission_required('Huerto.add_tratamiento')
def tratamiento_create(request):
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
        
    formulario = TratamientoModelForm(datosFormulario)
    
    if request.method == "POST":
        if formulario.is_valid():
            try:
                formulario.save()
                return redirect('tratamiento_lista')
            except Exception as error:
                print(error)
    
    return render(request, 'tratamiento/create.html', {"formulario": formulario})
@permission_required('Huerto.view_tratamiento')
def tratamiento_buscar(request):

    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaTratamientoForm(request.GET)
        if formulario.is_valid():
            
            mensaje_busqueda = "Se ha buscado por los siguientes valores:\n"
            
            QStrat = Tratamiento.objects.prefetch_related("plaga")
            
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            if(textoBusqueda != ""):
                QStrat = QStrat.filter(Q(descripcion__contains=textoBusqueda) | Q(consejos__contains=textoBusqueda)| Q(aplicacion__contains=textoBusqueda))
                mensaje_busqueda +=" Consejo, forma de aplicación o descripción que contengan la palabra "+textoBusqueda+"\n"
            tratamientos = QStrat.all()
            return render(request, 'tratamiento/lista_busqueda.html',
                            {"tratamiento_mostrar":tratamientos,
                            "texto_busqueda":mensaje_busqueda})
    else:
        formulario = BusquedaAvanzadaTratamientoForm(None)
    return render(request, 'tratamiento/busqueda_avanzada.html',{"formulario":formulario})
@permission_required('Huerto.change_tratamiento')
def tratamiento_actualizar(request,tratamiento_id):
    tratamiento = Tratamiento.objects.get(id=tratamiento_id)
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
    formulario = TratamientoModelForm(datosFormulario,instance = tratamiento)
    if (request.method == "POST"):
        if formulario.is_valid():
            try:  
                formulario.save()
                messages.success(request, 'Se ha editado el objeto')
                return redirect('tratamiento_lista')  
            except Exception as error:
                print(error)
    return render(request, 'tratamiento/actualizar.html',{"formulario":formulario,"tratamiento":tratamiento})
@permission_required('Huerto.delete_tratamiento')
def tratamiento_eliminar(request,tratamiento_id):
    tratamiento = Tratamiento.objects.get(id=tratamiento_id)
    try:
        tratamiento.delete()
        messages.success(request, "Se ha elimnado el objeto")
    except Exception as error:
        print(error)
    return redirect('tratamiento_lista')

def registrar_usuario(request):
    if request.method == 'POST':
        formulario = RegistroForm(request.POST)
        if formulario.is_valid():
            user = formulario.save()
            rol = int(formulario.cleaned_data.get('rol'))
            if(rol == Usuario.USU):
                grupo = Group.objects.get(name='Usu') 
                grupo.user_set.add(user)
                usu = Usu.objects.create( usuario = user)
                usu.save()
            elif(rol == Usuario.USU_PREMIUM):
                grupo = Group.objects.get(name='Usu_premium') 
                grupo.user_set.add(user)
                usu_premium = Usu_premium.objects.create(usuario = user)
                usu_premium.save()
            
            login(request, user)
            return redirect('index')
    else:
        formulario = RegistroForm()
    return render(request, 'registration/signup.html', {'formulario': formulario})


#Examen 14 diciembre

def promocion_create(request):
    datosFormulario = None
    if request.method=="POST":
        datosFormulario = request.POST
    
    formulario = PromocionModelForm(datosFormulario)
    if (request.method == "POST"):
        if formulario.is_valid():
            try:
                formulario.save()
                return redirect("promocion_lista") #es la url de nav no el nombre de la view
            except Exception as error:
                print(error)

    return render(request,'promocion/create.html',{'formulario':formulario})


def promocion_buscar(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaPromocion(request.GET)
        if formulario.is_valid():
            mensaje = "Se ha buscado por:\n"
            QStexto = Promocion.objects.select_related('usuario')

            texto = formulario.cleaned_data.get('texto')
            descuentoMayor = formulario.cleaned_data.get('descuentoMayor')
            fechaIn = formulario.cleaned_data.get('fechaIn')
            fechaFi = formulario.cleaned_data.get('fechaFi')

            if texto != "":
                QStexto = QStexto.filter(Q(descripcion=texto) | Q(nombre_promocion=texto))
                mensaje += texto + "\n"
            if str(descuentoMayor) != "":
                QStexto = QStexto.filter(descuento__gte=descuentoMayor)
                mensaje += str(descuentoMayor)

            if not fechaIn is None:
                mensaje += " La fecha sea mayor a " + datetime.strftime(fechaIn, '%d-%m-%Y') + "\n"
                QStexto = QStexto.filter(fecha_promocion__gte=fechaIn)

            # Obtenemos los libros con fecha publicación menor a la fecha desde
            if not fechaFi is None:
                mensaje += " La fecha sea menor a " + datetime.strftime(fechaFi, '%d-%m-%Y') + "\n"
                QStexto = QStexto.filter(fecha_promocion__lte=fechaFi)

            promocion = QStexto.all()
            return render(request, 'promocion/promocionlista.html', {"promocion_mostrar": promocion, "mensaje": mensaje})
    else:
        formulario = BusquedaAvanzadaPromocion(None)
    return render(request, 'promocion/busqueda.html', {"formulario": formulario})


def promocion_editar(request,id_promocion):
    promocion=Promocion.objects.get(id=id_promocion)

    datosFormulario=None

    if request.method =="POST":
        datosFormulario = request.POST
    
    formulario = PromocionModelForm(datosFormulario,instance=promocion)

    if (request.method =="POST"):
        if formulario.is_valid():
            try:
                formulario.save()
                return redirect('promocion_lista')
            except Exception as error:
                print(error)
    return render(request, 'promocion/editar.html', {"formulario": formulario, "promocion": promocion})


def promocion_eliminar(request,id_promocion):
    promocion= Promocion.objects.get(id=id_promocion)
    try:
        promocion.delete()
        messages.success(request,"se ha eliminado el gasto: "+promocion+' '+promocion.id)
    except Exception as error:
        print(error)
    return redirect('promocion_lista')

def promocion_lista(request):
    promocion=Promocion.objects.select_related('usuario')
    promocion=promocion.all()
    return render(request,'promocion/promocionlista.html',{'promocion':promocion})




from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView

class TokenObtainView(APIView):
    def post(self, request, *args, **kwargs):
        # Obtén el nombre de usuario y la contraseña de la solicitud POST
        username = request.data.get('username')
        password = request.data.get('password')

        # Realiza la autenticación del usuario (puedes personalizar esto según tus necesidades)
        user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            # Si la autenticación es exitosa, crea un token de acceso y actualización
            refresh = RefreshToken.for_user(user)

            # Accede al token de acceso y al token de actualización
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Devuelve los tokens en la respuesta
            return Response({
                'access_token': access_token,
                'refresh_token': refresh_token,
            }, status=status.HTTP_200_OK)
        else:
            # Si la autenticación falla, devuelve un error
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

