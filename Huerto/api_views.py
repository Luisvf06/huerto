from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .forms import *
from django.db.models import Q,Prefetch
from requests.exceptions import HTTPError
# views.py



@api_view(['GET'])
def huerto_list(request):
    huertos=Huerto.objects.all()
    serializer = HuertoSerializer(huertos,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def huerto_lista_mejorada(request):
    huertos=Huerto.objects.all()
    serializer = HuertoSerializerMejorado(huertos,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def gasto_list(request):
    gastos=Gastos.objects.select_related('usuario').all()
    serializer=GastosSerializerMejorado(gastos,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def blog_list(request):
    blogs=Blog.objects.select_related('usuario').all()
    serializer=BlogSerializerMejorado(blogs,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def huerto_buscar(request):
    #if(request.user.has_perm("Huerto.view_huerto")):
        formulario=BusquedaHuerto(request.query_params)
        if(formulario.is_valid()):
            texto=formulario.data.get('textoBusqueda')
            huertos = Huerto.objects.prefetch_related("usuario")
            print(huertos)
            huertos = huertos.filter(sitio__startswith=texto).all()
            serializer=HuertoSerializerMejorado(huertos,many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    #else:
    #    return Response({"Sin permisos"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def huerto_buscar_avanzado(request):
    
    if (len(request.query_params)>0):
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
            serializer=HuertoSerializerMejorado(huertos,many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors,status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def huerto_obtener(request,huerto_id):
    huerto=Huerto.objects.prefetch_related('usuario')
    huerto=huerto.get(id=huerto_id)
    serializer=HuertoSerializerMejorado(huerto)
    return Response(serializer.data)

@api_view(['GET'])
def usuario_list(request):
    usuarios=Usuario.objects.all()
    serializer=UsuarioSerializer(usuarios,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def huerto_crear(request):
    pass