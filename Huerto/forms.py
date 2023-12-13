from django.forms import ModelForm
from django import forms
from .models import *
from bootstrap_datepicker_plus.widgets import DatePickerInput
from datetime import date 
from datetime import datetime
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
        }
        localized_fields=[]

    def clean(self):
        super().clean()         
        ubicacion=self.cleaned_data.get('ubicacion').split(",")
        sitio=self.cleaned_data.get('sitio')
        sustrato=self.cleaned_data.get('sustrato')
        area=self.cleaned_data.get('area')
        acidez=self.cleaned_data.get('acidez')
        
        #validacion ubicacion
        if not (-90 <= float(ubicacion[0]) <= 90):
            self.add_error('ubicacion', 'La latitud debe estar entre -90 y 90')
        if not (-180 <= float(ubicacion[1]) <= 180):
            self.add_error('ubicacion', 'La longitud debe estar entre -180 y 180')
        
        #validacion sitio
        if len(sitio)<1:
            self.add_error('sitio','Elige una opción')
        #validacion sustrato
        if len(sustrato)<1:
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

    usuario=forms.CharField(label="Usuario", required=False)#entiendo que en buscar sí se puede poner para consultar un usuario, no como en crear que no tenía sentido

    def clean(self):
        super().clean()
        sustrato=self.cleaned_data.get('sustrato')
        area_minima=self.cleaned_data.get('area_minima')
        area_maxima=self.cleaned_data.get('area_maxima')
        usuario=self.cleaned_data.get('usuario')

        if ( len (sustrato)==0
            and area_minima==None
            and area_maxima==None
            and usuario==None):
            self.add_error('sustrato','Debe escoger al menos una opción')
            self.add_error('area_minima','Debe indicar al menos un valor')
            self.add_error('area_maxima','debe indicar al menos un valor')
            self.add_error('usuario','debe indicar al menos un valor')
            #esto no tiene mucho sentido por el booleanfield, pero lo dejo para probar si funciona o no
        else:


            if(not area_minima is None and not area_maxima is None and area_minima>area_maxima):
                self.add_error('area_minima','El área mínima no puede ser mayor al área máxima')
                self.add_error('area_maxima','El área máxima no puede ser menor al área mínima')
        return self.cleaned_data



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

class GastoModelForm(ModelForm):
    class Meta:
        model=Gastos
        fields=['herramientas','facturas','imprevistos','Descripcion','fecha','usuario']
        labels= {'herramientas':('Herramientas'),'facturas':('Facturas'),'imprevistos':('Imprevistos'),'Descripcion':('Descripción'),'fecha':('Fecha del gasto'),'usuario':('usuario')}
        widgets={'fecha':forms.SelectDateWidget()
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
        if hoy<fecha:
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
    
