Gabriela: vista Recomendacion plantas por estacion
    Uso el campo epoca_siembra, accedo al mes para ver la estacion con un if en la template y hacer que se muetre el nombre de las plantas que tienen esa fecha establecida
    Hecha: he creado 4 url uno para cada estación y cada uno devuelve las plantas de esa estación


Manuel: diferenciar  huertos disponibles y no y poner una lista con los huertos disponibles
    Creo un atributo de tipo booleanfield para el modelo Huerto con el nombre "disponible" si es true se mostrará y si no no.


Irene: en un huerto que aparezca cuando recolectar cada planta
    en el modelo planta tengo el campo recoleccion como datefield. Accedo a las plantas de un huerto en concreto y comparo las fechas

Alvaro:Imagenes de las plantas 


Alberto: Aviso de cuando regar con alert al hacer login
    acceder a la tabla intermedia de planta_regada, ver la fecha de riego, ver la fecha actual, si pasa de X tiempo, que salte el alert o lo que sea

Ivan: plagas posibles de un huerto en funcion de sus plantas
    Tengo que modificar la relacion planta-plaga para que sea n-m, crear una intermedia y en esa poner el total de plagas por planta, acceder a ella desde huerto para ver el total de plagas que puede tener ese huerto

Elvis: Hacer login de Google