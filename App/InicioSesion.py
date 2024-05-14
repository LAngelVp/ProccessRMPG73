import os
from PyQt6 import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from Reports_Logic.globalModulesShare.resources import *
from Front.inicio_sesion import UI_Inicio_Sesion
from Reports_Logic.globalModulesShare.mensajes_alertas import Mensajes_Alertas
from Home import *


class InicioSesion(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.ui = UI_Inicio_Sesion()
        self.ui.setupUi(self)
        self.setWindowTitle("Inicio de Sesión")
        self.setWindowIcon(QIcon(":/Source/LOGO_KREI_3.ico"))
        self.__User__ = "kenworth del este"
        self.__Password__ = "RMPG#73:)"
        self.ui.btn_aceptar_ingreso.clicked.connect(self.Ingresar)

    def Aceptar_callback(self):
        pass
    
    def Ingresar(self):
        user = self.ui.txt_usuario.text()
        password = self.ui.txt_usuarioPassword.text()
        if all((user, password)):
            if (user == self.__User__) and (password == self.__Password__):
                ventana = PrincipalWindow()
                ventana.show()
                self.close()
            else:
                Mensajes_Alertas(
                    "Error de inicio de sesión",
                    f"No ingresaste las credenciales correctas",
                    QMessageBox.Icon.Critical,
                    None,
                    botones=[
                        ("Aceptar", self.Aceptar_callback)
                    ]
                ).mostrar
        else:
            Mensajes_Alertas(
                    "Falta de datos",
                    f"Los campos no estan completos",
                    QMessageBox.Icon.Critical,
                    None,
                    botones=[
                        ("Aceptar", self.Aceptar_callback)
                    ]
                ).mostrar

def main():
    app = QApplication(sys.argv)
    ventana_principal = InicioSesion()
    ventana_principal.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()