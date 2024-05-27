#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios

class SeguimientoCores(Variables):
    def __init__(self):
        super().__init__()
        self.concesionario = Concesionarios().concesionarioEste
        self.variables = Variables()
        self.nombre_doc = 'SCE.xlsx'
        path = os.path.join(self.variables.ruta_Trabajos_kwe,self.nombre_doc)
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)

        df_SeguimientoCores = df.copy()

        columna_FechaFactura = df_SeguimientoCores.pop("FechaFactura")
        df_SeguimientoCores.insert(5, "FechaFactura", columna_FechaFactura)

        columna_FechaRecEnSucProcCores = df_SeguimientoCores.pop("FechaRecEnSucProcCores")
        df_SeguimientoCores.insert(6, "FechaRecEnSucProcCores", columna_FechaRecEnSucProcCores)

        df_SeguimientoCores.insert(7,"Fecha Hoy", self.variables.date_movement_config_document(), allow_duplicates=False)

        for column_name in df_SeguimientoCores.columns:
            if "fecha" in column_name.lower():
                df_SeguimientoCores = self.variables.global_date_format_america(df_SeguimientoCores, column_name)
            else:
                pass

        Antiguedad = df_SeguimientoCores.apply(self.OperacionAntiguedad, axis = 1)

        df_SeguimientoCores.insert(8,"Antigüedad", Antiguedad, allow_duplicates=False)

        df_SeguimientoCores["EstadoFact"] = df_SeguimientoCores.apply(self.EstadoFactura, axis = 1)

        df_SeguimientoCores.drop(["TE","TR","FechaRecEnSuc"], axis = 1)

        for column_name in df_SeguimientoCores.columns:
            if "fecha" in column_name.lower():
                df_SeguimientoCores = self.variables.global_date_format_dmy_mexican(df_SeguimientoCores, column_name)
            else:
                pass

        columnas_bol=df_SeguimientoCores.select_dtypes(include=bool).columns.tolist()
        df_SeguimientoCores[columnas_bol] = df_SeguimientoCores[columnas_bol].astype(str)

        df_SeguimientoCores['Antigüedad'] = pd.to_numeric(df_SeguimientoCores['Antigüedad'].dt.days, downcast='integer')

        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, df_SeguimientoCores, self.concesionario)

    def EstadoFactura(self, row):
        if pd.notna(row["FechaFactura"]):
            return "Facturado"
        else:
            return "Pendiente"

    def OperacionAntiguedad(self, row):
        if pd.notna(row["FechaFactura"]):
            return row["Fecha Hoy"] - row["FechaFactura"]
        else:
            return row["Fecha Hoy"] - row["Fecha"]
