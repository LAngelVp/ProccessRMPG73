#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
# esta clase sera intermediaria entre el front con el back.
import traceback
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
from .Logica_Reportes.Contabilidad import FactSitic_document, Nota_credito_retenido, FactSat_document
from .Logica_Reportes.VentasPerdidas import VentasPerdidas
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
        
    # COMPRAS DETALLADO FACTSITIC
    def ComprasDetalladoFactSitic(self):
        FactSitic_document().compras_detallado
    # NOTAS DE CARGO PROVEEDOR FACTSITIC
    def NotasCargoProveedor(self):
        FactSitic_document().notas_cargo_proveedor
    
    # NCR FACTSITIC
    def NcrFactSitic(self):
        Nota_credito_retenido().Ncr
    
    # FACTURAS FACTSAT
    def FacturasFactSat(self):
        FactSat_document().Facturas
    
    # NOTA DE CREDITO FACTSAT
    def NotaCreditoFactSat(self):
        FactSat_document().Nota_de_credito
        
    def VentasPerdidasMatriz(self):
        try:
            VentasPerdidas().venta_perdida_matriz()
        except Exception as e:
            print(f"Error: {e}")
    def VentasPerdidasTrebol(self):
        try:
            VentasPerdidas().venta_perdida_trebol()
        except Exception as e:
            print(f"Error: {e}")
    def VentasPerdidasVeracruz(self):
        try:
            VentasPerdidas().venta_perdida_veracruz()
        except Exception as e:
            print(f"Error: {e}")
    def VentasPerdidasOrizaba(self):
        try:
            VentasPerdidas().venta_perdida_orizaba()
        except Exception as e:
            print(f"Error: {e}")
    def VentasPerdidasTehuacan(self):
        try:
            VentasPerdidas().venta_perdida_tehuacan()
        except Exception as e:
            print(f"Error: {e}")
    def VentasPerdidasVillahermosa(self):
        try:
            VentasPerdidas().venta_perdida_villahermosa()
        except Exception as e:
            print(f"Error: {e}")
    def VentasPerdidasCoatzacoalcos(self):
        try:
            VentasPerdidas().venta_perdida_coatzacoalcos()
        except Exception as e:
            print(f"Error: {e}")
    def VentasPerdidasMerida(self):
        try:
            VentasPerdidas().venta_perdida_merida()
        except Exception as e:
            print(f"Error: {e}")
    def VentasPerdidasOaxaca(self):
        try:
            VentasPerdidas().venta_perdida_oaxaca()
        except Exception as e:
            print(f"Error: {e}")
    def VentasPerdidasTuxtla1(self):
        try:
            VentasPerdidas().venta_perdida_tuxtla1()
        except Exception as e:
            print(f"Error: {e}")
    def VentasPerdidasTuxtla2(self):
        try:
            VentasPerdidas().venta_perdida_tuxtla2()
        except Exception as e:
            print(f"Error: {e}")
    