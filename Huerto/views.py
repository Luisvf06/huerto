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
# Create your views here.
def index(request):
    return render(request,'index.html')

#devuelve las plantas que se encuentran en un huerto determinado
def lista_planta_huerto(request,id_huerto):
    plantas=Planta.objects.select_related('huerto')
    plantas=plantas.filter(huerto=id_huerto)
    return render(request,'planta/listaplanta.html',{'plantas_huerto':plantas})

#devuelve la fecha de la ultima modificacion de la contraseña, de un usuario. La idea original era sacar sólo la última contraseña porque pensaba que el campo era fecha_modificacion y no ultima_... he intentado cambiarlo pero no he encontrado ningún field de tipo lista en la documentación, por eso añado id_usuario
def ultima_modificacion(request,id_usuario):
    contras=Contrasenha.objects.select_related('usuario')
    contras=contras.filter(usuario=id_usuario)#.order_by('-ultima_modificacion')[:1].get()
    return render(request,'contrasenha/listacontra.html',{'modificaciones':contras})

#devuelve el gasto que ha supuesto un determinado huerto en un año
def gasto_huerto(request,id_huerto,anho_gasto):
    gastos=Gastos.objects.select_related('usuario')
    gastos=gastos.filter(Q(usuario__usuario_huerto=id_huerto) & Q(fecha__year=anho_gasto))
    return render(request,'gastos/listagasto.html',{'gasto_total':gastos})

#devuelve los usuarios que tengan un huerto de tipo parcela y cuyo apellido empiece por una letra concreto
def usuarios_parcelas(request,inicial):
    usuarios=Usuario.objects.prefetch_related(Prefetch('usuario_huerto'))
    usuarios=usuarios.filter(Q(usuario_huerto__sitio='P') & Q(apellidos__startswith=inicial))
    return render(request, 'usuario/listausuario.html',{'usuarios_parcelas':usuarios})

#devuelve las plagas de una planta junto a su fecha y descripcion
def plaga_planta(request,plant):
    plagas=Plaga.objects.select_related('planta').prefetch_related(Prefetch('plaga_plant'))
    plagas=plagas.filter(planta__nombre_comun=plant)
    return render(request,'plaga/listaplaga.html',{'histo_plaga':plagas})

#devuelve los consejos de tratamiento para cada planta cuando la infeccion es por hongo

def consejo_plaga(request):
    consejos=Tratamiento.objects.prefetch_related('plaga')
    consejos=consejos.filter(plaga__origen='F')
    return render(request,'tratamiento/listatratamiento.html',{'infeccionhongos':consejos})

#devuelve la ciudad y los gastos de los usuarios que han estito noticias (N) en el blog y no han usado etiquetas
def usuario_noticia(request):
    usuarios=Usuario.objects.prefetch_related(Prefetch('usuario_gasto')).prefetch_related(Prefetch('usuario_blog'))
    usuarios=usuarios.filter(Q(usuario_blog__etiqueta=None)&Q(usuario_blog__publicacion='N'))
    return render(request,'usuario/listausuario.html',{'usuario_noticias':usuarios})

#devuelve las plantas que crecen en ph entre 4 y 8 y necesitan mas de 6 horas de luz al dia
def planta_phluz(request,mi,ma,lu):
    plantas=Planta.objects.prefetch_related('huerto')
    plantas=plantas.filter(Q(phmax__lte=ma)& Q(phmin__gte=mi) &Q(horas_luz__gt=lu))
    return render(request,'planta/listaplanta2.html',{'requisitos':plantas})

#devuelve la indicencia mas reciente
def incidencia_reciente(request):
    incidencias=Incidencia.objects.prefetch_related('huerto')
    incidencias=incidencias.order_by("fecha_incidencia")[:1].get()
    return render(request,'huerto/mostrar_incidencia.html',{'incidenciahuerto':incidencias})

#devuelve los huertos que no han tenido incidencias
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
def ultimo_voto_huerto(request,id_huerto):
    voto=Votacion.objects.select_related('huerto','usuario')
    voto=voto.filter(huerto=id_huerto).order_by('fecha_voto')[:1].get
    return render(request,'votacion/votacion.html',{'voto':voto})
#Ejercicio 2
def voto_mas_tres(request, id_usuario):
    votos=Votacion.objects.select_related('huerto','usuario')
    votos=votos.filter(Q(usuario=id_usuario) &Q(puntuacion__gte=3))
    return render(request,'votacion/ejercicio2.html',{'totalvotos':votos})
#Ejercicio 3
def no_voto(request):
    usuarios=Usuario.objects.prefetch_related(Prefetch('usuario_voto'))
    usuarios=usuarios.filter(usuario_voto=None)
    return render (request, 'usuario/ejercicio3.html',{'sin_votos':usuarios})

#Ejercicio 4
def cuenta_usuario(request,nombreu):
    cuentas=Banco.objects.select_related('usuario')
    cuentas=cuentas.filter(Q(usuario__nombre__contains=nombreu) | Q(banco='C')| Q(banco='U'))
    return render(request,'cuenta/listacuenta.html',{'cuentas_usu':cuentas})

#Ejercicio 5
def media_doscinco(request):
    Huerto.objects.aggregate(Avg('huerto_voto',default=0))
    huertos=Huerto.objects.prefetch_related(Prefetch('huerto_voto'))

    huertos=huertos.filter(huerto_voto__gte=2.5)
    return render(request,'votacion/ejercicio5.html',{'nombre':huertos})
    

#Formularios
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

def crear_huerto_modelo(formulario):
    huerto_creado=False
    if formulario.is_valid():
        try:
            formulario.save()
            huerto_creado=True
        except Exception as error:
            print(error)
    return huerto_creado

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
    
def huerto_buscar_avanzado(request):
    if (len(request.GET)>0):
        formulario=BusquedaAvanzadaHuerto(request.GET)
        if formulario.is_valid():
            mensaje_busqueda="Se ha buscado por:\n"
            QShuerto=Huerto.objects.prefetch_related("usuario")

            area_maxima=formulario.cleaned_data.get("area_maxima")
            area_minima=formulario.cleaned_data.get("area_minima")
            usuario_id = formulario.cleaned_data.get("usuario")
            if usuario_id is not None:
                formulario.fields['usuario'].initial = usuario_id
            else:
                formulario.fields['usuario'].initial = None

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
                return redirect('listahuertos')
            except Exception as e:
                pass
    return render(request,'huerto/actualizar.html',{'formulario':formulario,'huerto':huerto})

def huerto_eliminar(request,huerto_id):
    huerto=Huerto.objects.get(id=huerto_id)
    try:
        huerto.delete()
        messages.success(request,"se ha eliminado el huerto"+huerto.id)
    except Exception as error:
        print(error)
    return redirect('listahuertos')


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

def gasto_lista(request):
    gastos=Gastos.objects.select_related('usuario')
    gastos=gastos.all()
    return render(request,'gastos/gastolista.html',{'gastos':gastos})

def gastos_create_simple(request):
    datosFormulario = None
    if request.method=="POST":
        datosFormulario = request.POST
    
    formulario = GastoModelForm(datosFormulario)
    if (request.method == "POST"):
        if formulario.is_valid():
            try:
                formulario.save()
                return redirect("gastos_lista") #es la url de nav no el nombre de la view
            except Exception as error:
                print(error)

    return render(request,'gastos/create.html',{'formulario':formulario})

def gasto_buscar(request):
    if(len(request.GET)>0):
        formulario= BusquedaAvanzadaGasto(request.GET)
        if formulario.is_valid():
            mensaje="Se ha buscado por:\n"
            QSgastos=Gastos.objects.select_related('usuario')

            gasto_busqueda=formulario.cleaned_data.get('gasto_busqueda')
            texto_busqueda=formulario.cleaned_data.get('texto_busqueda')

            if str(gasto_busqueda) !="":
                QSgastos = QSgastos.filter(Q(herramientas=gasto_busqueda) | Q(facturas=gasto_busqueda) | Q(imprevistos=gasto_busqueda))
                mensaje+=" Contiene: "+ str(gasto_busqueda)+"\n"
            if texto_busqueda != "":
                QSusuarios= QSusuarios.filter(descripcion=texto_busqueda)
                mensaje+= texto_busqueda+"\n"
            gastos=QSgastos.all()

            return render(request,'gastos/lista_busqueda.html',{"gastos_mostrar":gastos})
    else:
        formulario = BusquedaAvanzadaGasto(None)
    return render(request,'gastos/busqueda.html',{"formulario":formulario})

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


def gasto_eliminar(request,id_gasto):
    gasto= Gastos.objects.get(id=id_gasto)
    try:
        gasto.delete()
        messages.success(request,"se ha eliminado el gasto: "+gasto+' '+gasto.id)
    except Exception as error:
        print(error)
    return redirect('gastos_lista')


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