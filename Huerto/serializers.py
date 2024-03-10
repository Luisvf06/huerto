from .models import *
from .forms import *
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

from rest_framework import serializers

class HuertoSerializerMejorado(serializers.ModelSerializer):
    sitio = serializers.CharField(source='get_sitio_display')
    sustrato = serializers.CharField(source='get_sustrato_display')
    usuario = UsuarioSerializer(read_only=True, many=True)
    plantas_huerto = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'ubicacion', 'sitio', 'sustrato', 'area', 'acidez', 'abonado', 'disponible', 'usuario', 'plantas_huerto')
        model = Huerto

    def get_plantas_huerto(self, obj):
        plantas = obj.plantas_huerto.all()
        return PlantaSerializerMejorado(plantas, many=True, context=self.context).data


class GastosSerializerMejorado(serializers.ModelSerializer):
    fecha = serializers.DateField(format=('%d-%m-%Y'))
    usuario=UsuarioSerializer()

    class Meta:
        fields =('id',
                'herramientas',
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
        fields=('id',
                'publicacion',
                'fecha',
                'etiqueta',
                'usuario')
        model=Blog

class HuertoSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model =Huerto
        fields = ['ubicacion','sitio','sustrato','area','acidez','abonado','disponible']
        
    def validate_ubicacion(self,ubicacion): #entiendo que la validacion es la misma que en la de los formularios normales, pero no estoy seguro
        if ubicacion is not None:
            ubicacion=ubicacion.split(",")
            if not (-90 <= float(ubicacion[0]) <= 90):
                self.add_error('ubicacion', 'La latitud debe estar entre -90 y 90')
            if not (-180 <= float(ubicacion[1]) <= 180):
                self.add_error('ubicacion', 'La longitud debe estar entre -180 y 180')
        return ubicacion
    def validate_sitio(self,sitio):
        if sitio is not None and len(sitio)<1:
            self.add_error('sitio','Elige una opción')
        return sitio
    
    def validate_sustrato(self,sustrato):
        if sustrato is not None and len(sustrato)<1:
            self.add_error('sustrato','Elige una opción')
        return sustrato
    
    def validate_area(self,area):
        if not (re.match(r'\d+\.?\d*$',str(area)) and area>0):
            self.add_error('area','debe ser un número mayor que 0')
        return area
    
    def validate_acidez(self,acidez):
        if acidez is None:
            self.add_error('acidez', 'Este campo no puede estar en blanco')
        elif not (re.match(r'\d+\.?\d*$', str(acidez))):
            self.add_error('acidez', 'debe ser un número entre 0 y 14')
        elif not (0 < acidez < 14):
            self.add_error('acidez', 'debe ser un número entre 0 y 14')
        return acidez

class GastoSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Gastos
        fields = ('herramientas', 'facturas', 'imprevistos', 'Descripcion', 'fecha', 'usuario')

    def validate_herramientas(self, herramientas):
        if herramientas is None:
            self.add_error('herramientas', 'Este campo no puede estar en blanco')
        return herramientas

    def validate_facturas(self, facturas):
        if facturas is None:
            self.add_error('facturas', 'Este campo no puede estar en blanco')
        return facturas

    def validate_imprevistos(self, imprevistos):
        if imprevistos is None:
            self.add_error('imprevistos', 'Este campo no puede estar en blanco')
        return imprevistos

    def validate_Descripcion(self, Descripcion):
        if len(Descripcion) < 5:
            self.add_error('Descripcion', 'Mínimo 5 caracteres')
        return Descripcion

    def validate_fecha(self, fecha):
        hoy = date.today()
        if fecha and hoy < fecha:
            self.add_error('fecha', 'La fecha del gasto no puede ser posterior al día de hoy')
        return fecha

class BlogSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model=Blog
        fields=['publicacion','etiqueta','fecha','usuario']
    def validate_publicacion(self,publicacion):
        if publicacion is not None and len(publicacion)<1:
            self.add_error('publicacion','Debes elegir una categoría')
        return publicacion
    
    def validate_etiqueta(self,etiqueta):
        if len(etiqueta)<3:
            self.add_error('etiqueta','La etiqueta debe tener al menos 3 caracteres')
        return etiqueta
    def validate_fecha(self,fecha):
        hoy=date.today()
        if fecha and hoy<fecha:
            self.add_error('fecha','La fecha de la publicación no puede ser una fecha futura')
        return fecha

class UsuarioSerializerRegistro(serializers.Serializer):
    username=serializers.CharField()
    password1=serializers.CharField()
    password2=serializers.CharField()
    email=serializers.EmailField()
    rol=serializers.IntegerField()
    
    def validate_nombre(self, username):
        usuario=Usuario.objects.filter(username=username).first()
        if(not usuario is None):
            raise serializers.ValidationError("Ya existe un usuario con ese nombre")
        return username
    
    def validate_contra(self,password1,password2):
        if password1!=password2:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return password1
    def validate_email(self,email):
        usuario=Usuario.objects.filter(email=email).first()
        if(not usuario is None):
            raise serializers.ValidationError("Ese correo electrónico ya está registrado")
        return email
    def validate_rol(self,rol):
        rol not in [1,2]
        return rol
class Meta:
    model=Huertofields=['ubicacion']

    def validate_ubicacion(self,ubicacion):
        huertoubi=Huerto.objects.filter(ubicacion=ubicacion).first()
        if(not huertoubi is None and huertoubi.id !=self.instance.id):
            raise serializers.ValidationError('ya hay una ubicacion con esas coordenadas')
        return ubicacion


class HuertoSerializerActualizarAbonado(serializers.ModelSerializer):
    class Meta:
        model=Huertofields=['abonado']

    def validate_ubicacion(self,abonado):
        huertoubi=Huerto.objects.filter(abonado=abonado).first()
        if(not huertoubi is None and huertoubi.id !=self.instance.id):
            raise serializers.ValidationError('el campo ya teiene ese valor')
        return abonado
    
class HuertoSerializerActualizarSitio(serializers.ModelSerializer):
    class Meta:
        model=Huertofields=['ubicacion']

    def validate_sitio(self,ubicacion):
        huertoubi=Huerto.objects.filter(sitio=ubicacion).first()
        if(not huertoubi is None and huertoubi.id !=self.instance.id):
            raise serializers.ValidationError('ya esta escogido ese campo')
        return ubicacion

class HuertoSerializerActualizarSustrato(serializers.ModelSerializer):
    class Meta:
        model=Huertofields=['sustrato']

    def validate_ubicacion(self,ubicacion):
        huertoubi=Huerto.objects.filter(sustrato=ubicacion).first()
        if(not huertoubi is None and huertoubi.id !=self.instance.id):
            raise serializers.ValidationError('ya hay un sustato con ese valor')
        return ubicacion

class HuertoSerializerActualizarArea(serializers.ModelSerializer):
    class Meta:
        model=Huertofields=['area']

    def validate_ubicacion(self,ubicacion):
        huertoubi=Huerto.objects.filter(area=ubicacion).first()
        if(not huertoubi is None and huertoubi.id !=self.instance.id):
            raise serializers.ValidationError('ya hay un area asi')
        return ubicacion

class HuertoSerializerActualizarAcidez(serializers.ModelSerializer):
    class Meta:
        model=Huertofields=['ubicacion']

    def validate_ubicacion(self,ubicacion):
        huertoubi=Huerto.objects.filter(acidez=ubicacion).first()
        if(not huertoubi is None and huertoubi.id !=self.instance.id):
            raise serializers.ValidationError('ya hay una ubicacion con esas coordenadas')
        return ubicacion
    
class GastoSerializerActualizarFactura(serializers.ModelSerializer):
    class Meta:
        model=Huertofields=['factura']

    def validate_ubicacion(self,factura):
        huertoubi=Gastos.objects.filter(factura=factura).first()
        if(not huertoubi is None and huertoubi.id !=self.instance.id):
            raise serializers.ValidationError('ya hay una factura asi')
        return factura

class GastoSerializerActualizarDescripcion(serializers.ModelSerializer):
    class Meta:
        model=Huertofields=['Descripcion']

    def validate_ubicacion(self,factura):
        huertoubi=Gastos.objects.filter(Descripcion=factura).first()
        if(not huertoubi is None and huertoubi.id !=self.instance.id):
            raise serializers.ValidationError('ya hay una Descrp asi')
        return factura


class GastoSerializerActualizarHerramientas(serializers.ModelSerializer):
    class Meta:
        model=Huertofields=['herramientas']

    def validate_ubicacion(self,herramientas):
        huertoubi=Gastos.objects.filter(herramientas=herramientas).first()
        if(not huertoubi is None and huertoubi.id !=self.instance.id):
            raise serializers.ValidationError('ya hay una herramienta asi')
        return herramientas

class GastoSerializerActualizarImprevistos(serializers.ModelSerializer):
    class Meta:
        model=Huertofields=['Descripcion']

    def validate_ubicacion(self,factura):
        huertoubi=Gastos.objects.filter(Descripcion=factura).first()
        if(not huertoubi is None and huertoubi.id !=self.instance.id):
            raise serializers.ValidationError('ya hay una Descrp asi')
        return factura
    
class GastoSerializerActualizarFecha(serializers.ModelSerializer):
    class Meta:
        model=Huertofields=['fecha']

    def validate_ubicacion(self,factura):
        huertoubi=Gastos.objects.filter(Descripcion=factura).first()
        if(not huertoubi is None and huertoubi.id !=self.instance.id):
            raise serializers.ValidationError('ya hay una Descrp asi')
        return factura
    
class BlogSerializerActualizarFecha(serializers.ModelSerializer):
    class Meta:
        model=Blogfields=['fecha']

    def validate_ubicacion(self,factura):
        huertoubi=Gastos.objects.filter(fecha=factura).first()
        if(not huertoubi is None and huertoubi.id !=self.instance.id):
            raise serializers.ValidationError('ya hay una fecha asi')
        return factura
    
class BlogSerializerActualizarEtiqueta(serializers.ModelSerializer):
    class Meta:
        model=Blogfields=['etiqueta']

    def validate_ubicacion(self,factura):
        huertoubi=Blog.objects.filter(etiqueta=factura).first()
        if(not huertoubi is None and huertoubi.id !=self.instance.id):
            raise serializers.ValidationError('ya hay una etiqueta asi')
        return factura
    
class BlogSerializerActualizarPublicacion(serializers.ModelSerializer):
    class Meta:
        model=Blogfields=['publicacion']

    def validate_ubicacion(self,factura):
        huertoubi=Blog.objects.filter(publicacion=factura).first()
        if(not huertoubi is None and huertoubi.id !=self.instance.id):
            raise serializers.ValidationError('ya hay una publicacion asi')
        return factura

#tarea final
#Gabriela 
class PlantaSerializerMejorado(serializers.ModelSerializer):
    cantidad_tipos_plagas = serializers.SerializerMethodField()

    class Meta:
        model = Planta
        fields = (
            'id',
            'tipo',
            'ciclo',
            'nombre_comun',
            'nombre_cientifico',
            'phmax',
            'phmin',
            'epoca_siembra',
            'tiempo_trasplante',
            'temp_max',
            'temp_min',
            'horas_luz',
            'demanda_hidrica',
            'huerto',
            'recoleccion',
            'cantidad_tipos_plagas',  
        )

    def get_cantidad_tipos_plagas(self, obj):
        cantidad = PlagaPlanta.objects.filter(planta=obj).values('plaga').distinct().count()
        return cantidad
    def get_plagas(self, obj):
        cantidad_plagas = PlagaPlanta.objects.filter(planta=obj).values('plaga').distinct().count()
        return cantidad_plagas

from .models import UploadedFile

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ('file', 'uploaded_on',)


#Alberto 
class PlantaRegadaSerializerMejorado(serializers.ModelSerializer):
    nombre_comun = serializers.CharField(source='planta.nombre_comun')
    fecha = serializers.DateField(format=('%d-%m-%Y'))

    class Meta:
        fields = ('id','nombre_comun', 'fecha')
        model = Planta_regada
class RiegoSerializerMejorado(serializers.ModelSerializer):
    class Meta:
        model=Riego
        producto = serializers.CharField(source='get_producto_display')
        fields=['id','producto']

class RiegoPlantaSerializar(serializers.ModelSerializer):#clase para crear registros de la clase intermedia entre plata y riego
    class Meta:
        model=Planta_regada
        fields=['fecha','id','riego','planta']
    def validate_fecha(self,fecha):
        fechaHoy = date.today()
        if (not  fecha<=fechaHoy) :
            raise serializers.ValidationError('La fecha de riego debe ser menos o igual a Hoy')
        return fecha
class PlantaRiegoSerializerActualizarFecha(serializers.ModelSerializer):
    class Meta:
        model=Planta_regada
        fields=['fecha']
    def validate_fecha(self,fecha):
        riegoFecha=Planta_regada.objects.filter(fecha=fecha).first()
        if (not riegoFecha is None and riegoFecha.fecha != self.instance.fecha):
            raise serializers.ValidationError('La fecha debe ser difernte de la actual')
        return riegoFecha
        
#Ivan
class PlagaSerializerMejorado(serializers.ModelSerializer):
    origen=serializers.CharField(source='get_origen_display')
    planta=PlantaSerializerMejorado
    class Meta:
        
        fields=('origen','descripcion','planta')
        model=Plaga

class PlagaPlantaSerializerMejorado(serializers.ModelSerializer):
    plaga = PlagaSerializerMejorado(read_only=True)

    class Meta:
        model = PlagaPlanta
        fields = ('plaga',)
