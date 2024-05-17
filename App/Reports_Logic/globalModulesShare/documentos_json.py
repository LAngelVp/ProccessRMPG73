import os
import json
import random
import string
from PyQt6.QtWidgets import QMessageBox
from .mensajes_alertas import Mensajes_Alertas
class creacion_json():
    def __init__(self, ruta = None, nombre = None, objeto = None): #comment : ingresamos la ruta del documento y el objeto a crear.
        super().__init__()
        self.ruta = ruta
        self.nombre = nombre
        self.direccion = os.path.join(self.ruta,self.nombre)
        self.objeto = objeto
        self.__contenido_vacio_json = []

    def Aceptar_callback(self):
        pass

    def deleteDocument(self, documento):
        os.remove(documento)
        self.comprobar_existencia
#comment: comprueba si existe un documento
    @property
    def comprobar_existencia(self):
        if os.path.exists(self.direccion):
            try:
                with open(self.direccion, "r",encoding='utf-8') as documento:
                    self.documento_existe = json.load(documento)
            except FileNotFoundError:
                Mensajes_Alertas(
                    "Documento no encontrado",
                    "El documento no se encuentra existente en el sistema",
                    QMessageBox.Icon.Warning,
                    None,
                    botones = [
                        ("Construir" , self.aceptarCallback)
                        # ("Construir" , self.buildDocument(self.direccion))
                    ]
                )
            except ValueError as error:
                Mensajes_Alertas(
                    "Documento dañado",
                    "El documento se encuentra afectado debido a una mal estructura, por lo que si aceptas este sera eliminado",
                    QMessageBox.Icon.Warning,
                    None,
                    botones = [
                        ("Entendido" , self.deleteDocument(self.direccion))
                    ]
                )
        else:
            self.documento_existe = self.__contenido_vacio_json
            with open(self.direccion, "w", encoding='utf-8') as documento:
                json.dump(self.documento_existe, documento,ensure_ascii=False)

            with open(self.direccion, "r") as documento:
                self.documento_existe = json.load(documento)
                return self.documento_existe
        return self.documento_existe
  
    @property
    def agregar_json(self):
        self.comprobar_existencia
        self.longitud = 15
        self.cadena = string.ascii_letters+string.digits
        self.id = ''.join(random.choices(self.cadena, k=self.longitud))

        try:
            self.nuevo_objeto = {"id": self.id}
            self.nuevo_objeto.update(self.objeto)
            self.__contenido_vacio_json.append(self.nuevo_objeto)

            self.comprobar_existencia.extend(self.__contenido_vacio_json)

            self.sobre_escribir_json(self.documento_existe)
        except Exception as e:
            Mensajes_Alertas(
                    "Error",
                    f"Hubo un error al ingresar los datos.\n{e}",
                    QMessageBox.Icon.Warning,
                    None,
                    botones=[
                        ("Aceptar", self.Aceptar_callback)
                    ]
                ).mostrar

    
    @property
    def eliminar_datos_json(self):
        documento = self.comprobar_existencia
        valor_id = self.objeto
        id = valor_id["id"]
        for elemento in documento:
            if elemento["id"] == id:
                documento.remove(elemento)
                break
        self.sobre_escribir_json(documento)
    @property
    def obtener_datos_json_por_id(self):
        documento = self.comprobar_existencia
        id = self.objeto["id"]
        for elemento in documento:
            if elemento["id"] == id:
                return elemento

    def actualizar_datos(self, nuevos_datos):
        # Cargar el JSON desde el archivo
        datos = self.comprobar_existencia
        
        # Buscar el registro con el ID buscado y actualizar sus datos
        for registro in datos:
            if registro["id"] == self.objeto["id"]:
                registro.update(nuevos_datos)
                break
        
        self.sobre_escribir_json(datos)
    
    def sobre_escribir_json(self,documento):
        with open(self.direccion, "w", encoding='utf-8') as archivo:
            json.dump(documento, archivo, indent=4, ensure_ascii=False)
