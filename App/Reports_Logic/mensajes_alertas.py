import os
import json
from PyQt5.QtWidgets import QMessageBox, QPushButton
import pandas as pd

class Mensajes_Alertas:
    @staticmethod
    def mostrar(titulo, mensaje, icono = QMessageBox.Information, botones = [("Aceptar", QMessageBox.AcceptRole)]):        
        msg_box = QMessageBox()
        msg_box.setWindowTitle(titulo)
        msg_box.setIcon(icono)
        msg_box.setText(mensaje)
        for texto, rol in botones:
            msg_box.addButton(QPushButton(texto), rol)
        return msg_box.exec_()