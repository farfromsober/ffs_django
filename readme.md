# 4sale - Backend
---
Proyecto Final

KeepCoding Startup Engineering Master Boot Camp

---

### Estructura del proyecto:

* **Aplicaciones**:
	- **'users'**: Contendrá el modelo de usuario. Como en Django no está recomendada la herencia de modelos, se crea una nueva clase 'Profile' que tendrá un oneToOneField a la clase User de Django y añadirá los campos específicos del proyecto.
	- **'images'**: Únicamente encargada de la gestión de imágenes.
	- **'products'**: Aplicación principal, gestiona los modelos Category, Product, SavedSearch y Transaction.

* **Requirements.txt**
	- En este fichero ser irán añadiendo los paquetes necesarios para el proyecto con sus respectivas versiones. Para generarlo de nuevo ejecutar el siguiente comando con el entorno virtual activado:
```
pip freeze > requirements.txt
```
	- Se ha seleccionado la última versión de Django 1.8, indicado en el enunciado de la práctica, la 1.8.6. 
	- El paquete wheel se ha instalado automáticamente, parece que va a ser el nuevo estándar para distribución de python. Se deja incluido en el proyecto por acaso.
	- Para instalar paquetes en el entorno virtual local es recomendable usar:
```
pip install package_name==version
```
Esto es debido a que con el gestor de paquetes de pyCharm a veces no te deja especificar la versión.

* **gitignore**
	- Sacado de gitignore.io combinando el de Python con el de Django. Las reglas propias están añadidas al final.
	- El fichero de settings de producción nunca debe pertenecer al repositorio. Sólo está creado en la máquina de azure y no debe ser distribuido. Podría tener claves de la BD y tendrá la SECRET_KEY del proyecto.

## Modelo de datos:

####App 'users'
* **Profile**: 
	- Latitud y longitud se implementan como tipo float para realizar cálculos en el backend, aunque por la API se enviarán como string.
	- Sales será un field más y se actualizará al cambiar un producto de estado 'en venta' a 'vendido' y viceversa. No se implementa como una función para eliminar dependencia de la app 'products'.
	- Avatar será una url que apunte al recurso en Azure.
	- City y state podrán ser nulos. Se usarán para asignar una localización por defecto si el usuario tiene desactivada la localización.

####App 'products'
* **Product**:
	- Price se implementa como float aunque se enviará con la API como una string.
	- Selling será un boolean, True para 'en venta, False para 'vendido'.
	- La categoría puede ser nula, ya que al eliminar una categoría no queremos eliminar el producto.

* **Category**
	- Se le añade un index para ordenar las categorías según nos parezca. Este index es único, no puede estar repetido.

* **Transaction**
	- Usamos 'related_name' para seller y buyer porque ambas son claves foráneas al mismo modelo, entonces si no especificamos un nombre la relación inversa sería igual.

###App 'images'
* **Image**
	- No será de tipo ImageField, simplemente tiene el field url que apunta al recurso de azure.



## Procedimientos habituales

###Preparación del entorno en local
Seguir pasos descritos en vídeo de preparación subido a drive.

###Actualización del servidor de producción
1. Conectar a la máquina de azure por ssh. ```ssh azureuser@forsale.cloudapp.net```
2. Nos movemos a la carpeta de la app. ```cd /var/www/ffs_django/app/```
3. Ejecutamos el script de actualización ```sudo ./update.sh```

## Consideraciones generales
* Nunca ejecutar el makemigrations en el servidor, las migraciones se generan en local, viajan con el repositorio y se aplican en el servidor con el script de actualización.
