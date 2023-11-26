from django.forms import ModelForm
from django import forms
from .models import *
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
        
        if not (re.match(r'\d+\.?\d*$',str(acidez))):
            self.add_error('acidez','debe ser un número entre 0 y 14')
        if not (0<acidez<=14):
            self.add_error('acidez','debe ser un número entre 0 y 14')
            
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
        super.clean()
        textoBusqueda= self.cleaned_data.get('textoBusqueda')
        sitio=self.cleaned_data.get('sitio')
        sustrato=self.cleaned_data.get('sustrato')
        area_minima=self.cleaned_data.get('area_minima')
        area_maxima=self.cleaned_data.get('area_maxima')
        abonado=self.cleaned_data.get('abonado')

        if (textoBusqueda ==""
            and len(sitio)==0
            and len (sustrato)==0
            and area_minima==""
            and area_maxima==""):
            self.add_error('textoBusqueda','Debe introducir al menos un valor')
            self.add_error('sitio','Debe escoger al menos una opción')
            self.add_error('sustrato','Debe escoger al menos una opción')
            self.add_error('area_minima','Debe indicar al menos un valor')
            self.add_error('area_maxima','debe indicar al menos un valor')#esto no tiene mucho sentido por el booleanfield, pero lo dejo para probar si funciona o no
        else:
            ubicacion2=textoBusqueda.split(",")
            if(len(textoBusqueda.split(""))!=2):
                self.add_error('textoBusqueda','Debes introducir dos valores numéricos separados por coma')
            if(textoBusqueda!="" and (float(ubicacion2[0])<-90 or float(ubicacion2[0])>90)and (float(ubicacion2[1])<-180 or float(ubicacion2[1])>180)):
                self.add_error('textoBusqueda','El primer valor debe estar entre -90 y 90 y el segundo entre -180 y 180')

            if(not area_minima is None and not area_maxima is None and area_minima>area_maxima):
                self.add_error('area_minima','El área mínima no puede ser mayor al área máxima')
                self.add_error('area_maxima','El área máxima no puede ser menor al área mínima')
        return self.cleaned_data
