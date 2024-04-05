import os
import json
class creacion_json():
    def __init__(self, ruta = None, nombre = None, objeto = None):
        super().__init__()
        self.ruta = ruta
        self.nombre = nombre
        self.direccion = os.path.join(self.ruta,self.nombre)
        self.objeto = objeto
        self.__contenido_vacio_json = []


    @property
    def actualizar_json(self):
        self.comprobar_existencia
        try:

            self.__contenido_vacio_json.append(self.objeto)

            self.comprobar_existencia.extend(self.__contenido_vacio_json)

            with open(self.direccion, "w") as archivo:
                json.dump(self.documento_existe, archivo, indent=4)
        except Exception as e:
            print(e)

    @property
    def comprobar_existencia(self):
        if os.path.exists(self.direccion):
            try:
                with open(self.direccion, "r") as documento:
                    self.documento_existe = json.load(documento)
            except FileNotFoundError:
                print("EL DOCUMENTO NO PUEDE ABRIRSE")
                # raise
            except ValueError as error:
                print(
                    "El documento se encontraba dañado, por lo que se procedio a crear de nuevo"
                )
                os.remove(self.direccion)
                self.comprobar_existencia
        else:
            self.documento_existe = self.__contenido_vacio_json
            with open(self.direccion, "w") as documento:
                json.dump(self.documento_existe, documento)

            with open(self.direccion, "r") as documento:
                self.documento_existe = json.load(documento)
                return self.documento_existe
        return self.documento_existe