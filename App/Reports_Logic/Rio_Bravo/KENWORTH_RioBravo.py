#########################
# DESARROLLADOR
# LUIS ANGEL VALLEJO PEREZ
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

class KENWORTH_Rio_Bravo():
#--------------------------------
# SALIDAS EN VALE
    def SalidasEnVale_KWRB(self):
        SalidasVale().SalidasKWRB()
#---------------------------------
# FACTURA DE VENTA DE REFACCIONES
    def Refacciones_KWRB(self):
        Refacciones().RefaccionesKWRB()
#---------------------------------
# ORDENES DE SERVICIO
    def OrdenesServicio_KWRB(self):
        OrdenesServicio().OrdenesServicioKWRB()
#---------------------------------
# SERVICIO DETALLADO
    def ServicioDetallado_KWRB(self):
        ServioDetallado().ServioDetalladoKWRB()
#---------------------------------
# BACK ORDER DE REFACCIONES
    def BackOrder_KWRB(self):
        BackOrder().Back_Order_KWRB()
#--------------------------------
# COMPRAS DETALLADO
    def ComprasDetallado_KWRB(self):
        Compras().Compras_Detallado_KWRB()
#--------------------------------
# CREDITO
    def Credito_KWRB(self):
        Credito().Credito_Normal_KWRB()
#--------------------------------
# TRABAJOS POR ESTADO
    def TrabajosPorEstado_KWRB(self):
        TrabajosPorEstado().Trabajos_Por_Estado_KWRB()
#----------------------------------
# PAGO DE FACTURAS CLIENTES
    def PagosClientes_KWRB(self):
        PagosClientes().Pagos_Clientes_KWRB()
#----------------------------------
# INVENTARIO COSTEADO
    def InventarioCosteado_KWRB(self):
        InventarioCosteado().Inventario_Costeado_KWRB()
#---------------------------------
# INVENTARIO UNIDADES
    def InventarioUnidades_KWRB(self):
        InventarioUnidades().InvUnidades_KWRB()
#----------------------------------
# RESULTADOS FINANCIEROS
    def ResultadosFinancieros_KWRB(self):
        ResultadosFinancieros().ResultadosFinancieroKWRB()