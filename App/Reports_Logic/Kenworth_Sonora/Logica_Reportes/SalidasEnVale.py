#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from datetime import *
from .Variables.ContenedorVariables import Variables
class SalidasEnVale(Variables):
        def __init__(self):
            super().__init__()
            self.nombre_doc = 'SVS.xlsx'
            path = os.path.join(Variables().ruta_Trabajo,self.nombre_doc)
            df = pd.read_excel(path, sheet_name="Hoja2")
            # NOTE Guardamos una copia del documeto en una variable, haciendo uso de el en memoria para no gastar almacenamiento.
            #  SOLO TOMAMOS LAS COLUMNAS QUE VAMOS A UTILIZAR
            df = df.replace(to_replace=';', value='-', regex=True)
            df_Sin_Requisiciones = df.query("Tipo != ['Requisiciones']").copy()
            df_format1 = df_Sin_Requisiciones[df_Sin_Requisiciones.columns[0:52]].copy()

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
            
            # COMMENT: COMPROBACION DEL NOMBRE DEL DOCUMENTO PARA GUARDARLO
            if (os.path.basename(Variables().comprobar_reporte_documento_rutas(self.nombre_doc)).split(".")[1] == self.nombre_doc.split(".")[1]):
                df_format1.to_excel(Variables().comprobar_reporte_documento_rutas(self.nombre_doc), index=False )
            else:
                df_format1.to_csv(Variables().comprobar_reporte_documento_rutas(self.nombre_doc), encoding="utf-8", index=False )