# PRA1: ¿Cómo podemos capturar los datos de la web?

## Integrantes del grupo:
- **Alba Sanz Horcajo**
- **Carlos Santamaría de las Heras**

### Descripción

En un ambiente de precios de viviendas cada vez más caras, con unos tipos de interés recuperando máximos de hace años, se plantea un proyecto analítico capaz de ayudar a comparar inmuebles en venta en Madrid capital. 
Para ellos se ha elegido un portal web inmobiliario especializado en la compraventa y alquiler de viviendas en España como es Fotocasa (https://www.fotocasa.es/es/). 
El objetivo será el de generar un fichero que cualquier persona pueda entender y filtrar según las diferentes caracterísitcas que se ajusten a sus necesidades, ayudando así a la búsqueda de la vivienda.

Para ejecutar el script es necesario instalar las bibliotecas que aparecen en el documento requirements.txt:

* beautifulsoup4~=4.11.1
* selenium~=3.141.0
* requests~=2.28.1
* pandas~=1.4.4
* bs4~=0.0.1

Los campos que se extraen son: 
* precios
* m2 
* planta 
* baños
* habitaciones 
* calefaccion
* aireAC 
* ascensor
* enlaces
* titulos

### Ficheros y enlaces

* El fichero ejecutable se llama: **main.py**
* El fichero .csv generado se llama: **Inmuebles en venta en Madrid Capital.csv**
* La memoria se llama **memoria.pdf**
* El fichero **requirements.txt** y **robots.txt** se encuentran en la carpeta /source
* El DOI de Zenodo del dataset generado es el siguiente: *https://doi.org/10.5281/zenodo.7348662*

