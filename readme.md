Se necesita installar Pillow para trabajar con imagenes

    pip install pillow

Existe un usuario administrador:
    
    username = admin
    
    pass = 1234
    
El formulario para hacer login no está definida, por lo que se necesita 
entrar a http://localhost:8000/admin para iniciar sesión, entonces dirigirse 
a la pagina principal.

En la página principal existe el hipervinculo a cerrar sesión, este si está 
funcionando correctamente. 

### Importante:
Faltan las funciones que se encargan de guardar los modelos creados

## APIs y Bases de datos

####Información nutricional y lista de alimentos

Existe https://fdc.nal.usda.gov/index.html pagina gubernamental de EEUU que 
tiene información de muchos tipos de alimentos, esta información incluye:
* Producto
* Estado (crudo o no (?))
* Aporte nutricional
* Marca (Brand)
* Categoría del alimento
* Ingredientes
* Fuente de la información proporcionada
* otros

Tienen APIs para trabajar con sus datos y una librería en python.
Está en inglés, por lo que la información como los nombres de aliementos 
debería ser traducida a español. Por esto, una idea puede ser automatizar la 
búsqueda y traducción de productos en la base de datos. Entonces, volcar los 
datos mientras se van recopilando, traduciendo y filtrando, dentro de 
archivos JSON o csv . Una vez hecho esto, volcar la información a la base de 
datos que usemos y llenar los productos existentes.

Hacer este trabajo sirve para filtrar los elementos repetidos de la base de 
datos (por ejemplo, manzana vs manzana de una marca determinada). Otra opción
 es usar directamente la información de la base de datos, pero creo que el 
 exceso de información hará dificil controlar las recomendaciones, opciones 
 de autcompletar en texto (si es que se integrará).
 
 ##### Propuesta:
 Hacer lo mencionado, y generar una base de datos propia a partir de la 
 recolección de información del sistema existente.
 
 Usar la información proporcionada sólo por la FNDDS y no las marcas.
 
 Almacenar los datos de alimentos no procesados ie. omitir los valores de 
 alimentos de alta preparación/ comidas completas. 
 
    API FNDDS python: https://pypi.org/project/python-usda/
    
De manera alternativa se puede intentar encontrar la información de INFOODS 
de la FAO y obtener la información relevante desde ahí. A nivel Chile parece 
no haber una base de datos enfocada a los alimentos.

FAO: http://www.fao.org/infoods/infoods/tablas-y-bases-de-datos/es/


##TODO
Información de las cosas
 
 Agregar metodo que permita agregar usuarios a inventarios y listas de compras
 
 Comprobar tipo de canales para los datos compartidos (inventario y lista de
  compras)

Agregar Slugs donde sea necesario: Inventario y lista de compras?