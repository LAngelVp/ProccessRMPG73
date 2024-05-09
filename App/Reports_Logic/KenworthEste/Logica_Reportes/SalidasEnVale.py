#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
import os
import pandas as pd
from datetime import *
from ...globalModulesShare.ContenedorVariables import Variables
from ...globalModulesShare.ConcesionariosModel import Concesionarios
class SalidasEnVale(Variables):
    def __init__(self):
        self.nombre_doc = 'SVE.xlsx'
        self.concesionario = Concesionarios().concesionarioEste

        path = os.path.join(Variables().ruta_Trabajos_kwe,self.nombre_doc)
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
        Variables().guardar_datos_dataframe(self.nombre_doc, df_format1, self.concesionario)