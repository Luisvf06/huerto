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
                QShuerto=QShuerto.filter(area__gte=float(area_minima))
            if not area_maxima is None:
                QShuerto=QShuerto.filter(area__lte=float(area_maxima))
            
            huertos=QShuerto.all()
            serializer=HuertoSerializerMejorado(huertos,many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors,status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def gastos_buscar_avanzado(request):
    if(len(request.GET)>0):
        formulario= BusquedaAvanzadaGasto(request.GET)
        if formulario.is_valid():
            QSgastos=Gastos.objects.select_related('usuario')
            gasto_busqueda=formulario.cleaned_data.get('gasto_busqueda')
            texto_busqueda=formulario.cleaned_data.get('texto_busqueda')
            if not gasto_busqueda is None:
                QSgastos = QSgastos.filter(Q(herramientas=gasto_busqueda) | Q(facturas=gasto_busqueda) | Q(imprevistos=gasto_busqueda))
            if texto_busqueda != "":
                QSgastos = QSgastos.filter(Descripcion__contains=texto_busqueda)
            gastos=QSgastos.all()
            serializer=GastosSerializerMejorado(gastos,many=True)
            return Response(serializer.data)
        else:
            return Response (formulario.errors,status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def blog_buscar_avanzado(request):
    if(len(request.GET)>0):
        formulario= BusquedaAvanzadaBlogForm(request.GET)
        if formulario.is_valid():
            QSBlog=Blog.objects.select_related('usuario')
            etiqueta=formulario.cleaned_data.get('etiqueta')
            publicacion = formulario.cleaned_data.get('publicacion')
            fecha_desde = formulario.cleaned_data.get('fecha_desde')
            fecha_hasta = formulario.cleaned_data.get('fecha_hasta')
            if(etiqueta != ""):
                QSBlog = QSBlog.filter(etiqueta__contains=etiqueta)
                
            if(len(publicacion) > 0):
                filtroOR = Q(publicacion=publicacion[0])
                for publi in publicacion[1:]:
                    filtroOR |= Q(publi=publi)
                QSBlog =  QSBlog.filter(filtroOR)

            #Comprobamos fechas
            if(not fecha_desde is None):
                QSBlog = QSBlog.filter(fecha__gte=fecha_desde)

            if(not fecha_hasta is None):
                QSBlog = QSBlog.filter(fecha__lte=fecha_hasta)
            
            blogs = QSBlog.all()
            serializer=BlogSerializerMejorado(blogs,many=True)
            return Response(serializer.data)
        else:
            return Response (formulario.errors,status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def huerto_obtener(request,huerto_id):
    huerto=Huerto.objects.prefetch_related('usuario')
    huerto=huerto.get(id=huerto_id)
    serializer=HuertoSerializerMejorado(huerto)
    return Response(serializer.data)

@api_view(['GET'])
def gasto_obtener(request,gasto_id):
    gasto=Gastos.objects.select_related('usuario')
    gasto=gasto.get(id=gasto_id)
    serializer=GastosSerializerMejorado(gasto)
    return Response(serializer.data)

@api_view(['GET'])
def blog_obtener(request,blog_id):
    blog=Blog.objects.select_related('usuario')
    blog=blog.get(id=blog_id)
    serializer=GastosSerializerMejorado(blog)
    return Response(serializer.data)

@api_view(['GET'])
def usuario_list(request):
    usuarios=Usuario.objects.all()
    serializer=UsuarioSerializer(usuarios,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def huerto_crear(request):
    serializers= HuertoSerializerCreate(data=request.data)
    if serializers.is_valid():
        try:
            
            serializers.save()
            return Response("Huerto creado")
        except Exception as error:
            return Response(error,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def gasto_crear(request):
    print(request.data)
    gastosSerializer=GastoSerializerCreate(data=request.data)
    if gastosSerializer.is_valid():
        try:
            gastosSerializer.save()
            return Response("Gasto creado")
        
        except serializers.ValidationError as error:
            return Response(error.detail,status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(gastosSerializer.errors,status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
def huerto_eliminar(request,huerto_id):
    huerto=Huerto.objects.get(id=huerto_id)
    try:
        huerto.delete()
        return Response("Huerto eliminado")
    except Exception as error:
        return Response (error,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def gastos_eliminar(request,gastos_id):
    gastos=Gastos.objects.get(id=gastos_id)
    try:
        gastos.delete()
        return Response("Gastos eliminado")
    except Exception as error:
        return Response (error,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def blog_eliminar(request,blog_id):
    blog=Blog.objects.get(id=blog_id)
    try:
        blog.delete()
        return Response("Blog eliminado")
    except Exception as error:
        return Response (error,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def blog_crear(request):
    print(request.data)
    blogSerializer=BlogSerializerCreate(data=request.data)
    if blogSerializer.is_valid():
        try:
            blogSerializer.save()
            return Response("Blog creado")
        except serializers.ValidationError as error:
            return Response(error.detail,status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(blogSerializer.errors,status=status.HTTP_400_BAD_REQUEST)
