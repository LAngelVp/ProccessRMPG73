import os
import json
import random
import string
from PyQt5.QtWidgets import QMessageBox, QPushButton
import pandas as pd
class creacion_json():
    def __init__(self, ruta = None, nombre = None, objeto = None):
        super().__init__()
        self.ruta = ruta
        self.nombre = nombre
        self.direccion = os.path.join(self.ruta,self.nombre)
        self.objeto = objeto
        self.__contenido_vacio_json = []


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
            print(e)

    
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
        with open(self.direccion, "w", encoding='utf-8', errors='ignore') as archivo:
            json.dump(documento, archivo, indent=4)


    def Mensaje(self, mensaje, titulo, icono = QMessageBox.Information, botones = [QMessageBox.Ok]):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(titulo)
        msg_box.setIcon(icono)
        msg_box.setText(mensaje)
        for boton in botones:
            if isinstance(boton, QPushButton):
                msg_box.addButton(boton)
        return msg_box.exec_()