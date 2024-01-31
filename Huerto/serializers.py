from .models import *
from rest_framework import serializers
import re
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
        

class HuertoSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model =Huerto
        fields = ['ubicacion','sitio','sustrato','area','acidez','abobado']
        
    def validate_ubicacion(self,ubicacion): #entiendo que la validacion es la misma que en la de los formularios normales, pero no estoy seguro
        if ubicacion is not None:
            ubicacion=ubicacion.split(",")
            if not (-90 <= float(ubicacion[0]) <= 90):
                self.add_error('ubicacion', 'La latitud debe estar entre -90 y 90')
            if not (-180 <= float(ubicacion[1]) <= 180):
                self.add_error('ubicacion', 'La longitud debe estar entre -180 y 180')
    def validate_sitio(self,sitio):
        if sitio is not None and len(sitio)<1:
            self.add_error('sitio','Elige una opción')
    
    def validate_sustrato(self,sustrato):
        if sustrato is not None and len(sustrato)<1:
            self.add_error('sustrato','Elige una opción')

    def validate_area(self,area):
        
        if not (re.match(r'\d+\.?\d*$',str(area)) and area>0):
            self.add_error('area','debe ser un número mayor que 0')

    def validate_acidez(self,acidez):
        if acidez is None:
            self.add_error('acidez', 'Este campo no puede estar en blanco')
        elif not (re.match(r'\d+\.?\d*$', str(acidez))):
            self.add_error('acidez', 'debe ser un número entre 0 y 14')
        elif not (0 < acidez < 14):
            self.add_error('acidez', 'debe ser un número entre 0 y 14')

