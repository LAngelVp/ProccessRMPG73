#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from .Variables.ContenedorVariables import Variables
class CreditoKWESTEKREI(Variables):
    def CreditoKWESTE_KREI(self):
        path =  os.path.join(Variables().ruta_Trabajo,'CEKREI.xlsx')
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
        df2["Mes"] = Variables().nombre_mes_actual_abreviado()
        
        columnas_bol=df2.select_dtypes(include=bool).columns.tolist()
        df2[columnas_bol] = df2[columnas_bol].astype(str)

        # exportamos el documento
        df2.to_excel(os.path.join(Variables().ruta_procesados,f'KREI_Credito_KWESTE_RMPG_{Variables().FechaExternsionGuardar()}.xlsx'), index=False)


    def CreditoKWSUR_KREI(self):
        path =  os.path.join(Variables().ruta_Trabajo,'CSKREI.xlsx')
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
        df2["Mes"] = Variables().nombre_mes_actual_abreviado()

        columnas_bol=df2.select_dtypes(include=bool).columns.tolist()
        df2[columnas_bol] = df2[columnas_bol].astype(str)

        # exportamos el documento
        df2.to_excel(os.path.join(Variables().ruta_procesados,f'KREI_Credito_KWSUR_RMPG_{Variables().FechaExternsionGuardar()}.xlsx'), index=False)