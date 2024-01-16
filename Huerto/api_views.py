from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import *

@api_view(['GET'])
def huerto_list(request):
    huertos=Huerto.objects.all()
    serializer = HuertoSerializer(huertos,many=True)
    return Response(serializer.data)