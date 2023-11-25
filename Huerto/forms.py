from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.gis.forms import PointField
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

    area_minima=forms.FloatField(label="Área mínima",required=False,widgets=[forms.NumberInput(attrs={'type': 'number', 'step': '0.01'}),
                forms.NumberInput(attrs={'type': 'number', 'step': '0.1'})])
    
    area_maxima=forms.FloatField(label="Área máxima",required=False,widgets=[forms.NumberInput(attrs={'type': 'number', 'step': '0.01'}),
                forms.NumberInput(attrs={'type': 'number', 'step': '0.1'})])
    
    abonado=forms.BooleanField(required=False)

    ubicacion = forms.CharField(label="Ubicación",required=False,  widget=forms.TextInput(attrs={'placeholder': 'Ingrese la ubicación'}))#de momento no consigo hacer funcionar los widgets que encuentro para plainlocationfield
