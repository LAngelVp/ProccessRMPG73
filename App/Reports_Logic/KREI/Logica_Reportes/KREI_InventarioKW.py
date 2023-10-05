#########################
# DESARROLLADOR
# LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from .Variables.ContenedorVariables import Variables
class InventarioKWESTEKREI(Variables):
    def InventarioKWESTE_KREI(self):
        #obtenemos el archivo
        path = os.path.join(Variables().ruta_Trabajo,'ICEKREI.xlsx')
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

        df2.to_excel(os.path.join(Variables().ruta_procesados,f'InvCost_KWESTE_KREI_SDR_{Variables().FechaExternsionGuardar()}.xlsx'), index=False)
    
    def InventarioKWSUR_KREI(self):
        #obtenemos el archivo
        path = os.path.join(Variables().ruta_Trabajo,'ICSKREI.xlsx')
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
            
        df2.to_excel(os.path.join(Variables().ruta_procesados,f'InvCost_KWSUR_KREI_SDR_{Variables().FechaExternsionGuardar()}.xlsx'), index=False)