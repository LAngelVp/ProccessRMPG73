# Form implementation generated from reading ui file 'c:\Users\Angel Rodriguez\LUIS_ANGEL_VALLEJO\ProccessRMPG73\App\Front\ventanasui\V_KREI.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Kenworth_KREI(object):
    def setupUi(self, Kenworth_KREI):
        Kenworth_KREI.setObjectName("Kenworth_KREI")
        Kenworth_KREI.resize(800, 520)
        Kenworth_KREI.setMinimumSize(QtCore.QSize(800, 520))
        Kenworth_KREI.setMaximumSize(QtCore.QSize(800, 520))
        Kenworth_KREI.setStyleSheet("#Kenworth_KREI{\n"
"min-width: 800px;\n"
"min-height:520px;\n"
"max-width: 800px;\n"
"max-height:520px;\n"
"}\n"
"#WPrincipal{\n"
"background-color: rgb(234, 234, 234);\n"
"}\n"
"[objectName^=\"btc_btc\"]{\n"
"background-color: transparent;\n"
"border-radius:none;\n"
"width:35px;\n"
"height:35px;\n"
"}\n"
"[objectName^=\"btc_btc\"]:hover{\n"
"background-color: rgb(64, 150, 216);\n"
"    color: rgb(0, 0, 0);\n"
"    border-radius:4px;\n"
"}\n"
"[objectName^=\"Tabla\"]{\n"
"    background-color: rgb(255, 255, 255);\n"
"    border: 1px solid;\n"
"}\n"
"[objectName^=\"txt\"]{\n"
"    font-family: Arial;\n"
"    color: rgb(0, 0, 0);\n"
"    font-size: 20px;\n"
"}\n"
"[objectName^=\"btn_btn\"]{\n"
"background-color: rgb(64, 150, 216);\n"
"    border-radius:4px;\n"
"    color: rgb(0, 0, 0);\n"
"    height:35px;\n"
"}\n"
"[objectName^=\"btn_btn\"]:hover{\n"
"background-color: rgb(69, 163, 235);\n"
"}\n"
"#menuBar{\n"
"background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);\n"
"border-top-left-radius: 10px;\n"
"border-top-right-radius: 10px;\n"
"}")
        self.WPrincipal = QtWidgets.QWidget(parent=Kenworth_KREI)
        self.WPrincipal.setMinimumSize(QtCore.QSize(800, 500))
        self.WPrincipal.setMaximumSize(QtCore.QSize(800, 500))
        self.WPrincipal.setStyleSheet("")
        self.WPrincipal.setObjectName("WPrincipal")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.WPrincipal)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.WCabecera = QtWidgets.QWidget(parent=self.WPrincipal)
        self.WCabecera.setMinimumSize(QtCore.QSize(0, 50))
        self.WCabecera.setMaximumSize(QtCore.QSize(16777215, 50))
        self.WCabecera.setObjectName("WCabecera")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.WCabecera)
        self.horizontalLayout.setContentsMargins(5, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.WLogo = QtWidgets.QWidget(parent=self.WCabecera)
        self.WLogo.setMinimumSize(QtCore.QSize(200, 0))
        self.WLogo.setMaximumSize(QtCore.QSize(200, 16777215))
        self.WLogo.setObjectName("WLogo")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.WLogo)
        self.verticalLayout_9.setContentsMargins(0, 5, 0, 5)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.lblLogoKWKREI = QtWidgets.QLabel(parent=self.WLogo)
        self.lblLogoKWKREI.setText("")
        self.lblLogoKWKREI.setPixmap(QtGui.QPixmap("c:\\Users\\Angel Rodriguez\\LUIS_ANGEL_VALLEJO\\ProccessRMPG73\\App\\Front\\ventanasui\\../Source/LOGOKREI.png"))
        self.lblLogoKWKREI.setScaledContents(True)
        self.lblLogoKWKREI.setObjectName("lblLogoKWKREI")
        self.verticalLayout_9.addWidget(self.lblLogoKWKREI)
        self.horizontalLayout.addWidget(self.WLogo)
        spacerItem = QtWidgets.QSpacerItem(476, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.WBotonesSalida = QtWidgets.QWidget(parent=self.WCabecera)
        self.WBotonesSalida.setMinimumSize(QtCore.QSize(75, 0))
        self.WBotonesSalida.setMaximumSize(QtCore.QSize(75, 16777215))
        self.WBotonesSalida.setObjectName("WBotonesSalida")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.WBotonesSalida)
        self.horizontalLayout_10.setContentsMargins(-1, -1, 5, -1)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.btc_btc_Minimizar = QtWidgets.QPushButton(parent=self.WBotonesSalida)
        self.btc_btc_Minimizar.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btc_btc_Minimizar.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("c:\\Users\\Angel Rodriguez\\LUIS_ANGEL_VALLEJO\\ProccessRMPG73\\App\\Front\\ventanasui\\../Source/Icon_Minimize.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btc_btc_Minimizar.setIcon(icon)
        self.btc_btc_Minimizar.setIconSize(QtCore.QSize(30, 30))
        self.btc_btc_Minimizar.setObjectName("btc_btc_Minimizar")
        self.horizontalLayout_10.addWidget(self.btc_btc_Minimizar)
        self.btc_btc_Cerrar = QtWidgets.QPushButton(parent=self.WBotonesSalida)
        self.btc_btc_Cerrar.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btc_btc_Cerrar.setMouseTracking(True)
        self.btc_btc_Cerrar.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("c:\\Users\\Angel Rodriguez\\LUIS_ANGEL_VALLEJO\\ProccessRMPG73\\App\\Front\\ventanasui\\../Source/Icon_Close.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btc_btc_Cerrar.setIcon(icon1)
        self.btc_btc_Cerrar.setIconSize(QtCore.QSize(30, 30))
        self.btc_btc_Cerrar.setObjectName("btc_btc_Cerrar")
        self.horizontalLayout_10.addWidget(self.btc_btc_Cerrar)
        self.horizontalLayout.addWidget(self.WBotonesSalida)
        self.verticalLayout_10.addWidget(self.WCabecera)
        self.WCuerpo = QtWidgets.QWidget(parent=self.WPrincipal)
        self.WCuerpo.setMinimumSize(QtCore.QSize(0, 280))
        self.WCuerpo.setMaximumSize(QtCore.QSize(16777215, 280))
        self.WCuerpo.setObjectName("WCuerpo")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.WCuerpo)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.WTablaIzquierda = QtWidgets.QWidget(parent=self.WCuerpo)
        self.WTablaIzquierda.setObjectName("WTablaIzquierda")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.WTablaIzquierda)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.txt_Cola = QtWidgets.QLabel(parent=self.WTablaIzquierda)
        self.txt_Cola.setMinimumSize(QtCore.QSize(0, 20))
        self.txt_Cola.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(-1)
        self.txt_Cola.setFont(font)
        self.txt_Cola.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.txt_Cola.setObjectName("txt_Cola")
        self.verticalLayout_4.addWidget(self.txt_Cola)
        self.Tabla_Cola = QtWidgets.QTableWidget(parent=self.WTablaIzquierda)
        self.Tabla_Cola.setObjectName("Tabla_Cola")
        self.Tabla_Cola.setColumnCount(0)
        self.Tabla_Cola.setRowCount(0)
        self.verticalLayout_4.addWidget(self.Tabla_Cola)
        self.horizontalLayout_6.addWidget(self.WTablaIzquierda)
        self.WTablaDerecha = QtWidgets.QWidget(parent=self.WCuerpo)
        self.WTablaDerecha.setObjectName("WTablaDerecha")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.WTablaDerecha)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.txt_Procesado = QtWidgets.QLabel(parent=self.WTablaDerecha)
        self.txt_Procesado.setMinimumSize(QtCore.QSize(0, 20))
        self.txt_Procesado.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(-1)
        self.txt_Procesado.setFont(font)
        self.txt_Procesado.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.txt_Procesado.setObjectName("txt_Procesado")
        self.verticalLayout_5.addWidget(self.txt_Procesado)
        self.Tabla_Procesado = QtWidgets.QTableWidget(parent=self.WTablaDerecha)
        self.Tabla_Procesado.setObjectName("Tabla_Procesado")
        self.Tabla_Procesado.setColumnCount(0)
        self.Tabla_Procesado.setRowCount(0)
        self.verticalLayout_5.addWidget(self.Tabla_Procesado)
        self.horizontalLayout_6.addWidget(self.WTablaDerecha)
        self.verticalLayout_10.addWidget(self.WCuerpo)
        self.WPie = QtWidgets.QWidget(parent=self.WPrincipal)
        self.WPie.setMinimumSize(QtCore.QSize(0, 100))
        self.WPie.setMaximumSize(QtCore.QSize(16777215, 100))
        self.WPie.setObjectName("WPie")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.WPie)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.WBotones = QtWidgets.QWidget(parent=self.WPie)
        self.WBotones.setMinimumSize(QtCore.QSize(450, 0))
        self.WBotones.setObjectName("WBotones")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.WBotones)
        self.verticalLayout_6.setContentsMargins(10, 0, 0, 0)
        self.verticalLayout_6.setSpacing(5)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.WBotonesTrabajo = QtWidgets.QWidget(parent=self.WBotones)
        self.WBotonesTrabajo.setMinimumSize(QtCore.QSize(0, 50))
        self.WBotonesTrabajo.setMaximumSize(QtCore.QSize(16777215, 50))
        self.WBotonesTrabajo.setObjectName("WBotonesTrabajo")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.WBotonesTrabajo)
        self.horizontalLayout_8.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_8.setSpacing(5)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.btn_btn_Subir = QtWidgets.QPushButton(parent=self.WBotonesTrabajo)
        font = QtGui.QFont()
        font.setFamily("Cambria Math")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btn_btn_Subir.setFont(font)
        self.btn_btn_Subir.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_btn_Subir.setStyleSheet("")
        self.btn_btn_Subir.setObjectName("btn_btn_Subir")
        self.horizontalLayout_8.addWidget(self.btn_btn_Subir)
        self.btn_btn_Eliminar = QtWidgets.QPushButton(parent=self.WBotonesTrabajo)
        font = QtGui.QFont()
        font.setFamily("Cambria Math")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btn_btn_Eliminar.setFont(font)
        self.btn_btn_Eliminar.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_btn_Eliminar.setStyleSheet("")
        self.btn_btn_Eliminar.setObjectName("btn_btn_Eliminar")
        self.horizontalLayout_8.addWidget(self.btn_btn_Eliminar)
        self.btn_btn_Comenzar = QtWidgets.QPushButton(parent=self.WBotonesTrabajo)
        font = QtGui.QFont()
        font.setFamily("Cambria Math")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btn_btn_Comenzar.setFont(font)
        self.btn_btn_Comenzar.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_btn_Comenzar.setStyleSheet("")
        self.btn_btn_Comenzar.setObjectName("btn_btn_Comenzar")
        self.horizontalLayout_8.addWidget(self.btn_btn_Comenzar)
        self.verticalLayout_6.addWidget(self.WBotonesTrabajo)
        self.WBotonesRutas = QtWidgets.QWidget(parent=self.WBotones)
        self.WBotonesRutas.setObjectName("WBotonesRutas")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.WBotonesRutas)
        self.horizontalLayout_9.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_9.setSpacing(5)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.btn_btn_Procesados = QtWidgets.QPushButton(parent=self.WBotonesRutas)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.btn_btn_Procesados.setFont(font)
        self.btn_btn_Procesados.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_btn_Procesados.setStyleSheet("")
        self.btn_btn_Procesados.setObjectName("btn_btn_Procesados")
        self.horizontalLayout_9.addWidget(self.btn_btn_Procesados)
        self.btn_btn_Originales = QtWidgets.QPushButton(parent=self.WBotonesRutas)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_btn_Originales.setFont(font)
        self.btn_btn_Originales.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_btn_Originales.setStyleSheet("")
        self.btn_btn_Originales.setObjectName("btn_btn_Originales")
        self.horizontalLayout_9.addWidget(self.btn_btn_Originales)
        self.btn_btn_Errores = QtWidgets.QPushButton(parent=self.WBotonesRutas)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_btn_Errores.setFont(font)
        self.btn_btn_Errores.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_btn_Errores.setStyleSheet("")
        self.btn_btn_Errores.setObjectName("btn_btn_Errores")
        self.horizontalLayout_9.addWidget(self.btn_btn_Errores)
        self.verticalLayout_6.addWidget(self.WBotonesRutas)
        self.horizontalLayout_7.addWidget(self.WBotones)
        self.WTextoProceso = QtWidgets.QWidget(parent=self.WPie)
        self.WTextoProceso.setObjectName("WTextoProceso")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.WTextoProceso)
        self.verticalLayout_7.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_7.setSpacing(5)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.lbl_TrabajandoCon = QtWidgets.QLabel(parent=self.WTextoProceso)
        self.lbl_TrabajandoCon.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_TrabajandoCon.setFont(font)
        self.lbl_TrabajandoCon.setText("")
        self.lbl_TrabajandoCon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lbl_TrabajandoCon.setObjectName("lbl_TrabajandoCon")
        self.verticalLayout_7.addWidget(self.lbl_TrabajandoCon)
        self.lbl_NombreReporte = QtWidgets.QLabel(parent=self.WTextoProceso)
        self.lbl_NombreReporte.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_NombreReporte.setFont(font)
        self.lbl_NombreReporte.setText("")
        self.lbl_NombreReporte.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lbl_NombreReporte.setObjectName("lbl_NombreReporte")
        self.verticalLayout_7.addWidget(self.lbl_NombreReporte)
        self.horizontalLayout_7.addWidget(self.WTextoProceso)
        self.WBotonAyuda = QtWidgets.QWidget(parent=self.WPie)
        self.WBotonAyuda.setMinimumSize(QtCore.QSize(60, 0))
        self.WBotonAyuda.setMaximumSize(QtCore.QSize(60, 60))
        self.WBotonAyuda.setObjectName("WBotonAyuda")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.WBotonAyuda)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.btn_btn_Ayuda = QtWidgets.QPushButton(parent=self.WBotonAyuda)
        self.btn_btn_Ayuda.setMaximumSize(QtCore.QSize(16777213, 16777215))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_btn_Ayuda.setFont(font)
        self.btn_btn_Ayuda.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.btn_btn_Ayuda.setAcceptDrops(False)
        self.btn_btn_Ayuda.setToolTip("<html><head/><body><p align=\"justify\">Ayuda</p></body></html>")
        self.btn_btn_Ayuda.setToolTipDuration(0)
        self.btn_btn_Ayuda.setStatusTip("")
        self.btn_btn_Ayuda.setWhatsThis("")
        self.btn_btn_Ayuda.setAccessibleName("")
        self.btn_btn_Ayuda.setAccessibleDescription("")
        self.btn_btn_Ayuda.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.btn_btn_Ayuda.setAutoFillBackground(False)
        self.btn_btn_Ayuda.setStyleSheet("")
        self.btn_btn_Ayuda.setLocale(QtCore.QLocale(QtCore.QLocale.Language.Spanish, QtCore.QLocale.Country.Nicaragua))
        self.btn_btn_Ayuda.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("c:\\Users\\Angel Rodriguez\\LUIS_ANGEL_VALLEJO\\ProccessRMPG73\\App\\Front\\ventanasui\\../Source/Icon_Help.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btn_btn_Ayuda.setIcon(icon2)
        self.btn_btn_Ayuda.setIconSize(QtCore.QSize(32, 32))
        self.btn_btn_Ayuda.setObjectName("btn_btn_Ayuda")
        self.verticalLayout_8.addWidget(self.btn_btn_Ayuda)
        self.horizontalLayout_7.addWidget(self.WBotonAyuda)
        self.verticalLayout_10.addWidget(self.WPie)
        Kenworth_KREI.setCentralWidget(self.WPrincipal)
        self.menuBar = QtWidgets.QMenuBar(parent=Kenworth_KREI)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.menuBar.setFont(font)
        self.menuBar.setObjectName("menuBar")
        self.menuOPCIONES = QtWidgets.QMenu(parent=self.menuBar)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.menuOPCIONES.setFont(font)
        self.menuOPCIONES.setObjectName("menuOPCIONES")
        Kenworth_KREI.setMenuBar(self.menuBar)
        self.actionFechaMovimiento = QtGui.QAction(parent=Kenworth_KREI)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.actionFechaMovimiento.setFont(font)
        self.actionFechaMovimiento.setObjectName("actionFechaMovimiento")
        self.menuOPCIONES.addAction(self.actionFechaMovimiento)
        self.menuBar.addAction(self.menuOPCIONES.menuAction())

        self.retranslateUi(Kenworth_KREI)
        QtCore.QMetaObject.connectSlotsByName(Kenworth_KREI)

    def retranslateUi(self, Kenworth_KREI):
        _translate = QtCore.QCoreApplication.translate
        Kenworth_KREI.setWindowTitle(_translate("Kenworth_KREI", "KENWORTH KREI"))
        self.btc_btc_Minimizar.setToolTip(_translate("Kenworth_KREI", "Minimizar"))
        self.btc_btc_Cerrar.setToolTip(_translate("Kenworth_KREI", "Cerrar"))
        self.txt_Cola.setText(_translate("Kenworth_KREI", "Trabajos En Espera"))
        self.txt_Procesado.setText(_translate("Kenworth_KREI", "Trabajos Realizados"))
        self.btn_btn_Subir.setToolTip(_translate("Kenworth_KREI", "<html><head/><body><p>Selecciona un archivo .xlsx</p></body></html>"))
        self.btn_btn_Subir.setText(_translate("Kenworth_KREI", "Subir"))
        self.btn_btn_Eliminar.setToolTip(_translate("Kenworth_KREI", "<html><head/><body><p>Elimina los archivos procesados</p></body></html>"))
        self.btn_btn_Eliminar.setText(_translate("Kenworth_KREI", "Eliminar"))
        self.btn_btn_Comenzar.setToolTip(_translate("Kenworth_KREI", "<html><head/><body><p>Comenzar el proceso</p></body></html>"))
        self.btn_btn_Comenzar.setText(_translate("Kenworth_KREI", "Comenzar"))
        self.btn_btn_Procesados.setToolTip(_translate("Kenworth_KREI", "<html><head/><body><p>Ruta de archivos procesados</p></body></html>"))
        self.btn_btn_Procesados.setText(_translate("Kenworth_KREI", "Procesados"))
        self.btn_btn_Originales.setToolTip(_translate("Kenworth_KREI", "<html><head/><body><p>Ruta de archivos originales</p></body></html>"))
        self.btn_btn_Originales.setText(_translate("Kenworth_KREI", "Originales"))
        self.btn_btn_Errores.setToolTip(_translate("Kenworth_KREI", "<html><head/><body><p>Ruta de archivos erroneos</p></body></html>"))
        self.btn_btn_Errores.setText(_translate("Kenworth_KREI", "Erroneos"))
        self.menuOPCIONES.setTitle(_translate("Kenworth_KREI", "OPCIONES"))
        self.actionFechaMovimiento.setText(_translate("Kenworth_KREI", "FechaMovimiento"))
