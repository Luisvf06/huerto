from django.forms import ModelForm
from django import forms
from .models import *
from bootstrap_datepicker_plus.widgets import DatePickerInput
from datetime import date 
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.gis.forms import PointField
import re
#from leaflet.forms.widgets import LeafletWidget
class HuertoModelForm(ModelForm):
    class Meta:
        model = Huerto
        fields=['ubicacion','sitio','sustrato','area','acidez','abonado']
        labels={
            "ubicacion": ("Ubicación del huerto"),"sitio":("Sitio"),
                "sustrato":("Sustrato"),
                "area":("Área"),
                "acidez": ("Acidez"),
                "abonado":("Abonado"),
                }
        help_text= {
            "area":("En metros cuadrados"),
        }
        widgets={
            "abonado":forms.CheckboxInput()
        }
        localized_fields=[]

    def clean(self):
        super().clean()         
        ubicacion=self.cleaned_data.get('ubicacion')
        sitio=self.cleaned_data.get('sitio')
        sustrato=self.cleaned_data.get('sustrato')
        area=self.cleaned_data.get('area')
        acidez=self.cleaned_data.get('acidez')
        
        #validacion ubicacion
        if ubicacion is not None:
            ubicacion=ubicacion.split(",")
            if not (-90 <= float(ubicacion[0]) <= 90):
                self.add_error('ubicacion', 'La latitud debe estar entre -90 y 90')
            if not (-180 <= float(ubicacion[1]) <= 180):
                self.add_error('ubicacion', 'La longitud debe estar entre -180 y 180')
        
        #validacion sitio
        
        if sitio is not None and len(sitio)<1:
            self.add_error('sitio','Elige una opción')
        #validacion sustrato
        if sustrato is not None and len(sustrato)<1:
            self.add_error('sustrato','Elige una opción')
        #validacion area
        
        if not (re.match(r'\d+\.?\d*$',str(area)) and area>0):
            self.add_error('area','debe ser un número mayor que 0')
        #validacion acidez
        # validacion acidez
        if acidez is None:
            self.add_error('acidez', 'Este campo no puede estar en blanco')
        elif not (re.match(r'\d+\.?\d*$', str(acidez))):
            self.add_error('acidez', 'debe ser un número entre 0 y 14')
        elif not (0 < acidez < 14):
            self.add_error('acidez', 'debe ser un número entre 0 y 14')
            #la regex busca uno o mas numeros seguido o no de un punto decimal y cero o mas digitos
            
        #validacion abonado
            #En mi formulario esto es un checkbox, por lo tanto las opciones son marcarlo o no y ambas son válidas, no se me ocurre validación alguna
        #validacion usuario
        #reg=r'[a-zA-Z1-9]+'
        #if not(re.match(reg,usuario)):
        #    self.add_error('usuario','debe ser una cadena alfanumérica')
        return self.cleaned_data
        
class BusquedaHuerto(forms.Form):
    textoBusqueda = forms.CharField(required=True)

class BusquedaAvanzadaHuerto(forms.Form):

    sitio= forms.MultipleChoiceField(choices=Huerto.SITIO, required=False,widget=forms.CheckboxSelectMultiple())
    
    sustrato=forms.MultipleChoiceField(choices=Huerto.SUSTRATO,required=False,widget=forms.CheckboxSelectMultiple())

    area_minima=forms.FloatField(label="Área mínima",required=False)
    #tenia esto en los widgets de las areas pero me daba error ,widgets=[forms.NumberInput(attrs={'type': 'number', 'step': '0.01'}),forms.NumberInput(attrs={'type': 'number', 'step': '0.1'})]
    area_maxima=forms.FloatField(label="Área máxima",required=False)
    
    abonado=forms.BooleanField(required=False)

    ubicacion = forms.CharField(label="Ubicación",required=False,  widget=forms.TextInput(attrs={'placeholder': 'Ingrese la ubicación'}))#de momento no consigo hacer funcionar los widgets que encuentro para plainlocationfield


    def clean(self):
        super().clean()
        sustrato=self.cleaned_data.get('sustrato')
        area_minima=self.cleaned_data.get('area_minima')
        area_maxima=self.cleaned_data.get('area_maxima')


        if ( len (sustrato)==0
            and area_minima==None
            and area_maxima==None
            ):
            self.add_error('sustrato','Debe escoger al menos una opción')
            self.add_error('area_minima','Debe indicar al menos un valor')
            self.add_error('area_maxima','debe indicar al menos un valor')

            #esto no tiene mucho sentido por el booleanfield, pero lo dejo para probar si funciona o no
        else:


            if(not area_minima is None and not area_maxima is None and area_minima>area_maxima):
                self.add_error('area_minima','El área mínima no puede ser mayor al área máxima')
                self.add_error('area_maxima','El área máxima no puede ser menor al área mínima')
        return self.cleaned_data


'''
class UsuarioModelForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre_usuario','nombre','apellidos','email','telefono','ciudad']
        labels={
            'nombre_usuario':('Nombre de usuario'),'nombre':('Nombre'),'apellidos':('Apellidos'),'email':('email'),'telefono':('Teléfono'),'ciudad':('Ciudad')
        }
        widgets={
        }
        localized_fields=[]

    def clean(self):
        super().clean()

        nombre=self.cleaned_data.get('nombre')
        nombre_usuario=self.cleaned_data.get('nombre_usuario')
        apellidos=self.cleaned_data.get('apellidos')
        email=self.cleaned_data.get('email')
        telefono=self.cleaned_data.get('telefono')
        ciudad=self.cleaned_data.get('ciudad')

        usuarioNombre= Usuario.objects.filter(nombre_usuario=nombre_usuario).first()
        usuarioemail= Usuario.objects.filter(email=email).first()
        if(not (usuarioNombre is None or (not self.instance is None and usuarioNombre.id ==self.instance.id))):
            self.add_error('nombre_usuario','Ya existe un usuario con ese nombre')
        if(not (usuarioemail is None or (not self.instance is None and usuarioemail.id ==self.instance.id))):
            self.add_error('email','Ya existe un usuario con ese correo electrónico')
        if not(re.match(r'^[A-Z][a-z]+',nombre)):
            self.add_error('nombre','El nombre solo puede tener caracteres alfabéticos')
        
        if (not re.match(r'\w+@\w+\.\w',email)):
            self.add_error('email','El email debe tener un formato válido')
        if (not len(str(telefono))==9):
            self.add_error('telefono','el telefono debe tener 9 digitos')
        
        return self.cleaned_data

class BusquedaAvanzadaUsuario(forms.Form):
    textoBusqueda= forms.CharField(required=False)
    usuariotelefono=forms.IntegerField(required=False)


    def clean(self):
        super().clean()
        textoBusqueda=self.cleaned_data.get('textoBusqueda')
        usuariotelefono=self.cleaned_data.get('usuariotelefono')


        if(textoBusqueda == "" and usuariotelefono is None):
            self.add_error('textoBusqueda','Debes introducir algún valor')
            self.add_error('usuariotelefono','debes introducir algun valor')

        else:
            if(textoBusqueda=="" and str(usuariotelefono) is not None and (len(str(usuariotelefono))!=9)):
                self.add_error('usuariotelefono','el telefono debe tener 9 dígitos')
        return self.cleaned_data
'''
class GastoModelForm(ModelForm):
    class Meta:
        model=Gastos
        fields=['herramientas','facturas','imprevistos','Descripcion','fecha','usuario']
        labels= {'herramientas':('Herramientas'),'facturas':('Facturas'),'imprevistos':('Imprevistos'),'Descripcion':('Descripción'),'fecha':('Fecha del gasto'),'usuario':('usuario')}
        widgets={'fecha':forms.SelectDateWidget(),
                    'usuario':forms.HiddenInput()
                }
        localized_fields=["fecha"]
    
    def clean(self):
        super().clean()
        herramientas=self.cleaned_data.get('herramientas')
        facturas=self.cleaned_data.get('facturas')
        imprevistos=self.cleaned_data.get('imprevistos')
        Descripcion=self.cleaned_data.get('Descripcion')
        fecha=self.cleaned_data.get('fecha')
        usuario=self.cleaned_data.get('usuario')
        
        if not isinstance(herramientas,float):
            self.add_error('herramientas','debe ser un numero')
        if not isinstance(facturas,float):
            self.add_error('facturas','debe ser un numero')
        if not isinstance(imprevistos,float):
            self.add_error('imprevistos','debe ser un numero')
        hoy=date.today()
        if fecha and hoy<fecha:
            self.add_error('fecha','la fecha del gasto no puede ser posterior al día de hoy')
        
        return self.cleaned_data
    
class BusquedaAvanzadaGasto(forms.Form):

    gasto_busqueda=forms.FloatField(label="Importe",required=False)
    texto_busqueda=forms.CharField(label="Texto",required=False)

    def clean(self):
        super().clean()
        gasto_busqueda=self.cleaned_data.get('gasto_busqueda')
        texto_busqueda=self.cleaned_data.get('texto_busqueda')

        if gasto_busqueda is None and not texto_busqueda:
            self.add_error('gasto_busqueda', 'Debes introducir un valor')
            self.add_error('texto_busqueda', 'Debes introducir un valor')

        if not isinstance(gasto_busqueda, float) and gasto_busqueda is not None:
            self.add_error('gasto_busqueda', 'Debes introducir un valor numérico')

        return self.cleaned_data

class BlogModelForm(ModelForm):   
    class Meta:
        model = Blog
        fields = ['publicacion','fecha','etiqueta','usuario']
        labels = {
            "publicacion": ("Tipo de publicación"),'fecha':("Fecha de publicación"),'etiqueta':('Etiqueta'),'usuario':('usuario')
        }
        widgets = {
            "fecha":forms.SelectDateWidget(),
            "usuario":forms.HiddenInput(),
            "etiqueta":forms.TextInput(attrs={'placeholder':'Etiqueta'}),
            'publicacion': forms.Select(choices=Blog.PUBLICACION),

        }
        localized_fields = ["fecha"]
    
    
    def clean(self):

        #Validamos con el modelo actual
        super().clean()
        
        #Obtenemos los campos 
        publicacion = self.cleaned_data.get('publicacion')
        fecha = self.cleaned_data.get('fecha')
        etiqueta = self.cleaned_data.get('etiqueta')
        
        if publicacion is not None and len(publicacion) < 1:
            self.add_error('publicacion','Debes indicar el tipo de publicación')
        
        #Comprobamos que la fecha de publicación sea mayor que hoy
        fechaHoy = date.today()
        if not fechaHoy == fecha:
            self.add_error('fecha','La fecha de publicacion debe ser  igual a Hoy')
        #comianza y acaba por mayuscula o numero
        if not(re.match(r'^[A-Z0-9]+$',etiqueta)):
            self.add_error('etiqueta','El nombre solo puede tener caracteres en mayúsculas')

        if not(len(etiqueta)>=2):
            self.add_error('etiqueta','La etiqueda debe tener entre 2 y 15 caracteres')

        
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data
    

class BusquedaAvanzadaBlogForm(forms.Form):
    
    etiqueta = forms.CharField(required=False,
                        label='Etiqueta')
    
    publicacion = forms.MultipleChoiceField(choices=Blog.PUBLICACION,
                                required=False,
                                widget=forms.CheckboxSelectMultiple()
                                )
    
    fecha_desde = forms.DateField(label="Fecha Desde",
                                required=False,
                                widget= forms.SelectDateWidget(years=range(1990,2026))
                                )
    
    fecha_hasta = forms.DateField(label="Fecha Hasta",
                                required=False,
                                widget= forms.SelectDateWidget(years=range(1990,2026))
                                )
    
    usuario=forms.IntegerField(label='Usuario',
                            required=False,
                                )
    
    
    def clean(self):

        #Validamos con el modelo actual
        super().clean()
        
        #Obtenemos los campos 
        etiqueta = self.cleaned_data.get('etiqueta')
        publicacion = self.cleaned_data.get('publicacion')
        fecha_desde = self.cleaned_data.get('fecha_desde')
        fecha_hasta = self.cleaned_data.get('fecha_hasta')
        
        #Controlamos los campos
        if(etiqueta == "" 
        and len(publicacion) == 0
        and fecha_desde is None
        and fecha_hasta is None
        ):
            self.add_error('etiqueta','Debe introducir al menos un valor en un campo del formulario')
            self.add_error('publicacion','Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_desde','Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_hasta','Debe introducir al menos un valor en un campo del formulario')
        else:
            #La fecha hasta debe ser mayor o igual a fecha desde. Pero sólo se valida si han introducido ambas fechas
            if(not fecha_desde is None  and not fecha_hasta is None and fecha_hasta < fecha_desde):
                self.add_error('fecha_desde','La fecha hasta no puede ser menor que la fecha desde')
                self.add_error('fecha_hasta','La fecha hasta no puede ser menor que la fecha desde')
            
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data


class IncidenciaModelForm(ModelForm):   
    class Meta:
        model = Incidencia
        fields = ['descripcion','fecha_incidencia','huerto']
        labels = {
            "descripcion": ("Descripción"),
            "fecha_incidencia":("Fecha de la incidencia")
        }
        help_texts = {
            "descripcion": ("2000 caracteres como máximo"),
        }
        widgets = {
            "fecha_incidencia":forms.SelectDateWidget(),
            "descripcion":forms.Textarea

        }
        localized_fields = ["fecha_incidencia"]

    def clean(self):
        # Validamos con el modelo actual
        super().clean()

        # Obtenemos los campos
        descripcion = self.cleaned_data.get('descripcion')
        fecha_incidencia = self.cleaned_data.get('fecha_incidencia')

        # Comprobamos que el campo descripción no sea None y tenga menos de 10 caracteres o más de 2000
        if descripcion is not None and not (10 <= len(descripcion) <= 2000):
            self.add_error('descripcion', 'La descripción debe tener entre 10 y 2000 caracteres')

        # Comprobamos que la fecha de publicación sea hoy o una fecha anterior
        fechaHoy = date.today()
        if fecha_incidencia is not None and fechaHoy < fecha_incidencia:
            self.add_error('fecha_incidencia', 'La fecha de incidencia debe ser igual o anterior a la fecha de hoy')

        # Siempre devolvemos el conjunto de datos.
        return self.cleaned_data

    

class BusquedaAvanzadaIncidenciaForm(forms.Form):
    
    textoBusqueda = forms.CharField(required=False)
    
    
    fecha_desde = forms.DateField(label="Fecha Desde",
                                required=False,
                                widget= forms.SelectDateWidget(years=range(1990,2024))
                                )
    
    fecha_hasta = forms.DateField(label="Fecha Desde",
                                required=False,
                                widget= forms.SelectDateWidget(years=range(1990,2024))
                                )

    def clean(self):

        #Validamos con el modelo actual
        super().clean()
        
        #Obtenemos los campos 
        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        fecha_desde = self.cleaned_data.get('fecha_desde')
        fecha_hasta = self.cleaned_data.get('fecha_hasta')

        if(textoBusqueda == "" 
            and fecha_desde is None
            and fecha_hasta is None
            ):
            self.add_error('textoBusqueda','Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_desde','Debe introducir al menos un valor en un campo del formulario')
            self.add_error('fecha_hasta','Debe introducir al menos un valor en un campo del formulario')
        else:
            #Si introduce un texto al menos que tenga  10 caracteres o más
            if(textoBusqueda != "" and len(textoBusqueda) < 10):
                self.add_error('textoBusqueda','Debe introducir al menos 10 caracteres')
            
            #La fecha limite debe ser posterior a la inicial si se busca por ambas
            if(not fecha_desde is None  and not fecha_hasta is None and fecha_hasta < fecha_desde):
                self.add_error('fecha_desde','La fecha hasta no puede ser menor que la fecha desde')
                self.add_error('fecha_hasta','La fecha hasta no puede ser menor que la fecha desde')
            
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data

class FrutoModelForm(ModelForm):   
    class Meta:
        model = Fruto
        fields = ['nombre','tipo','planta']
        labels = {
            "nombre": ("Nombre del fruto"),
            "tipo": ("Tipo de fruto"),
            "planta":("Planta")
        }
        help_texts = {
        }
        widgets = {
        }
    
    
    def clean(self):

        #Validamos con el modelo actual
        super().clean()
        
        #Obtenemos los campos 
        nombre = self.cleaned_data.get('nombre')
        tipo = self.cleaned_data.get('tipo')
        planta=self.cleaned_data.get('planta')

        #Comprobamos que no exista un fruto con ese nombre
        texto = Fruto.objects.filter(nombre=nombre).first()

        if(not texto is None
        ):
            if(not self.instance is None and texto.id == self.instance.id):
                pass
            else:
                self.add_error('nombre','Ya existe un fruto con ese nombre')

        #Comprobamos que el campo descripción no tenga menos de 10 caracteres        
        if texto=="":
            self.add_error('nombre','El campo no puede estar vacío')
        if nombre is not None and not re.match(r'^[A-Z][a-z]+$', nombre):
            self.add_error('nombre', 'El campo debe empezar por mayúscula y sólo puede contener letras')

        if tipo is not None and not re.match(r'^[A-Z][a-z]+$', tipo):
            self.add_error('tipo', 'El campo debe empezar por mayúscula y sólo puede contener letras')


        if planta is None:
            self.add_error('planta', 'El campo no puede quedar vacío')

            ''' he tenido que quitar esta validacion porque me daba error al ser un choice
        if planta == None:
            self.add_error('planta','El campo no puede quedar vacío')
        if not(re.match(r'^[1-9]*[0-9]+$',planta)):
            self.add_error('planta','El campo  contener caracteres numéricos')
            '''
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data

class BusquedaAvanzadaFrutoForm(forms.Form):
    
    textoBusqueda = forms.CharField(required=False)
    plant=forms.IntegerField(required=False)
    
    
    def clean(self):

        #Validamos con el modelo actual
        super().clean()
        
        #Obtenemos los campos 
        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        plant = self.cleaned_data.get('plant')
        
        #Controlamos los campos
        #Ningún campo es obligatorio, pero al menos debe introducir un valor en alguno para buscar
        if(textoBusqueda == "" 
            and plant == None
            ):
            self.add_error('textoBusqueda','Debe introducir al menos un valor en un campo del formulario')
            self.add_error('plant','Debe introducir al menos un valor en un campo del formulario')
        else:
            #Si introduce un texto al menos que tenga  3 caracteres o más
            if not (isinstance(plant,int)):
                self.add_error('plant','el valor de búsqueda debe ser un nº entero')
            
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data


class TratamientoModelForm(ModelForm):   
    class Meta:
        model = Tratamiento
        fields = ['consejos','descripcion','aplicacion','plaga']
        labels = {
            "consejos": ("Consejos"),
            "descripcion":("Descripcion"),
            "aplicacion":("Aplicación del tratamiento"),
            "plaga":("Plaga")
        }
        help_texts = {
        }
        widgets = {
        }
        localized_fields = []
    
    def clean(self):

        #Validamos con el modelo actual
        super().clean()
        
        #Obtenemos los campos 
        consejos = self.cleaned_data.get('consejos')
        descripcion = self.cleaned_data.get('descripcion')
        aplicacion = self.cleaned_data.get('aplicacion')
        plaga = self.cleaned_data.get('plaga')

    # Comprobamos que el campo descripción no tenga menos de 50 caracteres
        if descripcion is None or len(descripcion) < 50:
            self.add_error('descripcion', 'Al menos debes indicar 50 caracteres')
        if descripcion is None or len(descripcion)>150:
            self.add_error('descripcion','La lonngitud maxima es 150')
        # Comprobamos que el campo consejos no tenga menos de 10 caracteres
        if consejos is None or len(consejos) < 10:
            self.add_error('consejos', 'Al menos debes indicar 10 caracteres')
        if consejos is None or len(consejos)>1000:
            self.add_error('consejos','La lonngitud maxima es 150')
        # Comprobamos que el campo aplicacion no tenga menos de 15 caracteres
        if aplicacion is None or len(aplicacion) < 15:
            self.add_error('aplicacion', 'Al menos debes indicar 15 caracteres')
        if aplicacion is None or len(aplicacion)>200:
            self.add_error('aplicacion','La lonngitud maxima es 200')


        #Que al menos seleccione dos autores

        
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data

class BusquedaAvanzadaTratamientoForm(forms.Form):
    
    textoBusqueda = forms.CharField(required=False)

    
    def clean(self):

        #Validamos con el modelo actual
        super().clean()
        
        #Obtenemos los campos 
        textoBusqueda = self.cleaned_data.get('textoBusqueda')

        
        #Controlamos los campos
        #Ningún campo es obligatorio, pero al menos debe introducir un valor en alguno para buscar
        if(textoBusqueda == "" 

        ):
            self.add_error('textoBusqueda','Debe introducir al menos un valor en un campo del formulario')

        else:
            #Si introduce un texto al menos que tenga  5 caracteres o más
            if(textoBusqueda != "" and len(textoBusqueda) < 5):
                self.add_error('textoBusqueda','Debe introducir al menos 3 caracteres')
            
        #Siempre devolvemos el conjunto de datos.
        return self.cleaned_data
class RegistroForm(UserCreationForm):
    roles =(
            (Usuario.USU, 'usu'),
            (Usuario.USU_PREMIUM,'usu_premium'),
    )
    rol = forms.ChoiceField(choices=roles)
    class Meta:
        model=Usuario
        fields= ('username','email','password1','password2','rol')
#examen 14 diciembre
class PromocionModelForm(ModelForm):
    class Meta:
        model=Promocion
        fields=['nombre_promocion','descripcion','descuento','fecha_promocion','usuario']
        labels= {'nombre_promocion':('Promocion'),'descripcion':('Descripcion'),'descuento':('Descuento'),'fecha_promocion':('fecha de la promocion'),'usuario':('usuario')}
        widgets={'fecha_promocion':forms.SelectDateWidget(),
                }
        localized_fields=["fecha_promocion"]
    
    def clean(self):
        super().clean()
        nombre_promocion=self.cleaned_data.get('nombre_promocion')
        descripcion=self.cleaned_data.get('descripcion')
        descuento=self.cleaned_data.get('descuento')
        fecha_promocion=self.cleaned_data.get('fecha_promocion')
        usuario = self.cleaned_data.get('usuario')

        
        nombre_promocion= Promocion.objects.select_related(usuario).filter(nombre_promocion=nombre_promocion).first()
        if(not (nombre_promocion is None or (not self.instance is None and nombre_promocion.id ==self.instance.id))):
            self.add_error('nombre_promocion','Ya existe una promocion con ese nombre')
        if(len(descripcion)<100):
            self.add_error('descripcion','La descripción debe tener al menos 100 caracteres')
        if(not descuento<=100 and 0<=descuento):
            self.add_error('descuento','el descuento debe estar entre 0 y 100')
        hoy=date.today()
        if (fecha_promocion<hoy):
            self.add_error('fecha_promocion','La fecha no puede ser anterior al dia de hoy')
        
        
        return self.cleaned_data

class BusquedaAvanzadaPromocion(forms.Form):

    texto=forms.CharField(label="texto",required=False)
    descuentoMayor=forms.IntegerField(label="Descuento",required=False)
    fechaIn= forms.DateField(label="Fecha Desde",
                            required=False,
                            widget= forms.SelectDateWidget(years=range(2023,2030))
                            )

    fechaFi = forms.DateField(label="Fecha hasta",
                            required=False,
                            widget= forms.SelectDateWidget(years=range(2023,2030))
                            )

    def clean(self):
        super().clean()
        texto=self.cleaned_data.get('texto')
        descuentoMayor=self.cleaned_data.get('descuentoMayor')
        fechaIn=self.cleaned_data.get('fechaIn')
        fechaFi=self.cleaned_data.get('fechaFi')
        
        if  descuentoMayor is None and not texto and fechaIn is None and fechaFi is None:
            self.add_error('texto', 'Debes introducir un valor')
            self.add_error('descuentoMayor', 'Debes introducir un valor')
            self.add_error('fechaFi','Debes introducir un valor')
            self.add_error('fechaIn','Debes introducir un valor')

        
        if (fechaFi<fechaIn):
            self.add_error('fechaFi','la fecha de finalizacion no puede ser anterior a la de comienzo')
            self.add_error('fechaIn','la fecha de finalizacion no puede ser anterior a la de comienzo')
        
        return self.cleaned_data
    
