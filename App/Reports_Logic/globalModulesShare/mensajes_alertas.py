import os
import json
from PyQt6.QtWidgets import QMessageBox, QPushButton
import pandas as pd

class Mensajes_Alertas:
    def __init__(self=None, titulo=None, mensaje=None, icono = QMessageBox.information,  texto_detallado=None, botones=[("Aceptar",QMessageBox.StandardButton.Ok)]):
        self.Titutlo = titulo
        self.Mensaje = mensaje
        self.Icono = icono
        self.Texto_Detallado = texto_detallado
        self.Botones = botones
        self.Ventana = QMessageBox()
        
    @property
    def mostrar(self):
        self.Ventana.setWindowTitle(self.Titutlo)
        self.Ventana.setText(self.Mensaje)
        self.Ventana.setIcon(self.Icono)
        if (self.Texto_Detallado != ""):
            self.Ventana.setDetailedText(self.Texto_Detallado)
        else:
            pass
        for texto, callback in self.Botones:
            texto_boton = QPushButton(texto)
            texto_boton.clicked.connect(callback)
            self.Ventana.addButton(texto_boton, QMessageBox.ActionRole)
        return self.Ventana.exec_()
    @property
    def Apartado_Ayuda(self):
        self.Ventana.setWindowTitle(self.Titutlo)
        self.Ventana.setText(self.Mensaje)
        self.Ventana.setIcon(self.Icono)
        if (self.Texto_Detallado != None):
            self.Ventana.setDetailedText(self.Texto_Detallado)
        else:
            self.Ventana.setDetailedText('Desarrollador: Luis Angel Vallejo Pérez\nNúmero de Celular: 2713997432\nCorreo Electronico: angelvallejop9610@gmail.com')
        # for texto, rol in botones:
        #     self.Ventana.addButton(QPushButton(texto), rol)
        for texto, callback in self.Botones:
            texto_boton = QPushButton(texto)
            texto_boton.clicked.connect(callback)
            self.Ventana.addButton(texto_boton, QMessageBox.ActionRole)
        return self.Ventana.exec_()
    @property
    def Eliminar_vacio(self):
        self.Ventana.setWindowTitle("Eliminar")
        self.Ventana.setText("No se encuentran documentos en la direccion de archivos procesados.")
        self.Ventana.setIcon(QMessageBox.Information)
        if (self.Texto_Detallado != None):
            self.Ventana.setDetailedText(self.Texto_Detallado)
        else:
            pass
        for texto, callback in self.Botones:
            texto_boton = QPushButton(texto)
            texto_boton.clicked.connect(callback)
            self.Ventana.addButton(texto_boton, QMessageBox.ActionRole)
        return self.Ventana.exec_()
    @property
    def Eliminar_lleno(self):
        self.Ventana.setWindowTitle("Eliminar")
        self.Ventana.setText("Al aceptar, se eliminará todo el contenido de los documentos procesados sin tener la posibilidad de recuperarlo.")
        self.Ventana.setIcon(QMessageBox.Warning)
        if (self.Texto_Detallado != None):
            self.Ventana.setDetailedText(self.Texto_Detallado)
        else:
            pass
        for texto, callback in self.Botones:
            texto_boton = QPushButton(texto)
            texto_boton.clicked.connect(callback)
            self.Ventana.addButton(texto_boton, QMessageBox.ActionRole)
        return self.Ventana.exec_()
    
