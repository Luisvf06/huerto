from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .forms import *
from django.db.models import Q,Prefetch
from requests.exceptions import HTTPError
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group
from django.db.models import Q
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
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

from rest_framework import generics
from rest_framework.permissions import AllowAny

class registrar(generics.CreateAPIView):
    serializer_class = UsuarioSerializerRegistro
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializers = UsuarioSerializerRegistro(data=request.data)
        if serializers.is_valid():
            try:
                rol = request.data.get('rol')
                user = Usuario.objects.create_user(
                        username = serializers.data.get("username"), 
                        email = serializers.data.get("email"), 
                        password = serializers.data.get("password1"),
                        rol = rol,
                        )
                if(rol==Usuario.USU):
                    grupo=Group.objects.get(name='Usu')
                    grupo.user_set.add(user)
                    usu=Usu.objects.create(usuario=user)
                    usu.save()
                elif(rol==Usuario.USU_PREMIUM):
                    grupo=Group.objects.get(name="Usu_premium")
                    grupo.user_set.add(user)
                    usu_prem=Usu_premium.objects.create(usuario=user)
                    usu_prem.save()
                usuarioSerilizado=UsuarioSerializer(user)
                return Response(usuarioSerilizado.data)
            except Exception as error:
                return Response(repr(error),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

from oauth2_provider.models import AccessToken     
@api_view(['GET'])
def obtener_usuario_token(request,token):
    ModeloToken = AccessToken.objects.get(token=token)
    usuario = Usuario.objects.get(id=ModeloToken.id)
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)
    


@api_view(['PUT'])
def huerto_editar(request,huerto_id):
    huerto=Huerto.objects.get(id=huerto_id)
    huertoserializer=HuertoSerializerCreate(data=request.data,instance=huerto)
    if huertoserializer.is_valid():
        try:
            huertoserializer.save()
            return Response("Huerto editado")
        except serializers.ValidationError as error:
            return Response(error.detail,satus=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(huertoserializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT'])
def gasto_editar(request,gasto_id):
    gasto=Gastos.objects.get(id=gasto_id)
    gastoserializer=GastoSerializerCreate(data=request.data,instance=gasto)
    if gastoserializer.is_valid():
        try:
            gastoserializer.save()
            return Response("Gasto editado")
        except serializers.ValidationError as error:
            return Response(error.detail,satus=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(gastoserializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    

@api_view(['PUT'])
def blog_editar(request,blog_id):
    blog=Blog.objects.get(id=blog_id)
    blogserializer=BlogSerializerCreate(data=request.data,instance=blog)
    if blogserializer.is_valid():
        try:
            blogserializer.save()
            return Response("Blog editado")
        except serializers.ValidationError as error:
            return Response(error.detail,satus=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(blogserializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH'])
def huerto_editar_ubicacion(request,huerto_id):
    serializers = HuertoSerializerCreate(data=request.data)
    huerto = Huerto.objects.get(id=huerto_id)
    serializers = HuertoSerializerActualizarUbicacion(data=request.data,instance=huerto)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("Campo EDITADO")
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH'])
def huerto_editar_sitio(request,huerto_id):
    serializers = HuertoSerializerCreate(data=request.data)
    huerto = Huerto.objects.get(id=huerto_id)
    serializers = HuertoSerializerActualizarSitio(data=request.data,instance=huerto)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("Campo EDITADO")
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH'])
def huerto_editar_sustrato(request,huerto_id):
    serializers = HuertoSerializerCreate(data=request.data)
    huerto = Huerto.objects.get(id=huerto_id)
    serializers = HuertoSerializerActualizarSustrato(data=request.data,instance=huerto)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("Campo EDITADO")
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH'])
def huerto_editar_abonado(request,huerto_id):
    serializers = HuertoSerializerCreate(data=request.data)
    huerto = Huerto.objects.get(id=huerto_id)
    serializers = HuertoSerializerActualizarAbonado(data=request.data,instance=huerto)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("Campo EDITADO")
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def huerto_editar_area(request,huerto_id):
    serializers = HuertoSerializerCreate(data=request.data)
    huerto = Huerto.objects.get(id=huerto_id)
    serializers = HuertoSerializerActualizarArea(data=request.data,instance=huerto)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("Campo EDITADO")
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def huerto_editar_acidez(request,huerto_id):
    serializers = HuertoSerializerCreate(data=request.data)
    huerto = Huerto.objects.get(id=huerto_id)
    serializers = HuertoSerializerActualizarAcidez(data=request.data,instance=huerto)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("Campo EDITADO")
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH'])
def gasto_editar_factura(request,huerto_id):
    serializers = GastoSerializerCreate(data=request.data)
    huerto = Gastos.objects.get(id=huerto_id)
    serializers = GastoSerializerActualizarFactura(data=request.data,instance=huerto)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("Campo EDITADO")
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH'])
def gasto_editar_descripcion(request,huerto_id):
    serializers = GastoSerializerCreate(data=request.data)
    huerto = Gastos.objects.get(id=huerto_id)
    serializers = GastoSerializerActualizarDescripcion(data=request.data,instance=huerto)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("Campo EDITADO")
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH'])
def gasto_editar_herramientas(request,huerto_id):
    serializers = GastoSerializerCreate(data=request.data)
    huerto = Gastos.objects.get(id=huerto_id)
    serializers = GastoSerializerActualizarHerramientas(data=request.data,instance=huerto)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("Campo EDITADO")
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def gasto_editar_imprevistos(request,huerto_id):
    serializers = GastoSerializerCreate(data=request.data)
    huerto = Gastos.objects.get(id=huerto_id)
    serializers = GastoSerializerActualizarImprevistos(data=request.data,instance=huerto)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("Campo EDITADO")
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH'])
def gasto_editar_fecha(request,huerto_id):
    serializers = GastoSerializerCreate(data=request.data)
    huerto = Gastos.objects.get(id=huerto_id)
    serializers = GastoSerializerActualizarFecha(data=request.data,instance=huerto)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("Campo EDITADO")
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def blog_editar_fecha(request,huerto_id):
    serializers = BlogSerializerCreate(data=request.data)
    huerto = Blog.objects.get(id=huerto_id)
    serializers = BlogSerializerActualizarFecha(data=request.data,instance=huerto)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("Campo EDITADO")
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def blog_editar_publicacion(request,huerto_id):
    serializers = BlogSerializerCreate(data=request.data)
    huerto = Blog.objects.get(id=huerto_id)
    serializers = BlogSerializerActualizarPublicacion(data=request.data,instance=huerto)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("Campo EDITADO")
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def blog_editar_etiqueta(request,huerto_id):
    serializers = BlogSerializerCreate(data=request.data)
    huerto = Blog.objects.get(id=huerto_id)
    serializers = BlogSerializerActualizarEtiqueta(data=request.data,instance=huerto)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response("Campo EDITADO")
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

#Tarea Final

#Gabriela
@api_view(['GET'])
def plantas_estacion(request,estacion):
    if estacion=='primavera':
        plantas=Planta.objects.select_related('huerto')
        plantas=plantas.filter(Q(epoca_siembra__month__gte=3) &Q(epoca_siembra__month__lt=6))
        serializer = PlantaSerializerMejorado(plantas,many=True)
    elif estacion=='verano':
        plantas=Planta.objects.select_related('huerto')
        plantas=plantas.filter(Q(epoca_siembra__month__gte=6) &Q(epoca_siembra__month__lt=9))
        serializer = PlantaSerializerMejorado(plantas,many=True)
    elif estacion=='otoño':
        plantas=Planta.objects.select_related('huerto')
        plantas=plantas.filter(Q(epoca_siembra__month__gte=9) &Q(epoca_siembra__month__lt=12))
        serializer = PlantaSerializerMejorado(plantas,many=True)
    elif estacion=='invierno':
        plantas=Planta.objects.select_related('huerto')
        plantas=plantas.filter(Q(Q(epoca_siembra__month__gte=1) &Q(epoca_siembra__month__lt=3)) | Q(epoca_siembra__month__gte=12))
    serializer = PlantaSerializerMejorado(plantas,many=True)
    return Response(serializer.data)

#Manuel
@api_view(['GET'])
def huerto_disponible(request):
    huertos=Huerto.objects.prefetch_related('usuario')
    huertos=huertos.filter(disponible=True)
    serializer=HuertoSerializerMejorado(huertos,many=True)
    return Response(serializer.data)

#Irene
@api_view(['GET'])
def huerto_recolectable(request, id_huerto):

    huerto = Huerto.objects.prefetch_related(Prefetch("plantas_huerto")).get(id=id_huerto)
    serializer = HuertoSerializerMejorado(huerto, many=False)
    huerto_data = serializer.data

    hoy = datetime.now().date()
    dia_inicio = hoy - timedelta(days=5)
    dia_fin = hoy + timedelta(days=5)

    for planta in huerto_data['plantas_huerto']:
        fecha_recoleccion = datetime.strptime(planta['recoleccion'], '%Y-%m-%d').date()
        planta['es_recolectable'] = dia_inicio <= fecha_recoleccion <= dia_fin

    return Response(huerto_data)

#Alvaro
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

class FileUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileUploadSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            
            uploaded_file = serializer.validated_data["file"]
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

#Alberto

@api_view(['GET'])
def planta_regable(request, id_usuario):
    planta_riego = Planta_regada.objects.select_related('planta').filter(planta__huerto__usuario__id=id_usuario)
    serializer = PlantaRegadaSerializerMejorado(planta_riego, many=True)
    riego_data = serializer.data
    
    for planta in riego_data:
        #accede al ultimo riego de la planta, lo formatea y da un margen de 3 días
        ultimo_riego = datetime.strptime(planta['fecha'], '%d-%m-%Y').date()
        dia_recomendado = ultimo_riego + timedelta(days=3)
        #si la fecha actual es mayor que el plazo se recomienda el riego
        necesita_riego_hoy = datetime.now().date() >= dia_recomendado
        planta['regar'] = necesita_riego_hoy

    return Response(riego_data)
#esta y la siguiente son las vistas para obtener las pk y datos de los modelos riego y planta y pasarselo al modelo intermeidio
@api_view(['GET'])
def planta_list(request):
    plantas=Planta.objects.all()
    serializer=PlantaSerializerMejorado(plantas,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def riego_list(request):
    riegos=Riego.objects.all()
    serializer=RiegoSerializerMejorado(riegos,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def planta_regar(request):
    riegoCreateSerializer=RiegoPlantaSerializar(data=request.data)
    if riegoCreateSerializer.is_valid():
        try:
            riegoCreateSerializer.save()
            return Response("riego apuntado")
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(riegoCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def planta_obtener(request,planta_id):
    planta=Planta.objects.select_related('Huerto')
    planta=planta.get(id=planta_id)
    serializer=PlantaSerializerMejorado(planta)
    return Response(serializer.data)

@api_view(['GET'])
def riego_obtener(request,riego_id):
    riego=Riego.objects.select_related('Planta_riego')
    riego=Riego.get(id=riego_id)
    serializer=RiegoSerializerMejorado(riego)
    return Response(serializer.data)

@api_view(['PATCH'])
def actualizar_fecha_riego(request,id_plantariego):
    riegoFecha=Planta_regada.objects.get(id=id_plantariego)
    serializers=PlantaRiegoSerializerActualizarFecha(data=request.data,instance=riegoFecha)
    if (serializers.is_valid()):
        try:
            serializers.save()
            return Response("Fecha del último riego modificada")
        except Exception as error:
            print(repr(error))
            return Response(repr(error),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

#Iván
@api_view(['GET'])
def huerto_plagas(request, huerto_id):
    try:
        huerto = Huerto.objects.prefetch_related(
            Prefetch('plantas_huerto', queryset=Planta.objects.prefetch_related(
                Prefetch('plagaplanta_set', queryset=PlagaPlanta.objects.select_related('plaga'))
            ))
        ).get(id=huerto_id)
        
        total_plagas = PlagaPlanta.objects.filter(planta__huerto=huerto).count()

        serializer = HuertoSerializerMejorado(huerto)
        serialized_data = serializer.data
        serialized_data['total_plagas'] = total_plagas
        return Response(serialized_data)
    except Huerto.DoesNotExist:
        return Response({'error': 'Huerto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

def registro_google(request):
    pass