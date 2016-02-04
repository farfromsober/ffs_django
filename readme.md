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


# Construcción API

Para construir un api para una entidad/conjunto de entidades del modelo, hemos utilizado las siguientes clases que Django.

- Serializers: Serializadores que permiten transformar objetos python en objetos jason y viceversa
- GenericViewSet: Clases que proveen acciones para listar, crear, actulizar y eliminar a través del protocolo http.
- FilterSet:  Clases que permiten definir filtros para una entidad
- BasePermissions: permite definir permisos a nivel método y a nivel objeto
- APITestCase: Permite definir casos de prueba para servicios.

##  Serializers

1. Crear un archivo serializers.py en la app si no existe
2. Por cada entidad involucrada en los servicios cree al menos un serializador que herede de serializer.ModelSerializer y defina los campos que se utilizan en la serialización.

```python
class XXXXXSerializer (serializers.ModelSerializer):
    class Meta:
        model = XXXXX
        fields = ('field1','field2','field3',...)
```
Este serializador se puede utilizar para todos los métodos de las api (GET/POST/UPDATE/PUT). Si no se indican campos se usarán todos los del modelo.
Los datos se validan contra las caractarísticas establecidas en el modelo utilizado.
###Casos especiales 

- Si se requiere que el serializador tenga campos diferentes para alguno de los métodos.

Especialice el serializador definiendo los campos que se quieren incluir. Este serializador es el que se va a usar para el método particular. Por ejemplo:

```python
class XXXXXListSerializer(XXXXXSerializer):

    class Meta(XXXXXSerializer.Meta):
	fields = ('field1','field2')
		
```
- Clases anidadas: cuando una objeto de una clase incluye uno de otra clase

1- Haga los serializadores de base. En el serializador de la clase que contiene otra, debe indicar los serializadores que deben tratar los objetos de la otras clase. Por ejemplo, si en la clase XXXXX el  atributo yyy es de la clase YYYYY:

```python
class XXXXXSerializer(serializers.ModelSerializer):

    yyy = YYYYYSerializer()

    class Meta:
        model = YYYYY
        fields = ('field1','field2','field3',...)
```
2- Crear serializadores para el métodos de crear y update con los campos que requiera, Se debe indicar que la clase anidada es un un campo relacionado. 

```python
class XXXXXCreateSerializer(XXXXSerializer):

    yyy = PrimaryKeyRelatedField(read_only='False')

    class Meta(ProductSerializer.Meta):
        fields = ('field1','field2','field3',...)
        
class XXXXXUpdateSerializer(XXXXSerializer):

    yyy = PrimaryKeyRelatedField(read_only='False')

    class Meta(ProductSerializer.Meta):
        fields = ('field1','field2','field3',...)
```
3- Si requiere realizar acciones particulares para uno de los métodos , puede sobreescribir el método respectivo en el serializador. Por ejemplo si requiere realizar unas acciones particulares en el método que crea una instancia.

```python
class XXXXXSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=XXXXX
        fields = ('field1','field2','field3',...)
        
    def create(self, validated_data):
       <accciones particulares>
        return XXXXX
```
##  Views del API
Las vistas de los API se localizan en el archivo api.py. Las vistas heredan de GenericViewSet y definen los métodos create, list, retrieve, update y destroy.
La vista define un serializador y un query, se pueden tambiern definir una clase de permisos y un filtro. Una viste simpl podría ser:

```python
class XXXXXViewSet(GenericViewSet):

    queryset = XXXXX.objects.objects.all()
    serializer_class = XXXXXSerializer
    permission_classes = (XXXXXPermission,)
    filter_class = XXXXXFilter

    def list(self, request):
        xxx = self.filter_class(request.query_params, queryset=self.queryset)
        serializer = XXXXXListSerializer(xxx.qs, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = XXXXXCreateSerializer(data=request.data)
        if serializer.is_valid():
            xxx = serializer.save()
            response_serializer = XXXXXListSerializer(product)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        xxx = get_object_or_404(XXXXX, pk=pk)
        self.check_object_permissions(request, xxx)  
        serializer = XXXXXListSerializer(xxx)
        return Response(serializer.data)

    def update(self, request, pk):
        xxx = get_object_or_404(XXXXX, pk=pk)
        self.check_object_permissions(request, xxx)  
        serializer = ProductUpdateSerializer(instance=product, data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            response_serializer = XXXXXListSerializer(product)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        xxx = get_object_or_404(Product, pk=pk)
        self.check_object_permissions(request, xxx)  
        xxx.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  
```
##  Permisos

Para definir los permisos sobre un API estamos usando permisos a nivel de vista, definiendo una clase uqe hereda de BasePermission, donde implementamos los siguientes métodos.
 
    .has_permission(self, request, view)               // Verifica permisos a nivel método
    .has_object_permission(self, request, view, obj)   // Verifica permisos a nivel objeto

Estos métodos devuelven True para conceder acceso y False de lo contrario. Los métodos deberian ser parecidos a los desarrollados para producto o usuario.

##  URLs
En el archivo api_urls se define el router para el servicio y otros urls específicos, estos urls se incluyen en ffs_django/urls.py.

```
# APIRouter
router = DefaultRouter()
router.register(r'xxxxxs', XXXXXViewSet, base_name='xxxxxs_list_api')

urlpatterns = [
    # API URLs
    url(r'1.0/', include(router.urls)),  # incluyo las URLS de API
    # otras URLs
    ...
]
```
Para incluir en las urls del proyecto agragar las siguientes líneas al archivo ffs_django/urls.py.

```
# XXXXXs URLs
    url(r'api/', include(xxxxxs_api_urls)),
```

##	Test

Para realizar pruebas del API usamos una clase que herede de **APITestCase**. Esto nos da acceso a los métodos assert y a un client con el cual podemos realizar peticiones http a los servicios para hacer las pruebas. En método **setUp** creamos los objetos necesarios para la prueba. Por cada prueba creamos un método cuyo nombre comience con **test**

