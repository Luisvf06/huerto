Gabriela: vista Recomendacion plantas por estacion
    Uso el campo epoca_siembra, accedo al mes para ver la estacion con un if en la template y hacer que se muetre el nombre de las plantas que tienen esa fecha establecida
    Hecha: he creado 4 url uno para cada estación y cada uno devuelve las plantas de esa estación


Manuel: diferenciar  huertos disponibles y no y poner una lista con los huertos disponibles
    Creo un atributo de tipo booleanfield para el modelo Huerto con el nombre "disponible" si es true se mostrará y si no no.


Irene: en un huerto que aparezca cuando recolectar cada planta
    en el modelo planta tengo el campo recoleccion como datefield. Accedo a las plantas de un huerto en concreto y comparo las fechas

Alvaro:Imagenes de las plantas 
    No funciona

Alberto: Aviso de cuando regar con alert
    acceder a la tabla intermedia de planta_regada, ver la fecha de riego, ver la fecha actual, si pasa de X tiempo, que salte el alert o lo que sea

Ivan: plagas posibles de un huerto en funcion de sus plantas
    Tengo que modificar la relacion planta-plaga para que sea n-m, crear una intermedia y en esa poner el total de plagas por planta, acceder a ella desde huerto para ver el total de plagas que puede tener ese huerto

Elvis: Hacer login de Google

Para asegurarte de haber creado un objeto SocialApp para el proveedor de autenticación de Google en tu base de datos, puedes seguir estos pasos:

Panel de administración de Django:

Inicia sesión en el panel de administración de tu aplicación Django.
Navega a la sección de "Social applications" o "Aplicaciones sociales".
Deberías encontrar una opción para agregar un nuevo objeto SocialApp.
Selecciona el proveedor de autenticación de Google y proporciona la información necesaria, como el ID del cliente y el secreto del cliente que obtuviste al registrar tu aplicación en Google Developer Console.
Utilizando la API de Django:
Puedes crear objetos SocialApp programáticamente utilizando la API de Django. Aquí hay un ejemplo de cómo podrías hacerlo en un script de gestión de Django o en un archivo de migraciones:

python
Copy code
from allauth.socialaccount.models import SocialApp

# Verifica si ya existe un objeto SocialApp para el proveedor de autenticación de Google
social_app, created = SocialApp.objects.get_or_create(provider='google')

# Si no existe, configura los campos necesarios
if created:
    social_app.name = 'Google'
    social_app.client_id = 'tu-client-id'
    social_app.secret = 'tu-secreto'
    social_app.save()
En este código, 'tu-client-id' y 'tu-secreto' son los valores que obtuviste al registrar tu aplicación en Google Developer Console.

Asegúrate de ejecutar este código en un lugar adecuado, como un archivo de migraciones o un script de gestión de Django, para garantizar que se cree el objeto SocialApp en tu base de datos. Una vez creado, podrás utilizar la autenticación de Google en tu aplicación Django utilizando django-allauth.