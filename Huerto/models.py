from django.db import models
from django.utils import timezone
from location_field.models.plain import PlainLocationField
# Create your models here.
class Usuario(models.Model):
    nombre_usuario=models.CharField(max_length=20)
    nombre=models.CharField(max_length=100)
    apellidos=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    telefono=models.IntegerField()
    ciudad=models.CharField(max_length=50)

class Contrasenha(models.Model):#creo que este modelo podria ser un atributo dentro de usuario, pero me faltaba una relacion 1-1
    contrasenha=models.CharField(max_length=30)
    ultima_modificacion=models.DateTimeField(default=timezone.now)
    usuario=models.OneToOneField(Usuario,on_delete=models.CASCADE)

class Gastos(models.Model):
    herramientas=models.FloatField()#no sé muy bien cómo encajar esta clase y sobre todo este atributo pero creo que lo mejor es orientarlo al gasto en herramientas
    facturas=models.FloatField()
    imprevistos=models.FloatField()
    Descripcion=models.TextField(max_length=2000)
    fecha=models.DateTimeField(default=timezone.now)
    usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE,related_name='usuario_gasto')

class Blog(models.Model):
    PUBLICACION=[('C','comentario'),('N','noticia'),('E','enlace'),('T','tutorial'),('R','reseña')]
    publicacion=models.CharField(max_length=1,choices=PUBLICACION)
    fecha=models.DateTimeField(default=timezone.now)
    etiqueta=models.CharField(max_length=15)
    usuario=models.ForeignKey(Usuario,on_delete=models.CASCADE,related_name='usuario_blog')

class Huerto(models.Model):
    ubicacion=PlainLocationField()#atributo para almacenar coordenadas en forma de tupla de cadenas de 2 elementos(latitud,longitud)
    SITIO=[('M','maceta'),('J','jardin'),('T','terraza'),('P','parcela')]
    sitio=models.CharField(max_length=1,choices=SITIO)
    SUSTRATO=[('ARE','arenoso'),('ARC','arcilloso'),('LIM','limoso'),('FRA','franco'),('TUR','turbado')]
    sustrato=models.CharField(max_length=3,choices=SUSTRATO)
    area=models.FloatField(blank=True,null=True)
    acidez=models.FloatField(blank=True,null=True)
    abonado=models.BooleanField()#esto no sé si incluirlo aqui o no ya que es algo que se hace cada X tiempo, por lo que en ciertas ocasiones puede ser True y en otras False
    usuario=models.ManyToManyField(Usuario,related_name="usuario_huerto")#lo he vuelto a hacer para poder relacionarlo de forma inversa con usuaroi

class Incidencia(models.Model):
    descripcion=models.TextField(max_length=2000)
    fecha_incidencia=models.DateTimeField(default=timezone.now,db_column='fecha')
    huerto=models.ForeignKey(Huerto,on_delete=models.CASCADE,related_name='huerto_incidencia')#entiendo que es 1-n porque aunque una incidencia puede ocurrir varias veces, como por ejemplo una inundacion, cada una es un hecho individual de cada huerto

class Planta(models.Model):
    TIPO=[('HE','herbacea'),('AL','árbol'),('AO','arbusto')]
    tipo=models.CharField(max_length=2,choices=TIPO)
    CICLO=[('A','anual'),('B','bianual'),('P','perenne')]
    ciclo=models.CharField(max_length=1,choices=CICLO)
    #los dos atributos de arriba no sé si debo dejarlos o no. Lo ideal sería que a partir del nombre_comun se autocompletasen, tal y como están ahora, puedo poner que tomate sea un árbol y no tiene sentido
    nombre_comun=models.CharField(max_length=20,db_column='nombre')
    nombre_cientifico=models.CharField(max_length=30)
    phmax=models.FloatField()
    phmin=models.FloatField()
    epoca_siembra=models.DateField(default=timezone.now,db_column='siembra')
    tiempo_trasplante=models.IntegerField()
    temp_max=models.IntegerField()
    temp_min=models.IntegerField()
    horas_luz=models.IntegerField()
    demanda_hidrica=models.FloatField(blank=True,null=True)
    huerto=models.ForeignKey(Huerto,on_delete=models.CASCADE)

class Riego(models.Model):#esta clase la planteé en un principio para que se relacionase de forma n-m con planta, pero decidí cambiar la relacion a 1-n añadiendo una tabla intermedia
    PRODUCTO=[('A','agua'),('F','fertilizante'),('L','lluvia'),('P','plaguicida')]
    producto=models.CharField(max_length=1,choices=PRODUCTO)
    planta=models.ManyToManyField(Planta,through="Planta_regada")
#también pensé que estas clases podrían ir mejor con Huerto, pero si tengo 4 plantas una al lado de otra en una misma parcela, puedo regar sólo una y no al resto
class Planta_regada(models.Model):
    fecha=models.DateTimeField(default=timezone.now)
    planta=models.ForeignKey(Planta,on_delete=models.CASCADE)
    riego=models.ForeignKey(Riego,on_delete=models.CASCADE)

class Fruto(models.Model):
    nombre=models.CharField(max_length=20)
    tipo=models.CharField(max_length=20)
    planta=models.OneToOneField(Planta,on_delete=models.CASCADE)

class Calendario(models.Model):
    fecha=models.DateField(default=timezone.now)
    EVENT=[('S','siembra'),('T','trasplante'),('C','Cosecha'),('R','riego'),('F','fumigacion'),('P','poda')]
    event=models.CharField(max_length=1,choices=EVENT)
    estacion=models.CharField(max_length=9)
    Planta=models.ManyToManyField(Planta,through='Evento')

class Evento(models.Model):
    descripcion=models.TextField(max_length=2000)
    planta=models.ForeignKey(Planta,on_delete=models.CASCADE)
    calendario=models.ForeignKey(Calendario,on_delete=models.CASCADE)

class Plaga(models.Model):
    ORIGEN=[('V','virico'),('B','bacteriano'),('F','fungico'),('A','animal'),('P','vegetal')]
    origen=models.CharField(choices=ORIGEN,max_length=1)
    descripcion=models.TextField(max_length=2000)
    planta=models.ForeignKey(Planta,on_delete=models.CASCADE)

class Historial(models.Model):
    fecha=models.DateTimeField(default=timezone.now)
    descripcion=models.TextField(max_length=2000)
    plaga=models.ForeignKey(Plaga,on_delete=models.CASCADE,related_name='plaga_plant',unique=False)

class Tratamiento(models.Model):
    descripcion=models.TextField(max_length=150)
    consejos=models.TextField(max_length=1000)
    aplicacion=models.TextField(max_length=200)
    plaga=models.ManyToManyField(Plaga)


