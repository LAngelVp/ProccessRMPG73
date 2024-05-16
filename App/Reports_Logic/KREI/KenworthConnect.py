#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
# APARTADO DE KREI
from .Logica_Reportes.KREI_OrdenesKW import *
from .Logica_Reportes.KREI_CreditoKW import *
from .Logica_Reportes.KREI_InventarioKW import *
from .Logica_Reportes.KREI_Refacciones import *
from .Logica_Reportes.KREI_ServicioDetallado import *
from .Logica_Reportes.KREI_ResultadosFinancieros import *
#-------------------------------------------
#CLASE
class KenworthConnect():
#------------------------------------------------------
# APARTADO DE KREI---------------------------------------
#-----------------
#ORDENES DE SERVICIO
    def OrdenesServicioKREIKWESTE(self):
        OrdenesServicioKWESTEKREI().OrdenesKWESTE_KREI()
    
    def OrdenesServicioKREIKWSUR(self):
        OrdenesServicioKWESTEKREI().OrdenesKWSUR_KREI()
#CREDITO
    def CreditoKREIKWSUR(self):
        CreditoKWESTEKREI().CreditoKWSUR_KREI()
    
    def CreditoKREIKWESTE(self):
        CreditoKWESTEKREI().CreditoKWESTE_KREI()
#INVENTARIO
    def InventarioKREIKWSUR(self):
        InventarioKWESTEKREI().InventarioKWSUR_KREI()
    
    def InventarioKREIKWESTE(self):
        InventarioKWESTEKREI().InventarioKWESTE_KREI()
#REFACCIONES
    def RefaccionesKREIKWSUR(self):
        RefaccionesKWESTEKREI().RefaccionesKWSUR_KREI()
    
    def RefaccionesKREIKWESTE(self):
        RefaccionesKWESTEKREI().RefaccionesKWESTE_KREI()
#SERVICIO DETALLADO
    def ServicioDetalladoKREIKWSUR(self):
        ServicioDetalladoKWESTEKREI().ServicioDetalladoKWSUR_KREI()
    
    def ServicioDetalladoKREIKWESTE(self):
        ServicioDetalladoKWESTEKREI().ServicioDetalladoKWESTE_KREI()

# RESULTADOS FINANCIEROS

    def ResultadosFinancierosEsteKREI(self):
        ResultadosFinancierosKREI().ReporteFinancieroKWESTE_KREI()
    
    def ResultadosFinancierosSurKREI(self):
        ResultadosFinancierosKREI().ReporteFinancieroKWSUR_KREI()