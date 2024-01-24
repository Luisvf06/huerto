from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .forms import *
from django.db.models import Q,Prefetch

@api_view(['GET'])
def huerto_list(request):
    huertos=Huerto.objects.all()
    serializer = HuertoSerializerMejorado(huertos,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def huerto_buscar(request):
    if(request.user.has_perm("Huerto.view_huerto")):
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
    else:
        return Response({"Sin permisos"},status=status.HTTP_400_BAD_REQUEST)
