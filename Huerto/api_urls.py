from django.urls import path
from .api_views import *
urlpatterns = [
    path('huertos',huerto_list),
    path('huerto_busqueda_simple',huerto_buscar),
    
    
]