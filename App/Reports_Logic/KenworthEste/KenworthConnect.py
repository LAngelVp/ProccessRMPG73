#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
# esta clase sera intermediaria entre el front con el back.
from .Logica_Reportes.Credito import *
from .Logica_Reportes.Inventario import *
from .Logica_Reportes.BackOrders import *
from .Logica_Reportes.SalidasEnVale import *
from .Logica_Reportes.SeguimientoCores import *
from .Logica_Reportes.OrdenesDeServicio import *
from .Logica_Reportes.TrabajosPorEstado import *
from .Logica_Reportes.PagoClientes import *
from .Logica_Reportes.Compras import *
from .Logica_Reportes.InventarioUnidades import *
from .Logica_Reportes.ServicioDetallado import *
from .Logica_Reportes.Refacciones import *
from .Logica_Reportes.Financiero import *
#-----------------------------------

#CLASE
class KenworthConnect():
    # este sera el apartado en donde se colocaran las funciones que conectaran al back.
    def Credito(self):
        Credito()
    #:------------------------------------------------------
    # INVENTARIO COSTEADO
    def Inventario(self):
        Inventario()

    #BACK ORDER REFACCIONES
    def BackOrders(self):
        BackOrders()

    #SALIDAS EN VALE
    def SalidasEnVale(self):
        SalidasEnVale()

    # SEGUIMIENTO CORES
    def SeguimientoCores(self):
        SeguimientoCores()

    # ORDENES DE SERVICIO
    def OrdenesDeServicio(self):
        OrdenesDeServicio()

    # TRABAJOS POR ESTADO
    def TrabajosPorEstado(self):
        TrabajosPorEstado()
    
    # PAGOS CLIENTES
    def PagoClientes(self):
        PagoClientes()

    # COMPRAS DETALLADO
    def Compras(self):
        Compras()

    # INVENTARIO DE UNIDADES
    def InventarioUnidades(self):
        InventarioUnidades()
    
    # SERVICIO DETALLADO
    def ServicioDetallado(self):
        ServicioDetallado()
    
    # REFACCIONES
    def Refacciones(self):
        Refacciones()
    
    # RESULTADOS FINANCIEROS
    def ResultadosFinancieros(self):
        ResultadosFinancieros()
        