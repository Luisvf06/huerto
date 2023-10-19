# huerto
Proyecto de aplicación para gestionar un huerto. La idea es que los usuarios se registren en ella y la usen tanto para informarse de las necesidades y cuidados de las plantas que tienen, como para compartir ideas y experiencias con otros usuarios. 

El modelo Evento relaciona los modelos planta y Calendario. No estoy totalmente seguro que sea necesario añadir ese modelo intermedio, pero de todas las relaciones que pude crear, era la que más podía necesitar de uno.

En cuanto a la tabla riego, no estaba seguro si incluirlo como tabla independiente o como un atributo dentro de calendario, ya que puede considerarse un evento periódico, pero dado que el riego puede tener ciertos atributos como la sustancia utilizada, decidí separarlo.

En el modelo Usuario he puesto el atributo ciudad con la idea de acceder a las coordenadas y a partir de ellas extraer datos climáticos de algún registro de forma que se pueda recomendar a cada usuario qué planta le resultaría más fácil cuidar según los factores ambientales (horas de luz y Tª), aunque esto sería una idea para ejecutar a largo plazo.