from django.forms import ModelForm
from .models import *
class HuertoForm(ModelForm):
    class Meta:
        model = Huerto
        fields=['ubicacion','sitio','sustrato','area','acidez','abonado','usuario']
        labels={
            "ubicacion": ("Ubicación del huerto"),"sitio":("Sitio"),
                "sustrato":("Sustrato"),
                "area":("Área"),
                "acidez": ("Acidez"),
                "abonado":("Abonado"),
                "usuario":("Usuario"),
                }
        help_text= {
            "area":("En metros cuadrados"),
        }
        widgets={   
        }
        localized_fields=[]
        def clean(self):
            super().clean()         
            ubicacion=self.cleaned_data.get('nombre_usuario')
            sitio=self.cleaned_data.get('nombre')
            sustrato=self.cleaned_data.get('apellidos')
            area=self.cleaned_data.get('email')
            acidez=self.cleaned_data.get('telefono')
            abonado=self.cleaned_data.get('ciudad')
            usuario=self.cleaned_data.get('usuario')
            
            huertoubicacion=Huerto.objects.filter