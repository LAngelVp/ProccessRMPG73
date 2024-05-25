#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from datetime import *
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
class InventarioUnidades():
    def __init__(self):
        super().__init__()
        self.concesionario = Concesionarios().concesionarioEste
        self.variables = Variables()
        self.nombre_doc = 'IUE.xlsx'
        path = os.path.join(self.variables.ruta_Trabajos_kwe,self.nombre_doc)
        df = pd.read_excel(path, sheet_name="Hoja2")
        df1 = df.copy()
        df1.columns = df1.columns.str.replace(" ", "_")
        df1.drop(["Serie_Motor","Int._Diario","Fecha_Vencimiento","Importe_Inventario_Moneda_Local","Moneda_Artículo","Fact._Compra_TipoCambio","Fact._Compra_Moneda"], axis=1, inplace=True)
        df1.insert(
            loc = 5,
            column = "Año Modelo",
            value = "AM"+df1["Año_Modelo"].map(str),
            allow_duplicates = True
        )
        col_serie = "S-" + df1["Serie"].map(str)
        df1["Serie"] = col_serie
        
        df1["TipoInv"] = df1["Tipo_Docto."].apply(lambda x:self.ClasificacionTipoInv(x))
        for column_name in df1.columns:
                if "f." in column_name.lower():
                    df1 = self.variables.global_date_format_america(df1, column_name)
                    df1 = self.variables.global_date_format_dmy_mexican(df1, column_name)
                else:
                    pass

        df1.drop(["Año_Modelo"], axis=1, inplace=True)
        columnas_bol=df1.select_dtypes(include=bool).columns.tolist()
        df1[columnas_bol] = df1[columnas_bol].astype(str)
        df1.columns = df1.columns.str.replace("_", " ")
        
        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, df1, self.concesionario)
    
    def ClasificacionTipoInv(self, valor):
            if (valor == "Factura"):
                return "Propia"
            else:
                return "Consigna"