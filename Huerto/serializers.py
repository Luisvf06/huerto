from .models import *
from rest_framework import serializers
'''
class HuertoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Huerto
        fields= '__all__'
'''        

        
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class HuertoSerializerMejorado(serializers.ModelSerializer):
    sitio=serializers.CharField(source='get_sitio_display')
    sustrato=serializers.CharField(source='get_sustrato_display')
    usuario=UsuarioSerializer(read_only=True, many=True)
    
    class Meta:
        model = Huerto
        fields =  ('ubicacion','sitio','sustrato','area','acidez','abonado','usuario')
