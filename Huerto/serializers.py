from .models import *
from rest_framework import serializers
class HuertoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Huerto
        fields= ['__all__']
    ubicacion=PlainLocationField()#atributo para almacenar coordenadas en forma de tupla de cadenas de 2 elementos(latitud,longitud)
    SITIO=[('M','maceta'),('J','jardin'),('T','terraza'),('P','parcela')]
    sitio=models.CharField(max_length=1,choices=SITIO)
    SUSTRATO=[('ARE','arenoso'),('ARC','arcilloso'),('LIM','limoso'),('FRA','franco'),('TUR','turbado')]
    sustrato=models.CharField(max_length=3,choices=SUSTRATO)
    area=models.FloatField(blank=True,null=True)
    acidez=models.FloatField(blank=True,null=True)
    abonado=models.BooleanField()#esto no sé si incluirlo aqui o no ya que es algo que se hace cada X tiempo, por lo que en ciertas ocasiones puede ser True y en otras False
    usuario=models.ManyToManyField(Usuario,related_name="usuario_huerto")