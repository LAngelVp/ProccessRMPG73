#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
# esta clase sera intermediaria entre el front con el back.
from .Logica_Reportes.CreditoKWESTE import *
from .Logica_Reportes.InventarioKWESTE import *
from .Logica_Reportes.BackOrderKWESTE import *
from .Logica_Reportes.SalidasEnValeKWESTE import *
from .Logica_Reportes.CoresKWESTE import *
from .Logica_Reportes.OrdenesServicioKWESTE import *
from .Logica_Reportes.TrabajosPorEstadoKWESTE import *
from .Logica_Reportes.PagosClientesKWESTE import *
from .Logica_Reportes.ComprasKWESTE import *
#-----------------------------------

#CLASE
class KENWORTHdelESTE():
    # este sera el apartado en donde se colocaran las funciones que conectaran al back.
    def CreditoNormalKWESTE(self):
        CreditoNormalKWESTE().Credito_Normal_KWESTE()
    #:------------------------------------------------------
    # INVENTARIO COSTEADO
    def InventarioKWESTE(self):
        InventarioKWESTE().Inventario_Costeado_KWESTE()

    #BACK ORDER REFACCIONES
    def BackOrderKWESTE(self):
        BackOrderKWESTE().BackOrder_KWESTE()

    #SALIDAS EN VALE
    def SalidasenValeKWESTE(self):
        SalidasEnValeKWESTE().SalidasEnVale_KWESTE()

    # SEGUIMIENTO CORES
    def SeguimientoCoresKWESTE(self):
        SeguimientoCoresKWESTE()

    # ORDENES DE SERVICIO
    def OrdenesDeServicioKWESTE(self):
        print (2)
        OrdenesDeServicioKWESTE()

    # TRABAJOS POR ESTADO
    def TrabajosPorEstadoKWESTE(self):
        TrabajosPorEstadoKWESTE()
    
    # PAGOS CLIENTES
    def PagosClientesKWESTE(self):
        PagosClientesKWESTE()

    # COMPRAS DETALLADO
    def ComprasDetallado(self):
        ComprasKWESTE()