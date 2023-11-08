![Kenworth del este](https://github.com/LAngelVp/programakw/blob/master/App/Source/LOGO_KWE.png)

# **Automatización de reportes**
Esta aplicación esta desarrollada con el lenguaje de programación **Python**, librerias de analisis de datos **Pandas**, libreria de desarrollo de interfaz de escritorio **PyQT5**.

# **Problematica**
El departamento de **Inteligencia de negocios** realizá reportes de manera manual con el apoyo de microsoft excel. Debido a la gran cantidad de tiempo que estos se llevan para quedar 100% listos para poder cargar los archivos a **SalesForces Analytics** y de esa manera estructurarlos para mostrar toda la data de manera grafica para todos los departamentos de la empresa **Kenworth del Este**. Consecuentemente a la gran cantidad de tiempo que se lleba hacer todo el proceso, se recurrio a la idea de desarrollar la automatización de todos los reportes que se hacian y se haran en un futuro.

# **Propuesta**
La propuesta para dicha problematica fue desarrollar una aplicación con el lenguaje de programación **Python** debido a que esta orientado a las areas de analisis de datos e inteligencia artificial. Ademas, para el analisis y tratamiento de datos, se opto por la libreria de pandas, ya que, se puede analizar una gran cantidad de datos de una manera muy eficiente, rapida y fiable.
Por otra parte, con la ayuda de la libreria de PyQT5 se tenia que desarrollar una interfaz grafica para el usuario y una experiencia de usuario fuida.

# **Explicación**
Para la lógica para la automatización de cada uno de los reportes, fue adquirida e implementada bajo la experiencia y el proceso de desarrollo de cada uno de los reportes, y debido a que no solo se iba a operar con el concesionario **Kenworth del Este** se tenia que desarrollar una interfaz grafica independiente a cada uno de los concesionarios que mas adelante se fueran a integrar debido a que cada concesionario manejaria su proceso y lógica muy independiente de cada concesionario.
Cada concesionario tendra su cantidad de reportes a procesar de manera automatica, y debido a eso, se estipulo una nomenclatura para el nombre de los archivos de excel y una restricción para su extension de archivos, los archivos solo tienen y tendran que ser de extensión (.xlsx) y su nomenclatura esta estipulada en un documento digital, el cual se encuentra en el apartado de ayuda, que es un boton que esta úbicado en la parte inferior derecha con el icono de una cabeza y signo de interrogación dentro, permitiendo al sistema lanzar una ventana emergente con los datos del desarrollador y un botón para aceptar y otro para ir al documento digital que se encuentra en linea, que contiene todas las nomenclaturas de los nombres de los documentos para poder subirlos y que estos sean procesados de manera correcta, de lo contrario seran colocados en una carpeta de errores.

Cuando los documentos sean procesados de manera correcta para cada uno de los concesionarios, estos seran enviados a una carpeta de archivos procesados, teniendo como resultado el documento procesado en la carpeta antes mencionada y una previsualización de los nombres de los archivos en una ventana del lado derecho con el titulo de procesados. Los documentos seran nombrados de forma detallada y de manera emblematica a su contenido y reporte al igual que la fecha en la que se realizarón.

En las ventanas principales de cafa uno de los concesionarios, contendran 6 botones importantes y muy aparte del botón de ayuda que serviran como apoyo para poder ingresar de manera mas rapida a las siguientes rutas:

- **Boton de Procesados** : Dirige a la ruta de los documentos que ya fueron procesados de manera correcta.
- **Botón de Originales** : Dirige a la ruta de documentosz originales, esta ruta almacena los documentos originales de los reportes por lo que cada vez que se realicen los sobreescribira.
- **Botón de Errores** : Dirige a la ruta de los documentos errores que se intentarón procesar.
- **Botón de Subir** : Abre el gestor de archivos del sistema para poder subir a la aplicación los documentos que se quieren procesar.
- **Botón de Eliminar** : Permite eliminar todos los documentos que estan el la ruta de procesados, eliminando su previsualización.
- **Botón de Comenzar** : Permite comenzar el ciclo de automatización de la aplicación.

Finalmente, esta aplicación es solo para uso personal del desarrollador **Luis Ángel Vallejo Pérez**.

# **Descripción de la estructura del código**
La estructura del programa se encuentra estipulada y organizada de la siguiente manera:

- **Source** : Módulo que contiene todas las imagenes.
- **Front** : Módulo que contiene todas la IU.ui
- **Reports_Logic** : Módulo que contiene toda la lógica del de darrollo de la funcionalidad de las UI de los concesionarios y la automatización de los reportes.
- **Archivo Home.py** : Es la ventana principal en donde comenzará todo.
- **VPrincipal.py** : Es la UI principal.
- **resources.py** : Archivo que contiene de manera binaria todas las imagenes.

Dentro de la carpeta de **Reports_Logic** se encuentran las carpetas de los distintos concesionarios:

+ **Kenworth del este.**
+ **Kenworth del rio bravo.**
+ **KREI.**
+ **Kenworth sonora**

Dentro de cada una de estas carpetas se encuentra la logica de su IU y proceso de desarrollo.

--------------------------------------------------------

## **Comandos de soporte:**
~~~~~
Ejecutable de la aplicación:
[pyinstaller --onefile --name "ProcesadorRMPG" --icon="LKW.ico" --windowed "Home.py"]
~~~~~
~~~
Transformar archivo .qrc a .py, por ejemplo para las imagenes.
[pyrcc5 resources.qrc -o resources.py]
~~~
~~~
Activar el entorno virtual
[EntornoVirtual\Scripts\activate]
~~~
~~~
comando para convertir un archivo de ui -> py:
pyuic5 -x Comenzar.ui -o Comenzar.py
~~~
~~~
Para poder hacer una ventana con bordes redondeados, debemos de hacer lo siguiente:
    Debemos de importar la libreria:
    from PyQt5.QtCore import Qt
    
    1.- La ventana le debemos de quitar la barra superior en donde aparecen los botones de manipulacion por defecto, colocando el siguiente codigo:
    self.setAttribute(Qt.WA_TranslucentBackground)

    2.- Posteriormente a eso, debemos de darle un border-radius al widget principal que contendra todos los controles de la ventana y estipulando que la ventana principal se vea totalmente transparente con el siguiente codigo:
    self.setAttribute(Qt.WA_TranslucentBackground)
~~~
![Python](https://codetorial.net/pyqt5/_images/0_pyqt_logo.png)
![Pandas](https://www.kindpng.com/picc/m/159-1595924_python-logo-clipart-easy-pandas-python-logo-hd.png)
