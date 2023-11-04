from django.shortcuts import render
from .models import Planta
from .models import Blog
from .models import Usuario
from .models import Huerto
from .models import Incidencia
from .models import Contrasenha
from .models import Gastos
from .models import Fruto
from .models import Historial
from .models import Plaga
from .models import Evento
from .models import Planta_regada
from .models import Calendario
from .models import Riego
from .models import Tratamiento
from django.views.defaults import page_not_found
from django.views.defaults import bad_request
from django.views.defaults import server_error
from django.views.defaults import permission_denied
from django.db.models import Q, Prefetch
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
    return render(request,'planta/listaplanta.html',{'requisitos':plantas})

#devuelve la indicencia mas reciente
def incidencia_reciente(request):
    incidencias=Incidencia.objects.prefetch_related('huerto')
    incidencias=incidencias.order_by("fecha_incidencia")[:1].get()
    return render(request,'huerto/listahuerto.html',{'incidenciahuerto':incidencias})

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
