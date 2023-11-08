from django.contrib import admin
from .models import Huerto
from .models import Usuario
from .models import Blog
from .models import Incidencia
from .models import Planta
from .models import Gastos
from .models import Contrasenha
from .models import Plaga
from .models import Historial
from .models import Tratamiento
from .models import Evento
from .models import Riego
from .models import Planta_regada
from .models import Fruto
from .models import Calendario
from .models import Banco
from .models import Votacion
# Register your models here.
admin.site.register(Banco)
admin.site.register(Votacion)
admin.site.register(Huerto)
admin.site.register(Usuario)
admin.site.register(Blog)
admin.site.register(Incidencia)
admin.site.register(Planta)
admin.site.register(Gastos)
admin.site.register(Contrasenha)
admin.site.register(Plaga)
admin.site.register(Historial)
admin.site.register(Tratamiento)
admin.site.register(Evento)
admin.site.register(Riego)
admin.site.register(Planta_regada)
admin.site.register(Fruto)
admin.site.register(Calendario)