import sys
from PyQt6 import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from Reports_Logic.globalModulesShare.resources import *
from Front.inicio_sesion import UI_Inicio_Sesion
from Reports_Logic.globalModulesShare.mensajes_alertas import Mensajes_Alertas
from Home import PrincipalWindow
import Reports_Logic.globalModulesShare.icono as icono

class InicioSesion(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.ui = UI_Inicio_Sesion()
        self.ui.setupUi(self)
        self.setWindowTitle("Inicio de Sesión")
        self.setWindowIcon(QIcon(":/Source/LOGO_KREI_3.ico"))
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.ui.label_2.setPixmap(QPixmap(":/Source/DevRous2.png"))
        self.ui.label_2.setScaledContents(True)
        self.ui.btn_manejoventana_2.setIcon(QIcon(":Source/Icon_Close.png"))
        self.ui.btn_manejoventana.setIcon(QIcon(":Source/Icon_Minimize.png"))
        self.ui.label.setStyleSheet("font-weight: bold;")
        self.ui.w_login.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=45, xOffset=0, yOffset=0))
        self.__User__ = "KREI"
        self.__Password__ = "RMPG73#"
        self.ui.btn_aceptar_ingreso.clicked.connect(self.Ingresar)
        self.ui.btn_manejoventana_2.clicked.connect(self.cerrar)
        self.ui.btn_manejoventana.clicked.connect(self.minimizar)


    def cerrar(self):
        self.close()

    def minimizar(self):
        self.showMinimized()

    def Aceptar_callback(self):
        pass

    # EVENTOS DEL MOUSE
    def mousePressEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.drag_start_position = event.globalPosition() - QPointF(self.pos())
    
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            if self.drag_start_position is not None:
                new_pos = event.globalPosition() - self.drag_start_position
                self.move(new_pos.toPoint())
    

    def Ingresar(self):
        user = self.ui.txt_usuario.text()
        password = self.ui.txt_usuarioPassword.text()
        if all((user, password)):
            if (user == self.__User__) and (password == self.__Password__):
                self.ventana = PrincipalWindow()
                self.ventana.show()
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana_principal = InicioSesion()
    ventana_principal.show()
    sys.exit(app.exec())