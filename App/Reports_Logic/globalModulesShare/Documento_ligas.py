import os
import json
from .ContenedorVariables import Variables
class CreacionJson():
    def __init__(self, nombre_documento=None, ruta_destino_documento=None, extension = None):
        self.nombre_documento = nombre_documento
        self.ruta_destino_documento = ruta_destino_documento
        self.extentension_documento = extension
        self.__contenido_vacio_json = []
        # Variables().comprobar_rutas_documentos_rutas
        self.__ruta_base_documento_json = Variables().documentSavingPaths

    @property
    def comprobar_existencia(self):
        
        if os.path.exists(self.__ruta_base_documento_json):
            try:
                with open(self.__ruta_base_documento_json, "r") as documento:
                    self.documento_existe = json.load(documento)
            except FileNotFoundError:
                print("EL DOCUMENTO NO PUEDE ABRIRSE")
                # raise
            except ValueError as error:
                print(
                    "El documento se encontraba dañado, por lo que se procedio a crear de nuevo"
                )
                os.remove(self.__ruta_base_documento_json)
                self.comprobar_existencia
        else:
            self.documento_existe = self.__contenido_vacio_json
            with open(self.__ruta_base_documento_json, "w") as documento:
                json.dump(self.documento_existe, documento)

            with open(self.__ruta_base_documento_json, "r") as documento:
                self.documento_existe = json.load(documento)
                return self.documento_existe
        return self.documento_existe

    @property
    def Agregar_ruta(self):
        self.comprobar_existencia
        nombre = self.nombre_documento
        self.nueva_direccion = {
            "Nombre_documento": self.nombre_documento + self.extentension_documento,
            "Ruta_destino_documento": self.ruta_destino_documento,
        }
        self.__contenido_vacio_json.append(self.nueva_direccion)

        self.comprobar_existencia.extend(self.__contenido_vacio_json)

        with open(self.__ruta_base_documento_json, "w") as documento:
            json.dump(self.documento_existe, documento, indent=4)

    def Eliminar_ruta(self, nombre, ruta):
        try:
            self.ruta = self.comprobar_existencia
        except FileNotFoundError:
            print("No se encontro la data")
        except ValueError:
            print("Documento Error")
            os.remove(self.__ruta_base_documento_json)
        # COMMENT : recorremos el json y en caso de coincidencia, agregamos el indice al array de eliminados.
        for i, direccion in enumerate(self.ruta):
            if (direccion["Nombre_documento"] == nombre) and (
                direccion["Ruta_destino_documento"] == ruta
            ):
                self.__contenido_vacio_json.append(i)
            else:
                pass
        for indice_registro_eliminar in reversed(self.__contenido_vacio_json):
            del self.ruta[indice_registro_eliminar]

        with open(self.__ruta_base_documento_json, "w") as documento:
            json.dump(self.ruta, documento, indent=4)
                

