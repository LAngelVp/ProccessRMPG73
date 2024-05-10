#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
class CreditoKWESTEKREI(Variables):
    def __init__(self):
        super().__init__()
        self.concesionario = Concesionarios().concesionarioKREI
        self.variables = Variables()

    def CreditoKWESTE_KREI(self):
        self.nombre_doc = 'CEKREI.xlsx'
        path =  os.path.join(self.variables.ruta_Trabajos_krei, self.nombre_doc)
        # leer el documento.
        df = pd.read_excel(path, sheet_name="Hoja2")
        # obtenemos las columnas que se van a utilizar
        df2 = df[df.columns[0:52]].copy()
        df2 = df2.replace(to_replace = ";", value = "_", regex = True)

        df2.insert(0,"Concesionario","KW ESTE", allow_duplicates=False)

        for i in df2:
            if ("fecha" in i.lower()):
                try:
                    df2[i] = pd.to_datetime(df2[i], errors = "coerce")
                except:
                    pass

        for i in df2:
            if ("fecha" in i.lower()):
                try:
                    df2[i] = df2[i].dt.strftime("%d/%m/%Y")
                except:
                    pass

        # columna del mes actual
        df2["Mes"] = self.variables.nombre_mes_actual_abreviado()
        
        columnas_bol=df2.select_dtypes(include=bool).columns.tolist()
        df2[columnas_bol] = df2[columnas_bol].astype(str)

        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, df2, self.concesionario)


    def CreditoKWSUR_KREI(self):
        self.nombre_doc = 'CSKREI.xlsx'
        path =  os.path.join(self.variables.ruta_Trabajos_krei, self.nombre_doc)
        # leer el documento.
        df = pd.read_excel(path, sheet_name="Hoja2")
        # obtenemos las columnas que se van a utilizar
        df2 = df[df.columns[0:52]].copy()
        df2 = df2.replace(to_replace = ";", value = "_", regex = True)

        df2.insert(0,"Concesionario","KW SUR", allow_duplicates=False)
        
        for i in df2:
            if ("fecha" in i.lower()):
                try:
                    df2[i] = pd.to_datetime(df2[i], errors = "coerce")
                except:
                    pass

        for i in df2:
            if ("fecha" in i.lower()):
                try:
                    df2[i] = df2[i].dt.strftime("%d/%m/%Y")
                except:
                    pass
        
        # columna del mes actual
        df2["Mes"] = self.variables.nombre_mes_actual_abreviado()

        columnas_bol=df2.select_dtypes(include=bool).columns.tolist()
        df2[columnas_bol] = df2[columnas_bol].astype(str)

        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, df2, self.concesionario)