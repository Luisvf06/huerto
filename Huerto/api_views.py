from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import *

@api_view(['GET'])
def huerto_list(request):
    huertos=Huerto.objects.all()
    serializer = HuertoSerializerMejorado(huertos,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def huerto_buscar(request):
    huertos=Huerto.objects.all()
    serializer=HuertoSerializerMejorado(huertos,many=True)
    return Response(serializer.data)

def huerto_buscar_cl(request):
    formulario=BusquedaHuerto(request.GET)
    headers={'Authorization': 'Bearer OjSzCkAWynmruDYbzT7MV4QAmavcV9'}
    response = requests.get('http://127.0.0.1:4999/api/v1/huertos',headers=headers,params=formulario.data)
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