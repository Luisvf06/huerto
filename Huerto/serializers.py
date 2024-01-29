from .models import *
from rest_framework import serializers

class HuertoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Huerto
        fields= '__all__'
    

        
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class HuertoSerializerMejorado(serializers.ModelSerializer):
    sitio=serializers.CharField(source='get_sitio_display')
    sustrato=serializers.CharField(source='get_sustrato_display')
    usuario=UsuarioSerializer(read_only=True, many=True)
    
    class Meta:
        fields =  ('id','ubicacion','sitio','sustrato','area','acidez','abonado','usuario')
        model = Huerto

class GastosSerializerMejorado(serializers.ModelSerializer):
    fecha = serializers.DateField(format=('%d-%m-%Y'))
    usuario=UsuarioSerializer()

    class Meta:
        fields =('herramientas',
                'facturas',
                'imprevistos',
                'Descripcion',
                'fecha',
                'usuario')
        model = Gastos

class BlogSerializerMejorado(serializers.ModelSerializer):
    publicacion=serializers.CharField(source='get_publicacion_display')
    fecha=serializers.DateField(format=('%d-%m-%Y'))
    usuario=UsuarioSerializer()

    class Meta:
        fields=('publicacion',
                'fecha',
                'etiqueta',
                'usuario')
        model=Gastos
