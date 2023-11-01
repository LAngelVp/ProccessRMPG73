#########################
# DESARROLLADOR
# RMPG - LUIS ANGEL VALLEJO PEREZ
#########################
# importamos librerias
import os
import pandas as pd
import numpy as np
from .Variables.ContenedorVariables import Variables
class BackOrders(Variables):
    def __init__(self):
        # obtenemos el path.
        # leemos el archivo.
        path = os.path.join(Variables().ruta_Trabajo,'BOE.xlsx')
        df = pd.read_excel(path, sheet_name='Hoja2')
        df = df.replace(to_replace=';', value='-', regex=True)
        # copiamos el dataframe
        df2 = df.copy()
        df2.columns = df2.columns.str.replace(' ', '_')
        df2 = df2.rename(columns={ 'Número_BO': 'num'})
        # creamos la columna nueva del numero de back-order
        df2.insert(
            loc  = 2,
            column = 'Número_BO',
            value = 'BO' + df2['num'].map(str),
            allow_duplicates = True
        )
        df2['FechaHoy'] = Variables().date_movement_config_document()

        self.columnas_fecha = df2.select_dtypes(include=['datetime64']).columns
        
        for column_title in self.columnas_fecha:
            try:
                df2[column_title] = pd.to_datetime(df2[column_title], format='%d/%m/%Y', errors = 'coerce')
            except:
                pass
        
        # df2["Fecha_Promesa"] = pd.to_datetime(df2["Fecha_Promesa"])
        # df2['Fecha_Promesa'] = df2['Fecha_Promesa'].dt.date + "/" + df2['Fecha_Promesa'].dt.month + "/" + df2['Fecha_Promesa'].dt.year
        # cambiamos el titulo de las columnas a trabajar.
        df_no_nat = df2.query("Fecha_Alta_FC != ['NaT']").copy()
        df_no_nat["Antigüedad"] = (df_no_nat["FechaHoy"] - df_no_nat["Fecha_Alta_FC"])
        df_nat = df2.query("Fecha_Alta_FC == ['NaT']").copy()
        df_nat["Antigüedad"] = (df_nat["FechaHoy"] - df_nat["Fecha_Alta"])
        df_resta_fechas = pd.concat([df_no_nat, df_nat], join="inner")

        # COLOCAMOS EL FORMATO A TODA COLUMNA QUE SEA TIPO FECHA.
        for column_title in self.columnas_fecha:
            try:
                df_resta_fechas[column_title] = df_resta_fechas[column_title].dt.strftime('%d/%m/%Y')
            except:
                pass
        
        df_resta_fechas["Fecha_Promesa"] = pd.to_datetime(df_resta_fechas["Fecha_Promesa"], format='%d/%m/%Y', errors = 'coerce')
        df_resta_fechas["Fecha_Promesa"] = df_resta_fechas["Fecha_Promesa"].dt.strftime('%d/%m/%Y')
        # cambiamos el formato de las columnas de fecha a trabajar.
        df_resta_fechas.drop(['Folio','FechaHoy','Unidad_Relacionada', 'num'], axis=1, inplace=True)
        
        columnas_bol=df_resta_fechas.select_dtypes(include=bool).columns.tolist()
        df_resta_fechas[columnas_bol] = df_resta_fechas[columnas_bol].astype(str)
        df_resta_fechas['Antigüedad'] = pd.to_numeric(df_resta_fechas['Antigüedad'].dt.days, downcast='integer')

        for column in df_resta_fechas['Antigüedad']:
            if (column < (0)):
                df_resta_fechas['Antigüedad'] = df_resta_fechas['Antigüedad'].replace(column,0)
            else:
                pass
        
        df_resta_fechas.columns = df_resta_fechas.columns.str.replace('_', ' ')

        df_resta_fechas.to_excel(os.path.join(Variables().ruta_procesados,f'KWESTE_BackOrder_RMPG_{Variables().FechaExternsionGuardar()}.xlsx'), index=False)

