# Este programa es para la automatizacion de reportes de kenworth del este,
# con el objetivo de minimizar el tiempo de trabajo y aumentar el niver de desarrolla, para que la empresa pueda ingresar mas sucursales al plan de trabajo.
# Todo sin un mayor esfuerzo.

Para poder hacer ejecutable el programa y de ese modo distribuirlo, necesitamos la creacion de un archivo ejecutable para que los compañeros del area tambien puedan tener acceso al software.
¿Como lo vamos a lograr?
muy sencillo...
con el siguiente comando en consola, podemos convertir el software en un ejecutable:

# pyinstaller --windowed --onefile --icon=./nombre del archivo "nombre del archivo.py"

El archivo tengo entendido que debe de ser el index.
Tambien se le puede crear una imagen de logo, solo colocando a nivel de raiz una imagen con extension .ico.


pyrcc5 resources.qrc -o resources.py
EntornoVirtual\Scripts\activate
pyinstaller --onefile --name "ProcesadorSDR" --icon="LKW.ico" --windowed "Index.py"