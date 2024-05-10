#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
class InventarioKWESTEKREI(Variables):

    def __init__(self):
        super().__init__()
        self.concesionario = Concesionarios().concesionarioKREI
        self.variables = Variables()

    def InventarioKWESTE_KREI(self):
        #obtenemos el archivo
        self.nombre_doc = 'ICEKREI.xlsx'
        path = os.path.join(self.variables.ruta_Trabajos_krei,self.nombre_doc)
        #leer el documento con pandas
        df = pd.read_excel(path, sheet_name="Hoja2")
        #reemplazar el ";" de los registros que lo contengan por un "-"
        df = df.replace(to_replace=";", value="-", regex=True)
        #obtener solo las celdas que vamos a trabajar.
        df2 = df[df.columns[0:33]].copy()

        df2.insert(0,"Concesionario","KW ESTE", allow_duplicates=False)

        for column_title in df2:
            if ("Fecha" in column_title):
                try:
                    df2[column_title] = pd.to_datetime(df2[column_title], errors="coerce")
                except:
                    pass
            else:
                pass
        #cambiamos el formato de la columna de la "Fecha Entrada".
        for i in df2:
            try:
                if ("Fecha" in i):
                    df2[i] = df2[i].dt.strftime("%d/%m/%Y")                    
                else:
                    pass
            except:
                pass

        # columna del mes actual
        df2["Mes"] = self.variables.nombre_mes_actual_abreviado()

        columnas_bol=df2.select_dtypes(include=bool).columns.tolist()
        df2[columnas_bol] = df2[columnas_bol].astype(str)

        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, df2, self.concesionario)
    
    def InventarioKWSUR_KREI(self):
        #obtenemos el archivo
        path = os.path.join(self.variables.ruta_Trabajos_krei,'ICSKREI.xlsx')
        #leer el documento con pandas
        df = pd.read_excel(path, sheet_name="Hoja2")
        #reemplazar el ";" de los registros que lo contengan por un "-"
        df = df.replace(to_replace=";", value="-", regex=True)
        #obtener solo las celdas que vamos a trabajar.
        df2 = df[df.columns[0:33]].copy()

        df2.insert(0,"Concesionario","KW SUR", allow_duplicates=False)

        for column_title in df2:
            if ("Fecha" in column_title):
                try:
                    df2[column_title] = pd.to_datetime(df2[column_title], errors="coerce")
                except:
                    pass
            else:
                pass
        #cambiamos el formato de la columna de la "Fecha Entrada".
        for i in df2:
            try:
                if ("Fecha" in i):
                    df2[i] = df2[i].dt.strftime("%d/%m/%Y")                    
                else:
                    pass
            except:
                pass
            
        # columna del mes actual
        df2["Mes"] = self.variables.nombre_mes_actual_abreviado()

        columnas_bol=df2.select_dtypes(include=bool).columns.tolist()
        df2[columnas_bol] = df2[columnas_bol].astype(str)

        # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
        self.variables.guardar_datos_dataframe(self.nombre_doc, df2, self.concesionario)