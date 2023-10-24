#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
#--------------------
# CLASE INTERMEDIARIA ENTRE EL FRONT Y EL BACK PANDAS
#---------------------
import sys
import os
import shutil
#ANCHOR KENWORTH RIO BRAVO
from .Logica_Reportes.Back_Order import BackOrder
from .Logica_Reportes.Compras import Compras
from .Logica_Reportes.Credito import Credito
from .Logica_Reportes.Ordenes_Servicio import OrdenesServicio
from .Logica_Reportes.PagosClientes import PagosClientes
from .Logica_Reportes.Refacciones import Refacciones
from .Logica_Reportes.Salidas_Vale import SalidasVale
from .Logica_Reportes.Servicio_Detallado import ServioDetallado
from .Logica_Reportes.Trabajos_Por_Estado import TrabajosPorEstado
from .Logica_Reportes.InventarioCosteado import InventarioCosteado
from .Logica_Reportes.InventarioUnidades import InventarioUnidades
from .Logica_Reportes.Financiero import ResultadosFinancieros
#___________________________________________________

class KenworthConnect():
#--------------------------------
# SALIDAS EN VALE
    def SalidasEnVale(self):
        SalidasVale()
#---------------------------------
# FACTURA DE VENTA DE REFACCIONES
    def Refacciones(self):
        Refacciones()
#---------------------------------
# ORDENES DE SERVICIO
    def OrdenesDeServicio(self):
        OrdenesServicio()
#---------------------------------
# SERVICIO DETALLADO
    def ServicioDetallado(self):
        ServioDetallado()
#---------------------------------
# BACK ORDER DE REFACCIONES
    def BackOrder(self):
        BackOrder()
#--------------------------------
# COMPRAS DETALLADO
    def ComprasDetallado(self):
        Compras()
#--------------------------------
# CREDITO
    def Credito(self):
        Credito()
#--------------------------------
# TRABAJOS POR ESTADO
    def TrabajosPorEstado(self):
        TrabajosPorEstado()
#----------------------------------
# PAGO DE FACTURAS CLIENTES
    def PagosClientes(self):
        PagosClientes()
#----------------------------------
# INVENTARIO COSTEADO
    def InventarioCosteado(self):
        InventarioCosteado()
#---------------------------------
# INVENTARIO UNIDADES
    def InventarioDeUnidades(self):
        InventarioUnidades()
#----------------------------------
# RESULTADOS FINANCIEROS
    def ResultadosFinancieros(self):
        ResultadosFinancieros()