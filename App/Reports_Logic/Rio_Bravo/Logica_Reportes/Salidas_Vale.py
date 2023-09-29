#########################
# DESARROLLADOR
# LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from datetime import *
from .Variables.ContenedorVariables import Variables
class SalidasVale(Variables):
    def SalidasKWRB(self):
        path = os.path.join(Variables().ruta_Trabajo,'SVR.xlsx')

        df = pd.read_excel(path, sheet_name="Hoja2")


        # NOTE Guardamos una copia del documeto en una variable, haciendo uso de el en memoria para no gastar almacenamiento.
        #  SOLO TOMAMOS LAS COLUMNAS QUE VAMOS A UTILIZAR
        df = df.replace(to_replace=';', value='-', regex=True)
        df_format1 = df[df.columns[0:52]].copy()


        # NOTE Le damos formato a las columnas de fecha. Inidcando que solo queremos el formato [dia/mes/año]
        for column_title in df_format1:
            if ("Fecha" in column_title):
                try:
                    df_format1[column_title] = (df_format1[column_title].dt.strftime('%d/%m/%Y'))
                except:
                    pass
            else:
                pass

        # NOTE Guardamos el documento como archivo CSV en la ruta indicada, con una codificacion de salida de "UTF-8", para poder ser detectados los caracteres especiales en cualquier idioma.
        # NOTE También le indicamos que no queremos el id de las columnas.

        columnas_bol=df_format1.select_dtypes(include=bool).columns.tolist()
        df_format1[columnas_bol] = df_format1[columnas_bol].astype(str)
        
        df_format1.to_excel(os.path.join(Variables().ruta_procesados,f'SV_KWRB_SRD_{Variables().FechaExternsionGuardar()}.xlsx'), index=False)
